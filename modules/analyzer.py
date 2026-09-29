"""
Article Analyzer - Core analysis engine for 5W1H and basic information extraction
Enhanced with robust JSON parsing and fallback mechanisms.
"""

import json
import re
from typing import Dict, Optional
from .gemini_client import GeminiClient


class ArticleAnalyzer:
    """Analyzes articles for basic information, 5W1H, and core thesis."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def analyze_5w1h(self, text: str) -> Dict:
        """Extract 5W1H information matrix from the article."""
        prompt = f"""Analyze this article and return ONLY valid JSON (no markdown, no code blocks, no explanations).

ARTICLE:
{text}

Return this exact JSON structure with all fields filled:

{{
  "title": "article title",
  "summary": "2-3 sentence English summary",
  "summary_bn": "2-3 বাক্যের বাংলা সারাংশ",
  "word_count": 500,
  "reading_level": "Advanced",
  "genre": "Editorial",
  "tone": "Analytical",
  "five_w_one_h": {{
    "who": {{"english": "who is involved", "bangla": "কারা জড়িত"}},
    "what": {{"english": "what happened", "bangla": "কী ঘটেছে"}},
    "when": {{"english": "time context", "bangla": "সময়ের প্রসঙ্গ"}},
    "where": {{"english": "location", "bangla": "স্থান"}},
    "why": {{"english": "reasons", "bangla": "কারণ"}},
    "how": {{"english": "process", "bangla": "প্রক্রিয়া"}}
  }},
  "core_thesis": {{
    "main_argument": "central argument",
    "main_argument_bn": "মূল যুক্তি",
    "focus_maintenance": "how author maintains focus",
    "focus_maintenance_bn": "লেখক কীভাবে ফোকাস বজায় রেখেছেন",
    "supporting_points": ["point 1", "point 2", "point 3"],
    "rhetorical_strategy": "rhetorical approach",
    "rhetorical_strategy_bn": "বাগ্মিতার কৌশল"
  }},
  "basic_facts": ["fact 1", "fact 2", "fact 3"],
  "basic_facts_bn": ["তথ্য ১", "তথ্য ২", "তথ্য ৩"]
}}

CRITICAL RULES:
1. Output ONLY the JSON object - nothing before or after
2. Do NOT use markdown code blocks (no ```json or ```)
3. Use double quotes for all strings
4. Escape any internal quotes with backslash
5. Do not include newlines inside string values (use spaces instead)
6. Ensure all brackets and braces are properly closed"""

        # Try up to 3 times with different strategies
        for attempt in range(3):
            try:
                raw_response = self.client.generate(prompt)
                
                if raw_response.startswith("Error"):
                    continue
                
                # Try parsing with our enhanced parser
                parsed = self._robust_json_parse(raw_response)
                
                if parsed and self._validate_structure(parsed):
                    return parsed
                    
            except Exception as e:
                if attempt == 2:
                    return {
                        "error": f"Analysis failed after 3 attempts: {str(e)}",
                        "raw_response": raw_response if 'raw_response' in dir() else "No response"
                    }
                continue
        
        # Final fallback: return whatever we got
        return {
            "error": "JSON parsing failed - AI returned malformed data",
            "raw_response": raw_response if 'raw_response' in locals() else "No response"
        }

    def _robust_json_parse(self, text: str) -> Optional[Dict]:
        """Enhanced JSON parser with multiple fallback strategies."""
        if not text:
            return None
        
        # Strategy 1: Direct parse after cleanup
        cleaned = self._clean_response(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract JSON object using regex
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Strategy 3: Try to fix common JSON errors
                fixed = self._fix_common_json_errors(json_str)
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    pass
        
        # Strategy 4: Aggressive cleanup and retry
        aggressive = self._aggressive_cleanup(text)
        try:
            return json.loads(aggressive)
        except json.JSONDecodeError:
            return None

    def _clean_response(self, text: str) -> str:
        """Clean common issues from AI response."""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*', '', text)
        
        # Remove leading/trailing whitespace and text
        text = text.strip()
        
        # Remove any text before first { or [
        first_brace = text.find('{')
        first_bracket = text.find('[')
        
        if first_brace == -1 and first_bracket == -1:
            return text
        
        if first_brace == -1:
            start = first_bracket
        elif first_bracket == -1:
            start = first_brace
        else:
            start = min(first_brace, first_bracket)
        
        text = text[start:]
        
        # Remove any text after last } or ]
        last_brace = text.rfind('}')
        last_bracket = text.rfind(']')
        end = max(last_brace, last_bracket)
        
        if end != -1:
            text = text[:end + 1]
        
        return text

    def _fix_common_json_errors(self, text: str) -> str:
        """Fix common JSON errors that AI models make."""
        # Fix trailing commas before } or ]
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        
        # Fix single quotes to double quotes (carefully)
        # Only replace if not inside a string
        text = re.sub(r"(?<![a-zA-Z])'([^']*?)'(?![a-zA-Z])", r'"\1"', text)
        
        # Fix unescaped newlines inside strings
        text = re.sub(r'(?<!\\)\n(?=[^"]*"(?:[^"]|"[^"]*")*$)', ' ', text)
        
        # Fix missing commas between objects
        text = re.sub(r'}\s*{', '},{', text)
        text = re.sub(r']\s*\[', '],[', text)
        
        return text

    def _aggressive_cleanup(self, text: str) -> str:
        """Last resort cleanup for very malformed JSON."""
        # Remove all non-printable characters except newlines and tabs
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        
        # Clean up
        text = self._clean_response(text)
        text = self._fix_common_json_errors(text)
        
        # Try to fix unclosed strings
        # Count quotes and try to balance
        lines = text.split('\n')
        fixed_lines = []
        for line in lines:
            quote_count = line.count('"') - line.count('\\"')
            if quote_count % 2 != 0:
                # Odd number of quotes - try to fix
                line = line.rstrip() + '"'
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)

    def _validate_structure(self, data: Dict) -> bool:
        """Validate that the parsed data has required fields."""
        if not isinstance(data, dict):
            return False
        
        # Check for essential fields
        essential_fields = ["title", "summary", "five_w_one_h"]
        for field in essential_fields:
            if field not in data:
                return False
        
        # Check 5W1H structure
        five_w = data.get("five_w_one_h", {})
        if not isinstance(five_w, dict):
            return False
        
        required_w = ["who", "what", "when", "where", "why", "how"]
        for w in required_w:
            if w not in five_w:
                # Add missing field with placeholder
                five_w[w] = {"english": "Not available", "bangla": "উপলব্ধ নয়"}
        
        # Ensure other fields exist with defaults
        data.setdefault("summary_bn", data.get("summary", ""))
        data.setdefault("word_count", 0)
        data.setdefault("reading_level", "Intermediate")
        data.setdefault("genre", "Article")
        data.setdefault("tone", "Neutral")
        data.setdefault("basic_facts", [])
        data.setdefault("basic_facts_bn", [])
        
        # Ensure core_thesis exists
        if "core_thesis" not in data:
            data["core_thesis"] = {
                "main_argument": "Not analyzed",
                "main_argument_bn": "বিশ্লেষণ করা হয়নি",
                "focus_maintenance": "Not analyzed",
                "focus_maintenance_bn": "বিশ্লেষণ করা হয়নি",
                "supporting_points": [],
                "rhetorical_strategy": "Not analyzed",
                "rhetorical_strategy_bn": "বিশ্লেষণ করা হয়নি"
            }
        
        return True
"""
Article Analyzer - Visual Information Extraction
Extracts raw facts and shows how they grow into sentences.
No explanations. Just facts + visual mapping.
"""

import json
import re
from typing import Dict, Optional
from .gemini_client import GeminiClient


class ArticleAnalyzer:
    """Extracts raw facts and maps them to sentences visually."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def analyze_5w1h(self, text: str) -> Dict:

        prompt = f"""You are a sentence deconstruction engine. Your job:
1. Extract raw facts from the article
2. For each fact, find the EXACT sentence where it appears
3. Mark which words are the RAW INFO and which words are ADDED DECORATION

ARTICLE:
\"\"\"
{text}
\"\"\"

Return ONLY valid JSON:

{{
  "title": "Article title",
  "word_count": 0,
  "reading_level": "Beginner/Intermediate/Advanced/Expert",

  "raw_facts": [
    "Fact 1: bare minimum info",
    "Fact 2: bare minimum info",
    "Fact 3: bare minimum info",
    "Fact 4: bare minimum info",
    "Fact 5: bare minimum info",
    "Fact 6: bare minimum info",
    "Fact 7: bare minimum info",
    "Fact 8: bare minimum info",
    "Fact 9: bare minimum info",
    "Fact 10: bare minimum info"
  ],
  "raw_facts_bn": [
    "তথ্য ১", "তথ্য ২", "তথ্য ৩", "তথ্য ৪", "তথ্য ৫",
    "তথ্য ৬", "তথ্য ৭", "তথ্য ৮", "তথ্য ৯", "তথ্য ১০"
  ],

  "fact_to_sentence": [
    {{
      "fact": "the raw fact",
      "fact_bn": "কাঁচা তথ্য বাংলায়",
      "full_sentence": "the EXACT complete sentence from the article that contains this fact",
      "info_words": ["word1", "word2", "word3"],
      "added_words": ["word4", "word5", "word6"],
      "role": "hook / support / conclusion / context / contrast / data",
      "role_bn": "হুক / সমর্থন / উপসংহার / প্রসঙ্গ / বৈপরীত্য / তথ্য"
    }},
    {{
      "fact": "another raw fact",
      "fact_bn": "আরেকটি কাঁচা তথ্য",
      "full_sentence": "the exact sentence",
      "info_words": ["key", "words"],
      "added_words": ["decoration", "words"],
      "role": "hook",
      "role_bn": "হুক"
    }}
  ],

  "idea_flow": [
    {{
      "facts_used": ["Fact 1", "Fact 2"],
      "idea": "What idea these facts create together",
      "idea_bn": "এই তথ্যগুলো মিলে কী ধারণা তৈরি করে"
    }},
    {{
      "facts_used": ["Fact 3", "Fact 4"],
      "idea": "Next idea",
      "idea_bn": "পরবর্তী ধারণা"
    }},
    {{
      "facts_used": ["Fact 5", "Fact 6", "Fact 7"],
      "idea": "Another idea",
      "idea_bn": "আরেকটি ধারণা"
    }}
  ],

  "hook_analysis": [
    {{
      "fact": "The raw fact used as hook",
      "fact_bn": "হুক হিসেবে ব্যবহৃত কাঁচা তথ্য",
      "hook_sentence": "The exact opening/hook sentence from the article",
      "hook_type": "question / shocking_stat / bold_claim / contrast / anecdote",
      "hook_type_bn": "প্রশ্ন / চমকপ্রদ তথ্য / সাহসী দাবি / বৈপরীত্য / গল্প"
    }}
  ]
}}

CRITICAL RULES:
1. info_words = words that carry the RAW FACT (nouns, verbs, numbers, names)
2. added_words = words added for style (adjectives, adverbs, clauses, connectors)
3. Use EXACT sentences from the article, do not rewrite
4. 8-10 fact_to_sentence entries minimum
5. info_words and added_words should be actual words from the full_sentence
6. Output ONLY JSON, no markdown"""

        for attempt in range(3):
            try:
                raw_response = self.client.generate(prompt)
                if raw_response.startswith("Error"):
                    continue
                parsed = self._robust_json_parse(raw_response)
                if parsed and self._validate(parsed):
                    return parsed
            except Exception as e:
                if attempt == 2:
                    return {"error": str(e), "raw_response": raw_response if 'raw_response' in locals() else ""}
                continue
        return {"error": "Failed", "raw_response": raw_response if 'raw_response' in locals() else ""}

    def _robust_json_parse(self, text: str) -> Optional[Dict]:
        if not text:
            return None
        text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*', '', text).strip()
        f = text.find('{')
        l = text.rfind('}')
        if f == -1 or l == -1:
            return None
        s = text[f:l+1]
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            s = re.sub(r',(\s*[}\]])', r'\1', s)
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                return None

    def _validate(self, data: Dict) -> bool:
        if not isinstance(data, dict):
            return False
        if "raw_facts" not in data or "fact_to_sentence" not in data:
            return False
        data.setdefault("raw_facts_bn", [])
        data.setdefault("idea_flow", [])
        data.setdefault("hook_analysis", [])
        data.setdefault("title", "Untitled")
        data.setdefault("word_count", 0)
        data.setdefault("reading_level", "N/A")
        return True
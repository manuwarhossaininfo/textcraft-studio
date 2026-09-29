"""
Article Analyzer - Deep 5W1H, Idea Generation & Sentence Construction Analysis
Enhanced: Exhaustive detail, idea flow mapping, sentence construction breakdown.
"""

import json
import re
from typing import Dict, Optional
from .gemini_client import GeminiClient


class ArticleAnalyzer:
    """Deep analysis engine for 5W1H, idea generation, and sentence construction."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def analyze_5w1h(self, text: str) -> Dict:
        """Extract exhaustive 5W1H, idea flow, and sentence construction analysis."""

        prompt = f"""You are a world-class linguistic analyst, writing coach, and discourse analyst combined.
Your job is to perform the MOST EXHAUSTIVE AND DETAILED analysis possible of the following article.

ARTICLE:
\"\"\"
{text}
\"\"\"

CRITICAL INSTRUCTIONS:
- Be EXTREMELY detailed. Every field must have 3-5 sentences minimum.
- Do NOT give one-liner answers. Explain thoroughly.
- For 5W1H, extract EVERY possible detail, not just the obvious ones.
- For idea generation, trace HOW the author builds arguments step by step.
- For sentence construction, explain HOW sentences are built from raw facts.
- All Bengali translations must be natural and detailed, not machine-translated.

Return ONLY valid JSON with this exact structure:

{{
  "title": "Article title or best generated title",
  "summary": "4-5 sentence detailed English summary covering all major points",
  "summary_bn": "৪-৫ বাক্যের বিস্তারিত বাংলা সারাংশ",
  "word_count": 0,
  "reading_level": "Beginner/Intermediate/Advanced/Expert",
  "genre": "News/Editorial/Academic/Opinion/Feature/Analysis",
  "tone": "Formal/Informal/Persuasive/Analytical/Critical/Balanced",
  "target_audience": "Who this article is written for",
  "target_audience_bn": "এই আর্টিকেল কাদের জন্য লেখা",

  "five_w_one_h": {{
    "who": {{
      "english": "EXTREMELY detailed answer: ALL people, organizations, groups, stakeholders mentioned. Include their roles, positions, relationships, and significance. 4-6 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত উত্তর বাংলায়: সমস্ত ব্যক্তি, সংগঠন, গোষ্ঠী, স্টেকহোল্ডার। তাদের ভূমিকা, অবস্থান, সম্পর্ক ও গুরুত্ব সহ। ৪-৬ বাক্য।",
      "key_entities": ["Person/Org 1 with role", "Person/Org 2 with role", "Person/Org 3 with role"],
      "relationships": "How the entities relate to each other",
      "relationships_bn": "সত্তাগুলো কীভাবে একে অপরের সাথে সম্পর্কিত"
    }},
    "what": {{
      "english": "EXTREMELY detailed: What exactly happened, what is being discussed, what are the main events/arguments/developments. Include specific data, numbers, policies if mentioned. 5-7 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত: ঠিক কী ঘটেছে, কী আলোচনা হচ্ছে, মূল ঘটনা/যুক্তি/উন্নয়ন কী। নির্দিষ্ট তথ্য, সংখ্যা, নীতি উল্লেখ থাকলে সহ। ৫-৭ বাক্য।",
      "key_events": ["Event/Argument 1", "Event/Argument 2", "Event/Argument 3", "Event/Argument 4"],
      "data_points": ["Specific statistic or data point 1", "Data point 2"],
      "central_conflict": "What is the core tension or debate",
      "central_conflict_bn": "মূল দ্বন্দ্ব বা বিতর্ক কী"
    }},
    "when": {{
      "english": "EXTREMELY detailed: All time references — specific dates, periods, historical context, timeline of events, future projections. 3-5 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত: সমস্ত সময়সূচি — নির্দিষ্ট তারিখ, সময়কাল, ঐতিহাসিক প্রসঙ্গ, ঘটনার কালানুক্রম, ভবিষ্যৎ প্রক্ষেপণ। ৩-৫ বাক্য।",
      "timeline": ["Time point 1: what happened", "Time point 2: what happened", "Time point 3: what happened"],
      "historical_context": "What historical background is relevant",
      "historical_context_bn": "কোন ঐতিহাসিক পটভূমি প্রাসঙ্গিক"
    }},
    "where": {{
      "english": "EXTREMELY detailed: All locations — countries, cities, regions, institutions, virtual spaces. Include geographical and institutional context. 3-5 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত: সমস্ত স্থান — দেশ, শহর, অঞ্চল, প্রতিষ্ঠান, ভার্চুয়াল স্থান। ভৌগোলিক ও প্রাতিষ্ঠানিক প্রসঙ্গ সহ। ৩-৫ বাক্য।",
      "locations": ["Location 1 with significance", "Location 2 with significance"],
      "geopolitical_context": "Geopolitical significance of the locations",
      "geopolitical_context_bn": "স্থানগুলোর ভূ-রাজনৈতিক গুরুত্ব"
    }},
    "why": {{
      "english": "EXTREMELY detailed: ALL reasons, causes, motivations, underlying factors — economic, political, social, environmental, psychological. Go beyond surface-level. 5-7 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত: সমস্ত কারণ, উদ্দেশ্য, অন্তর্নিহিত বিষয় — অর্থনৈতিক, রাজনৈতিক, সামাজিক, পরিবেশগত, মনস্তাত্ত্বিক। পৃষ্ঠতলের বাইরে গিয়ে। ৫-৭ বাক্য।",
      "root_causes": ["Root cause 1", "Root cause 2", "Root cause 3"],
      "surface_causes": ["Surface cause 1", "Surface cause 2"],
      "hidden_motivations": "What unstated motivations might exist",
      "hidden_motivations_bn": "কোন অকথিত উদ্দেশ্য থাকতে পারে"
    }},
    "how": {{
      "english": "EXTREMELY detailed: ALL processes, methods, mechanisms, strategies — how things happened, how systems work, how the author constructs the argument. 5-7 sentences.",
      "bangla": "অত্যন্ত বিস্তারিত: সমস্ত প্রক্রিয়া, পদ্ধতি, কৌশল — কীভাবে ঘটনা ঘটল, কীভাবে সিস্টেম কাজ করে, কীভাবে লেখক যুক্তি গঠন করেছেন। ৫-৭ বাক্য।",
      "processes": ["Process/Mechanism 1", "Process/Mechanism 2", "Process/Mechanism 3"],
      "methods_used": "What methods or approaches are described",
      "methods_used_bn": "কোন পদ্ধতি বা দৃষ্টিভঙ্গি বর্ণনা করা হয়েছে"
    }}
  }},

  "core_thesis": {{
    "main_argument": "The central thesis in 3-4 detailed sentences",
    "main_argument_bn": "মূল যুক্তি ৩-৪টি বিস্তারিত বাক্যে",
    "thesis_position": "Where in the article the thesis appears (opening/middle/closing) and why",
    "thesis_position_bn": "আর্টিকেলের কোথায় থিসিস আছে এবং কেন",
    "focus_maintenance": "DETAILED explanation of how the author maintains focus: paragraph transitions, topic sentences, recurring keywords, thematic threads. 4-6 sentences.",
    "focus_maintenance_bn": "লেখক কীভাবে ফোকাস বজায় রেখেছেন তার বিস্তারিত ব্যাখ্যা: অনুচ্ছেদ সংযোগ, বিষয়বাক্য, পুনরাবৃত্ত শব্দ, থিম্যাটিক সুতা। ৪-৬ বাক্য।",
    "supporting_points": [
      "Supporting point 1 with evidence",
      "Supporting point 2 with evidence",
      "Supporting point 3 with evidence",
      "Supporting point 4 with evidence",
      "Supporting point 5 with evidence"
    ],
    "counterarguments": ["Counterargument 1 the author addresses", "Counterargument 2"],
    "rhetorical_strategy": "DETAILED: What rhetorical strategies — ethos, pathos, logos, analogy, data, anecdote, contrast, concession. 3-4 sentences.",
    "rhetorical_strategy_bn": "বিস্তারিত: কোন বাগ্মিতার কৌশল — এথোস, প্যাথোস, লোগোস, উপমা, তথ্য, গল্প, বৈপরীত্য, স্বীকারোক্তি। ৩-৪ বাক্য।"
  }},

  "idea_generation_map": {{
    "description": "How the author generates and develops ideas throughout the article — the intellectual journey from opening to closing. 3-4 sentences.",
    "description_bn": "লেখক কীভাবে আর্টিকেল জুড়ে ধারণা তৈরি ও বিকশিত করেছেন — শুরু থেকে শেষ পর্যন্ত বুদ্ধিবৃত্তিক যাত্রা। ৩-৪ বাক্য।",
    "idea_flow": [
      {{
        "stage": "Opening Hook",
        "idea": "What idea is planted at the beginning",
        "idea_bn": "শুরুতে কোন ধারণা রোপণ করা হয়েছে",
        "technique": "How the idea is introduced (question/statistic/anecdote/bold claim)",
        "technique_bn": "কীভাবে ধারণাটি উপস্থাপন করা হয়েছে"
      }},
      {{
        "stage": "Context Building",
        "idea": "What background/context is established",
        "idea_bn": "কোন পটভূমি/প্রসঙ্গ স্থাপন করা হয়েছে",
        "technique": "How context is built",
        "technique_bn": "কীভাবে প্রসঙ্গ তৈরি করা হয়েছে"
      }},
      {{
        "stage": "Core Argument Development",
        "idea": "How the main argument is developed and supported",
        "idea_bn": "মূল যুক্তি কীভাবে বিকশিত ও সমর্থিত হয়েছে",
        "technique": "Evidence types used (data/examples/expert quotes/analogies)",
        "technique_bn": "কোন ধরনের প্রমাণ ব্যবহৃত হয়েছে"
      }},
      {{
        "stage": "Counterargument & Nuance",
        "idea": "How opposing views or complexities are introduced",
        "idea_bn": "কীভাবে বিরোধী মত বা জটিলতা আনা হয়েছে",
        "technique": "Concession technique used",
        "technique_bn": "কোন স্বীকারোক্তি কৌশল ব্যবহৃত হয়েছে"
      }},
      {{
        "stage": "Resolution & Call to Action",
        "idea": "How the article concludes and what it leaves the reader with",
        "idea_bn": "কীভাবে আর্টিকেল শেষ হয়েছে এবং পাঠককে কী দিয়ে গেছে",
        "technique": "Closing technique (echo/projection/question/call)",
        "technique_bn": "সমাপনী কৌশল"
      }}
    ],
    "paragraph_to_idea_mapping": [
      "Paragraph 1-2: [What idea] — [How it connects to thesis]",
      "Paragraph 3-4: [What idea] — [How it connects to thesis]",
      "Paragraph 5-6: [What idea] — [How it connects to thesis]",
      "Paragraph 7+: [What idea] — [How it connects to thesis]"
    ]
  }},

  "sentence_construction_analysis": {{
    "description": "How raw facts and ideas are transformed into polished sentences. The alchemy of turning data into prose. 3-4 sentences.",
    "description_bn": "কীভাবে কাঁচা তথ্য ও ধারণা পরিমার্জিত বাক্যে রূপান্তরিত হয়। তথ্যকে গদ্যে পরিণত করার রসায়ন। ৩-৪ বাক্য।",
    "construction_patterns": [
      {{
        "pattern_name": "Fact → Elaboration Pattern",
        "pattern_name_bn": "তথ্য → বিস্তারিতকরণ প্যাটার্ন",
        "raw_fact": "The basic fact before sentence construction",
        "constructed_sentence": "How the author built a full sentence from this fact",
        "construction_steps": [
          "Step 1: Started with the core fact",
          "Step 2: Added a qualifier or context",
          "Step 3: Embedded a subordinate clause for depth",
          "Step 4: Used a powerful verb instead of a weak one"
        ],
        "construction_steps_bn": [
          "ধাপ ১: মূল তথ্য দিয়ে শুরু",
          "ধাপ ২: যোগ্যতা বা প্রসঙ্গ যোগ",
          "ধাপ ৩: গভীরতার জন্য অধীন ক্লজ সন্নিবেশ",
          "ধাপ ৪: দুর্বল ক্রিয়ার বদলে শক্তিশালী ক্রিয়া"
        ]
      }},
      {{
        "pattern_name": "Contrast Pattern",
        "pattern_name_bn": "বৈপরীত্য প্যাটার্ন",
        "raw_fact": "Two contrasting facts",
        "constructed_sentence": "How the author merged them into one powerful sentence",
        "construction_steps": ["Step 1", "Step 2", "Step 3"],
        "construction_steps_bn": ["ধাপ ১", "ধাপ ২", "ধাপ ৩"]
      }},
      {{
        "pattern_name": "Cause-Effect Chain Pattern",
        "pattern_name_bn": "কারণ-ফলাফল শৃঙ্খল প্যাটার্ন",
        "raw_fact": "A chain of cause and effect",
        "constructed_sentence": "How the author wove the chain into prose",
        "construction_steps": ["Step 1", "Step 2", "Step 3"],
        "construction_steps_bn": ["ধাপ ১", "ধাপ ২", "ধাপ ৩"]
      }},
      {{
        "pattern_name": "Data Integration Pattern",
        "pattern_name_bn": "তথ্য সংযোজন প্যাটার্ন",
        "raw_fact": "A statistic or data point",
        "constructed_sentence": "How the author embedded data naturally into a sentence",
        "construction_steps": ["Step 1", "Step 2", "Step 3"],
        "construction_steps_bn": ["ধাপ ১", "ধাপ ২", "ধাপ ৩"]
      }}
    ],
    "idea_to_sentence_pipeline": "DETAILED explanation of the complete pipeline: Raw Observation → Fact Extraction → Idea Formation → Clause Planning → Vocabulary Selection → Sentence Assembly → Stylistic Polish. 4-6 sentences.",
    "idea_to_sentence_pipeline_bn": "সম্পূর্ণ পাইপলাইনের বিস্তারিত ব্যাখ্যা: কাঁচা পর্যবেক্ষণ → তথ্য নিষ্কাশন → ধারণা গঠন → ক্লজ পরিকল্পনা → শব্দ চয়ন → বাক্য সংযোজন → শৈলীগত পরিশীলন। ৪-৬ বাক্য।"
  }},

  "basic_facts": [
    "Stripped fact 1 — pure information, no ornamentation",
    "Stripped fact 2",
    "Stripped fact 3",
    "Stripped fact 4",
    "Stripped fact 5",
    "Stripped fact 6",
    "Stripped fact 7",
    "Stripped fact 8",
    "Stripped fact 9",
    "Stripped fact 10"
  ],
  "basic_facts_bn": [
    "অলংকার ছাড়া মূল তথ্য ১",
    "অলংকার ছাড়া মূল তথ্য ২",
    "অলংকার ছাড়া মূল তথ্য ৩",
    "অলংকার ছাড়া মূল তথ্য ৪",
    "অলংকার ছাড়া মূল তথ্য ৫",
    "অলংকার ছাড়া মূল তথ্য ৬",
    "অলংকার ছাড়া মূল তথ্য ৭",
    "অলংকার ছাড়া মূল তথ্য ৮",
    "অলংকার ছাড়া মূল তথ্য ৯",
    "অলংকার ছাড়া মূল তথ্য ১০"
  ],

  "key_takeaways": [
    "Takeaway 1: What the reader should remember",
    "Takeaway 2",
    "Takeaway 3",
    "Takeaway 4",
    "Takeaway 5"
  ],
  "key_takeaways_bn": [
    "মূল শিক্ষা ১: পাঠকের কী মনে রাখা উচিত",
    "মূল শিক্ষা ২",
    "মূল শিক্ষা ৩",
    "মূল শিক্ষা ৪",
    "মূল শিক্ষা ৫"
  ]
}}

CRITICAL RULES:
1. Output ONLY the JSON object — nothing before or after
2. Do NOT use markdown code blocks
3. Use double quotes for ALL strings
4. Do not include literal newlines inside string values — use spaces
5. Fill EVERY field with detailed, substantive content
6. Every 5W1H answer must be 3-7 sentences, not one-liners
7. Include at least 10 basic facts
8. The idea_generation_map must trace the FULL intellectual journey"""

        for attempt in range(3):
            try:
                raw_response = self.client.generate(prompt)

                if raw_response.startswith("Error"):
                    continue

                parsed = self._robust_json_parse(raw_response)

                if parsed and self._validate_structure(parsed):
                    return parsed

            except Exception as e:
                if attempt == 2:
                    return {
                        "error": f"Analysis failed: {str(e)}",
                        "raw_response": raw_response if 'raw_response' in locals() else "No response"
                    }
                continue

        return {
            "error": "JSON parsing failed after 3 attempts",
            "raw_response": raw_response if 'raw_response' in locals() else "No response"
        }

    def _robust_json_parse(self, text: str) -> Optional[Dict]:
        """Enhanced JSON parser with multiple fallback strategies."""
        if not text:
            return None

        cleaned = self._clean_response(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                fixed = self._fix_common_json_errors(json_str)
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    pass

        aggressive = self._aggressive_cleanup(text)
        try:
            return json.loads(aggressive)
        except json.JSONDecodeError:
            return None

    def _clean_response(self, text: str) -> str:
        text = re.sub(r'```json\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()

        first_brace = text.find('{')
        if first_brace == -1:
            return text
        text = text[first_brace:]

        last_brace = text.rfind('}')
        if last_brace != -1:
            text = text[:last_brace + 1]

        return text

    def _fix_common_json_errors(self, text: str) -> str:
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        text = re.sub(r'}\s*{', '},{', text)
        text = re.sub(r']\s*\[', '],[', text)
        return text

    def _aggressive_cleanup(self, text: str) -> str:
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        text = self._clean_response(text)
        text = self._fix_common_json_errors(text)
        return text

    def _validate_structure(self, data: Dict) -> bool:
        if not isinstance(data, dict):
            return False

        essential = ["title", "summary", "five_w_one_h"]
        for field in essential:
            if field not in data:
                return False

        five_w = data.get("five_w_one_h", {})
        for w in ["who", "what", "when", "where", "why", "how"]:
            if w not in five_w:
                five_w[w] = {"english": "Not available", "bangla": "উপলব্ধ নয়"}

        data.setdefault("summary_bn", data.get("summary", ""))
        data.setdefault("word_count", 0)
        data.setdefault("reading_level", "Intermediate")
        data.setdefault("genre", "Article")
        data.setdefault("tone", "Neutral")
        data.setdefault("basic_facts", [])
        data.setdefault("basic_facts_bn", [])
        data.setdefault("key_takeaways", [])
        data.setdefault("key_takeaways_bn", [])

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

        if "idea_generation_map" not in data:
            data["idea_generation_map"] = {
                "description": "Not analyzed",
                "description_bn": "বিশ্লেষণ করা হয়নি",
                "idea_flow": [],
                "paragraph_to_idea_mapping": []
            }

        if "sentence_construction_analysis" not in data:
            data["sentence_construction_analysis"] = {
                "description": "Not analyzed",
                "description_bn": "বিশ্লেষণ করা হয়নি",
                "construction_patterns": [],
                "idea_to_sentence_pipeline": "Not analyzed",
                "idea_to_sentence_pipeline_bn": "বিশ্লেষণ করা হয়নি"
            }

        return True
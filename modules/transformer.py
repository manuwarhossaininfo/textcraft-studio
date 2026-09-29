"""
Sentence Transformer - Live Sentence Transformation Lab
"""

from typing import Dict
from .gemini_client import GeminiClient


class SentenceTransformer:
    """Transforms basic sentences through 4 levels of sophistication."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def transform(self, raw_text: str) -> Dict:
        """Transform raw text through 4 levels."""
        prompt = f"""You are an expert writing transformation engine. Take the following raw/basic text and transform it through 4 progressively sophisticated levels.

RAW INPUT:
\"\"\"
{raw_text}
\"\"\"

Respond in valid JSON:
{{
    "original_input": "{raw_text}",
    "transformations": [
        {{
            "level": 1,
            "level_name": "Elementary / Basic",
            "level_name_bn": "প্রাথমিক / মৌলিক",
            "text": "Simple, clear sentences with basic vocabulary. Correct but plain.",
            "word_count": 0,
            "characteristics": ["Short sentences", "Basic vocabulary", "Simple structure"],
            "characteristics_bn": ["ছোট বাক্য", "সাধারণ শব্দভান্ডার", "সরল গঠন"]
        }},
        {{
            "level": 2,
            "level_name": "Intermediate (Compound/Complex)",
            "level_name_bn": "মধ্যবর্তী (যৌগিক/জটিল)",
            "text": "Compound and complex sentences with better vocabulary and some connectors.",
            "word_count": 0,
            "characteristics": ["Compound sentences", "Better transitions", "Some academic words"],
            "characteristics_bn": ["যৌগিক বাক্য", "উন্নত সংযোজক", "কিছু একাডেমিক শব্দ"]
        }},
        {{
            "level": 3,
            "level_name": "Advanced Academic",
            "level_name_bn": "উচ্চতর একাডেমিক",
            "text": "Sophisticated academic prose with subordinate clauses, precise vocabulary, and clear argumentation.",
            "word_count": 0,
            "characteristics": ["Subordinate clauses", "Precise terminology", "Academic register"],
            "characteristics_bn": ["অধীন ক্লজ", "সুনির্দিষ্ট পরিভাষা", "একাডেমিক রেজিস্টার"]
        }},
        {{
            "level": 4,
            "level_name": "Masterclass Editorial",
            "level_name_bn": "মাস্টারক্লাস এডিটোরিয়াল",
            "text": "The Economist / Harvard Review quality prose. Elegant, powerful, with sophisticated clause structures, rhetorical devices, and GRE-level vocabulary.",
            "word_count": 0,
            "characteristics": ["Rhetorical devices", "GRE vocabulary", "Masterful clause subordination", "Compelling rhythm"],
            "characteristics_bn": ["বাগ্মিতার কৌশল", "জিআরই শব্দভান্ডার", "দক্ষ ক্লজ সাব-অর্ডিনেশন", "আকর্ষণীয় ছন্দ"]
        }}
    ],
    "level_4_analysis": {{
        "clause_breakdown": [
            {{
                "clause_text": "clause from level 4",
                "clause_type": "type of clause",
                "clause_type_bn": "ক্লজের ধরন বাংলায়"
            }}
        ],
        "gre_words_used": [
            {{
                "word": "GRE word used in Level 4",
                "meaning_bn": "বাংলা অর্থ",
                "replaced_from": "The simpler word it replaced"
            }}
        ],
        "techniques_applied": [
            {{
                "technique": "Technique name",
                "technique_bn": "কৌশলের নাম বাংলায়",
                "example": "How it was applied"
            }}
        ]
    }}
}}"""

        result = self.client.generate_json(prompt)
        if result is None:
            raw = self.client.generate(prompt)
            return {"error": "JSON parsing failed", "raw_response": raw}
        return result
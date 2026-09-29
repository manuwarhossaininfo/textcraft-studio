"""
Vocabulary Processor - GRE High-Frequency Vocabulary Matrix
"""

from typing import Dict, List, Optional
from .gemini_client import GeminiClient


class VocabularyProcessor:
    """Processes articles to extract and elevate vocabulary to GRE level."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def extract_vocabulary(self, text: str) -> Dict:
        """Extract GRE-level vocabulary matrix from the article."""
        prompt = f"""You are a GRE vocabulary expert and linguistic analyst. Analyze the following article and create a comprehensive GRE High-Frequency Vocabulary Matrix.

ARTICLE:
\"\"\"
{text}
\"\"\"

Instructions:
1. Identify 12-18 significant words from the article that are either already advanced OR could be elevated to GRE-level equivalents.
2. For each word, provide the complete analysis.

Respond in valid JSON:
{{
    "vocabulary_matrix": [
        {{
            "basic_word": "the simple/common version of the concept",
            "article_word": "the actual word used in the article",
            "article_sentence": "the exact sentence from the article where this word appears",
            "part_of_speech": "noun/verb/adjective/adverb",
            "bangla_meaning": "বাংলা অর্থ ও সংজ্ঞা",
            "english_definition": "Clear English definition",
            "gre_synonyms": [
                {{"word": "synonym1", "nuance": "subtle difference explained", "nuance_bn": "সূক্ষ্ম পার্থক্য বাংলায়"}},
                {{"word": "synonym2", "nuance": "subtle difference explained", "nuance_bn": "সূক্ষ্ম পার্থক্য বাংলায়"}},
                {{"word": "synonym3", "nuance": "subtle difference explained", "nuance_bn": "সূক্ষ্ম পার্থক্য বাংলায়"}}
            ],
            "antonyms": ["antonym1", "antonym2"],
            "frequency_tier": "Essential / Advanced Editorial / Mastery",
            "root_etymology": "Latin/Greek root and meaning",
            "mnemonic": "Memory hook or trick to remember",
            "mnemonic_bn": "মনে রাখার কৌশল বাংলায়",
            "example_sentence": "A new example sentence using the GRE word",
            "pronunciation": "phonetic pronunciation (IPA or simplified)"
        }}
    ],
    "total_words_analyzed": 0,
    "tier_distribution": {{
        "essential": 0,
        "advanced_editorial": 0,
        "mastery": 0
    }}
}}"""

        result = self.client.generate_json(prompt)
        if result is None:
            raw = self.client.generate(prompt)
            return {"error": "JSON parsing failed", "raw_response": raw}
        return result

    def generate_csv_data(self, vocab_data: Dict) -> str:
        """Generate CSV formatted string from vocabulary data."""
        if "error" in vocab_data or "vocabulary_matrix" not in vocab_data:
            return ""

        lines = [
            "Basic Word,Article Word,Part of Speech,Bangla Meaning,English Definition,"
            "GRE Synonyms,Antonyms,Frequency Tier,Root/Etymology,Mnemonic,Example,Pronunciation"
        ]

        for item in vocab_data["vocabulary_matrix"]:
            synonyms = "; ".join([s.get("word", "") for s in item.get("gre_synonyms", [])])
            antonyms = "; ".join(item.get("antonyms", []))
            line = (
                f'"{item.get("basic_word", "")}","{item.get("article_word", "")}",'
                f'"{item.get("part_of_speech", "")}","{item.get("bangla_meaning", "")}",'
                f'"{item.get("english_definition", "")}","{synonyms}","{antonyms}",'
                f'"{item.get("frequency_tier", "")}","{item.get("root_etymology", "")}",'
                f'"{item.get("mnemonic", "")}","{item.get("example_sentence", "")}",'
                f'"{item.get("pronunciation", "")}"'
            )
            lines.append(line)

        return "\n".join(lines)
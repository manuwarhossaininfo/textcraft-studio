"""
Clause & Grammar X-Ray - Sentence and clause structure analysis
"""

from typing import Dict
from .gemini_client import GeminiClient


class ClauseXRay:
    """Analyzes sentence structures, clause types, and grammatical patterns."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def analyze_clauses(self, text: str) -> Dict:
        """Perform clause and grammar X-Ray on the article."""
        prompt = f"""You are an expert syntactician and grammar analyst. Perform a comprehensive Clause & Grammar X-Ray on the following article.

ARTICLE:
\"\"\"
{text}
\"\"\"

Select the 5-7 MOST complex and interesting sentences from the article. For each sentence, provide a complete syntactic breakdown.

Respond in valid JSON:
{{
    "clause_analysis": [
        {{
            "original_sentence": "The exact sentence from the article",
            "sentence_number": 1,
            "syntactic_formula": "e.g., [Adverbial Clause of Concession] + [Independent Clause] + [Relative Clause]",
            "clause_breakdown": [
                {{
                    "clause_text": "the actual clause text",
                    "clause_type": "Independent Clause / Adverbial Clause of Concession / Relative Clause / Participial Phrase / Noun Clause / etc.",
                    "clause_type_bn": "ক্লজের ধরন বাংলায়",
                    "function": "What role this clause plays in the sentence",
                    "function_bn": "এই ক্লজ বাক্যে কী ভূমিকা পালন করে",
                    "connector": "the subordinating conjunction or relative pronoun used (if any)"
                }}
            ],
            "beginner_version": {{
                "sentences": [
                    "Simple sentence 1 that a beginner would write",
                    "Simple sentence 2",
                    "Simple sentence 3"
                ],
                "explanation_bn": "একজন সাধারণ শিক্ষার্থী কেন এভাবে ৩-৪টি ছোট বাক্যে লিখত তার ব্যাখ্যা"
            }},
            "editorial_technique": {{
                "technique_name": "Name of the writing technique used",
                "technique_name_bn": "ব্যবহৃত লেখার কৌশলের নাম বাংলায়",
                "explanation": "How the author combined clauses and why it's effective",
                "explanation_bn": "লেখক কীভাবে ক্লজগুলো জোড়া লাগিয়েছেন এবং কেন এটি প্রভাবশালী - বিস্তারিত বাংলায়",
                "stylistic_devices": ["device1", "device2"]
            }},
            "grammar_notes_bn": "বাংলায় গুরুত্বপূর্ণ ব্যাকরণগত নোট ও বিশ্লেষণ"
        }}
    ],
    "overall_style_profile": {{
        "dominant_clause_patterns": ["pattern1", "pattern2"],
        "average_clauses_per_sentence": 0,
        "style_description": "Overall writing style description",
        "style_description_bn": "সামগ্রিক লেখার শৈলীর বিবরণ বাংলায়",
        "difficulty_level": "Intermediate/Advanced/Expert"
    }}
}}"""

        result = self.client.generate_json(prompt)
        if result is None:
            raw = self.client.generate(prompt)
            return {"error": "JSON parsing failed", "raw_response": raw}
        return result
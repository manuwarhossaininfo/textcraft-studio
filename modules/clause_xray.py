"""
Clause & Grammar X-Ray - Comprehensive sentence-level analysis
Enhanced: Minimum 15 sentences, full article coverage.
"""

from typing import Dict
from .gemini_client import GeminiClient


class ClauseXRay:
    """Deep clause and grammar analysis for ALL sentences in the article."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def analyze_clauses(self, text: str) -> Dict:
        """Perform exhaustive clause X-Ray on the article — minimum 15 sentences."""

        # Count approximate sentences
        import re
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 20]
        total_sentences = len(sentences)
        target_count = max(15, min(total_sentences, 25))

        prompt = f"""You are an expert syntactician, grammarian, and writing coach.
Perform a COMPREHENSIVE Clause & Grammar X-Ray on the following article.

The article has approximately {total_sentences} sentences.
You MUST analyze AT LEAST {target_count} sentences — pick the most complex, interesting, and instructive ones.
If the article has more than {target_count} sentences, analyze exactly {target_count}.

ARTICLE:
\"\"\"
{text}
\"\"\"

CRITICAL INSTRUCTIONS:
- Analyze AT LEAST {target_count} sentences. This is NON-NEGOTIABLE.
- For EACH sentence, provide a COMPLETE syntactic breakdown.
- Show the Beginner vs Editorial comparison for EVERY sentence.
- Explain in Bengali how each sentence is constructed.
- Number each sentence clearly.

Respond in valid JSON:
{{
    "total_sentences_in_article": {total_sentences},
    "sentences_analyzed": {target_count},
    "clause_analysis": [
        {{
            "sentence_number": 1,
            "original_sentence": "The EXACT complete sentence from the article",
            "sentence_length_words": 0,
            "syntactic_formula": "[Adverbial Clause] + [Independent Clause] + [Relative Clause] + [Participial Phrase]",
            "clause_breakdown": [
                {{
                    "clause_text": "the exact clause text from the sentence",
                    "clause_type": "Independent Clause",
                    "clause_type_bn": "স্বাধীন ক্লজ / প্রধান বাক্যাংশ",
                    "function": "Carries the main assertion of the sentence",
                    "function_bn": "বাক্যের মূল প্রতিপাদ্য বহন করে",
                    "connector": "none / although / while / which / that / because / etc.",
                    "grammar_note": "Specific grammar rule at play",
                    "grammar_note_bn": "নির্দিষ্ট ব্যাকরণ নিয়ম বাংলায়"
                }},
                {{
                    "clause_text": "second clause",
                    "clause_type": "Adverbial Clause of Concession",
                    "clause_type_bn": "বৈপরীত্যসূচক অব্যয়ী ক্লজ",
                    "function": "Acknowledges an opposing reality before the main point",
                    "function_bn": "মূল বক্তব্যের আগে বিরোধী বাস্তবতা স্বীকার করে",
                    "connector": "Although / While / Despite",
                    "grammar_note": "Subordinating conjunction introduces concession",
                    "grammar_note_bn": "অধীন সংযোজক স্বীকারোক্তি প্রবর্তন করে"
                }}
            ],
            "beginner_version": {{
                "sentences": [
                    "Simple sentence 1 a beginner would write",
                    "Simple sentence 2",
                    "Simple sentence 3",
                    "Simple sentence 4"
                ],
                "explanation": "Why a beginner would break this into 3-4 separate sentences",
                "explanation_bn": "একজন সাধারণ শিক্ষার্থী কেন এটিকে ৩-৪টি আলাদা বাক্যে ভাঙত তার বিস্তারিত ব্যাখ্যা"
            }},
            "editorial_technique": {{
                "technique_name": "Name of the specific writing technique",
                "technique_name_bn": "নির্দিষ্ট লেখার কৌশলের নাম বাংলায়",
                "explanation": "DETAILED explanation of how the author combined clauses and why this is more effective than the beginner version. 2-3 sentences.",
                "explanation_bn": "লেখক কীভাবে ক্লজগুলো জোড়া লাগিয়েছেন এবং কেন এটি বিগিনার ভার্সনের চেয়ে বেশি প্রভাবশালী তার বিস্তারিত ব্যাখ্যা। ২-৩ বাক্য।",
                "stylistic_devices": ["Parallelism", "Inversion", "Apposition", "etc."],
                "impact_on_reader": "What effect this sentence structure has on the reader",
                "impact_on_reader_bn": "এই বাক্য গঠনের পাঠকের উপর কী প্রভাব পড়ে"
            }},
            "grammar_deep_dive_bn": "বাংলায় গভীর ব্যাকরণগত বিশ্লেষণ: কোন tense, কোন voice, কোন mood, কোন clause type, কোন conjunction, কোন modifier — সবকিছু বিস্তারিত। ৩-৫ বাক্য।",
            "replication_template": "A fill-in-the-blank template the learner can use to write similar sentences",
            "replication_template_bn": "শিক্ষার্থী অনুরূপ বাক্য লেখার জন্য যে ফাঁকা-পূরণ টেমপ্লেট ব্যবহার করতে পারে"
        }}
    ],
    "overall_style_profile": {{
        "dominant_clause_patterns": [
            "Pattern 1: e.g., Concession + Main + Relative",
            "Pattern 2: e.g., Participial opener + Main clause",
            "Pattern 3: e.g., Conditional + Consequence"
        ],
        "average_clauses_per_sentence": 0,
        "average_sentence_length": 0,
        "longest_sentence_word_count": 0,
        "shortest_sentence_word_count": 0,
        "most_common_connectors": ["although", "while", "which", "that", "because"],
        "style_description": "DETAILED overall writing style description covering sentence variety, rhythm, complexity, and rhetorical sophistication. 4-5 sentences.",
        "style_description_bn": "সামগ্রিক লেখার শৈলীর বিস্তারিত বিবরণ: বাক্যের বৈচিত্র্য, ছন্দ, জটিলতা, এবং বাগ্মিতার পরিশীলন। ৪-৫ বাক্য।",
        "difficulty_level": "Intermediate/Advanced/Expert",
        "readability_assessment": "How readable this style is for different audiences",
        "readability_assessment_bn": "বিভিন্ন শ্রোতাদের জন্য এই শৈলী কতটা পাঠযোগ্য",
        "writing_lessons": [
            "Lesson 1: What a learner can take away from this article's sentence construction",
            "Lesson 2",
            "Lesson 3",
            "Lesson 4",
            "Lesson 5"
        ],
        "writing_lessons_bn": [
            "শিক্ষা ১: এই আর্টিকেলের বাক্য গঠন থেকে শিক্ষার্থী কী শিখতে পারে",
            "শিক্ষা ২",
            "শিক্ষা ৩",
            "শিক্ষা ৪",
            "শিক্ষা ৫"
        ]
    }}
}}

CRITICAL RULES:
1. You MUST include at least {target_count} entries in the clause_analysis array
2. Each sentence must have at least 2-4 clauses in the breakdown
3. Every field must be filled with detailed, substantive content
4. Bengali translations must be natural and detailed
5. Output ONLY valid JSON — no markdown, no explanations outside JSON"""

        result = self.client.generate_json(prompt)
        if result is None:
            raw = self.client.generate(prompt)
            return {"error": "JSON parsing failed", "raw_response": raw}
        return result
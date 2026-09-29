"""
Writing Program - Step-by-Step Advanced Writing Masterclass
"""

from typing import Dict
from .gemini_client import GeminiClient


class WritingProgram:
    """Provides step-by-step writing masterclass based on article analysis."""

    def __init__(self, client: GeminiClient):
        self.client = client

    def generate_masterclass(self, text: str) -> Dict:
        """Generate a comprehensive writing masterclass blueprint."""
        prompt = f"""You are a world-class writing coach who teaches people to write at The Economist and Harvard Business Review level. Based on the following article, create a comprehensive Step-by-Step Advanced Writing Masterclass.

ARTICLE:
\"\"\"
{text}
\"\"\"

Respond in valid JSON:
{{
    "masterclass": {{
        "overview": "Brief overview of what makes this article's writing excellent",
        "overview_bn": "এই আর্টিকেলের লেখা কেন চমৎকার তার সংক্ষিপ্ত বিবরণ বাংলায়",

        "steps": [
            {{
                "step_number": 1,
                "step_name": "Idea Isolation",
                "step_name_bn": "ধারণা পৃথকীকরণ",
                "description": "How to strip away ornament and isolate raw facts/ideas",
                "description_bn": "কীভাবে অলংকার সরিয়ে কাঁচা তথ্য/ধারণা আলাদা করবেন - বিস্তারিত বাংলায়",
                "example_from_article": {{
                    "original": "Original complex sentence from article",
                    "stripped": "The raw fact/idea underneath",
                    "stripped_bn": "মূল কাঁচা তথ্য বাংলায়"
                }},
                "practice_exercise": "Exercise for the learner to practice",
                "practice_exercise_bn": "অনুশীলনের জন্য ব্যায়াম বাংলায়"
            }},
            {{
                "step_number": 2,
                "step_name": "Vocabulary Elevation",
                "step_name_bn": "শব্দভান্ডার উন্নতিকরণ",
                "description": "How to replace basic words with precise, powerful alternatives",
                "description_bn": "কীভাবে সাধারণ শব্দের জায়গায় যথাযথ, শক্তিশালী বিকল্প বসাবেন - বাংলায়",
                "example_from_article": {{
                    "basic": "Basic version with simple words",
                    "elevated": "Article version with elevated vocabulary",
                    "words_changed": [{{"from": "basic", "to": "elevated", "why": "reason", "why_bn": "কারণ বাংলায়"}}]
                }},
                "practice_exercise": "Exercise for the learner",
                "practice_exercise_bn": "অনুশীলন বাংলায়"
            }},
            {{
                "step_number": 3,
                "step_name": "Clause Subordination",
                "step_name_bn": "ক্লজ সাব-অর্ডিনেশন",
                "description": "How to combine simple sentences using subordination",
                "description_bn": "কীভাবে সাধারণ বাক্যগুলোকে সাব-অর্ডিনেশন ব্যবহার করে যুক্ত করবেন - বাংলায়",
                "example_from_article": {{
                    "simple_sentences": ["Simple sentence 1", "Simple sentence 2", "Simple sentence 3"],
                    "combined": "Combined sentence from article",
                    "technique": "Subordination technique used",
                    "technique_bn": "ব্যবহৃত সাব-অর্ডিনেশন কৌশল বাংলায়"
                }},
                "practice_exercise": "Exercise",
                "practice_exercise_bn": "অনুশীলন বাংলায়"
            }},
            {{
                "step_number": 4,
                "step_name": "Stylistic Devices & Inversion",
                "step_name_bn": "অলংকরণ, প্যারালেলিজম ও ইনভার্সন",
                "description": "How to add rhetorical polish",
                "description_bn": "কীভাবে বাগ্মিতার পরিশীলন যোগ করবেন - বাংলায়",
                "devices_found": [
                    {{
                        "device": "Device name (Parallelism/Inversion/Metaphor/etc.)",
                        "device_bn": "কৌশলের নাম বাংলায়",
                        "example": "Example from article",
                        "effect": "What effect it creates",
                        "effect_bn": "এটি কী প্রভাব তৈরি করে বাংলায়"
                    }}
                ],
                "practice_exercise": "Exercise",
                "practice_exercise_bn": "অনুশীলন বাংলায়"
            }},
            {{
                "step_number": 5,
                "step_name": "Rhythm & Cohesion",
                "step_name_bn": "ছন্দ ও প্রাঞ্জলতা",
                "description": "How to ensure flow and coherence",
                "description_bn": "কীভাবে প্রবাহ ও সুসংগতি নিশ্চিত করবেন - বাংলায়",
                "cohesion_devices_used": [
                    {{"device": "device name", "example": "example from article", "device_bn": "বাংলায় নাম"}}
                ],
                "practice_exercise": "Exercise",
                "practice_exercise_bn": "অনুশীলন বাংলায়"
            }}
        ],

        "clause_templates": [
            {{
                "template_name": "Concessive Pivot",
                "template_name_bn": "বৈপরীত্যমূলক পিভট",
                "formula": "Although/While [concession], [main point].",
                "example": "Although X seems Y, the reality is Z.",
                "use_case": "When you need to acknowledge opposing views",
                "use_case_bn": "যখন বিরোধী মতামত স্বীকার করতে হয়"
            }},
            {{
                "template_name": "Participial Cause & Consequence",
                "template_name_bn": "পার্টিসিপিয়াল কারণ ও ফলাফল",
                "formula": "[Present/Past Participle phrase], [main clause].",
                "example": "Driven by mounting pressure, the government reversed its stance.",
                "use_case": "When showing cause-effect elegantly",
                "use_case_bn": "যখন কারণ-ফলাফল মার্জিতভাবে দেখাতে হয়"
            }},
            {{
                "template_name": "Tricolon with Climax",
                "template_name_bn": "ক্লাইম্যাক্সসহ ত্রিবিধ গঠন",
                "formula": "[Item 1], [Item 2], and [most powerful Item 3].",
                "example": "It demands patience, rewards persistence, and ultimately transforms thinking.",
                "use_case": "When building rhetorical emphasis",
                "use_case_bn": "যখন বাগ্মিতায় জোর দিতে হয়"
            }},
            {{
                "template_name": "Inversion for Emphasis",
                "template_name_bn": "জোর দেওয়ার জন্য ইনভার্সন",
                "formula": "[Adverb/Negative] + [Auxiliary] + [Subject] + [Verb]",
                "example": "Rarely has a policy shift generated such widespread controversy.",
                "use_case": "When making a dramatic point",
                "use_case_bn": "যখন নাটকীয় পয়েন্ট তৈরি করতে হয়"
            }},
            {{
                "template_name": "Appositive Insertion",
                "template_name_bn": "অ্যাপোজিটিভ সন্নিবেশ",
                "formula": "[Subject], [appositive phrase], [verb]...",
                "example": "The proposal, a bold departure from convention, drew praise and criticism alike.",
                "use_case": "When adding context without a new sentence",
                "use_case_bn": "যখন নতুন বাক্য ছাড়াই প্রসঙ্গ যোগ করতে হয়"
            }}
        ],

        "editorial_checklist": [
            {{"item": "Does every sentence serve the thesis?", "item_bn": "প্রতিটি বাক্য কি থিসিসকে সেবা করে?", "category": "Focus"}},
            {{"item": "Have you replaced vague words with precise ones?", "item_bn": "আপনি কি অস্পষ্ট শব্দ সুনির্দিষ্ট শব্দ দিয়ে প্রতিস্থাপন করেছেন?", "category": "Vocabulary"}},
            {{"item": "Is there at least one subordinate clause per paragraph?", "item_bn": "প্রতি অনুচ্ছেদে কি অন্তত একটি অধীন ক্লজ আছে?", "category": "Syntax"}},
            {{"item": "Have you varied sentence length for rhythm?", "item_bn": "ছন্দের জন্য বাক্যের দৈর্ঘ্য কি ভিন্ন করেছেন?", "category": "Rhythm"}},
            {{"item": "Does the opening hook the reader?", "item_bn": "শুরুটি কি পাঠককে আকৃষ্ট করে?", "category": "Structure"}},
            {{"item": "Is there logical flow between paragraphs?", "item_bn": "অনুচ্ছেদের মধ্যে কি যৌক্তিক প্রবাহ আছে?", "category": "Cohesion"}},
            {{"item": "Have you used at least two stylistic devices?", "item_bn": "আপনি কি অন্তত দুটি শৈলীগত কৌশল ব্যবহার করেছেন?", "category": "Style"}},
            {{"item": "Does the conclusion echo or advance the opening?", "item_bn": "উপসংহার কি শুরুর প্রতিধ্বনি বা অগ্রগতি?", "category": "Structure"}},
            {{"item": "Is passive voice used sparingly and deliberately?", "item_bn": "কর্মবাচ্য কি সংযতভাবে ও ইচ্ছাকৃতভাবে ব্যবহৃত হয়েছে?", "category": "Grammar"}},
            {{"item": "Would a reader understand the main point in 30 seconds?", "item_bn": "একজন পাঠক কি ৩০ সেকেন্ডে মূল বক্তব্য বুঝতে পারবে?", "category": "Clarity"}}
        ]
    }}
}}"""

        result = self.client.generate_json(prompt)
        if result is None:
            raw = self.client.generate(prompt)
            return {"error": "JSON parsing failed", "raw_response": raw}
        return result
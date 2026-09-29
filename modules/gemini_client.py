"""
Gemini API Client - Handles all communication with Google Gemini API
"""

import google.generativeai as genai
import json
import re
import time
from typing import Optional, Dict, Any


class GeminiClient:
    """Manages Gemini API interactions with retry logic and response parsing."""

    def __init__(self, api_key: str, model_name: str = "gemini-3.5-flash-lite"):
        """Initialize the Gemini client."""
        self.api_key = api_key
        self.model_name = model_name
        self._configure()

    def _configure(self):
        """Configure the Gemini API."""
        genai.configure(api_key=self.api_key)

        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=65536,
        )

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

    def generate(self, prompt: str, max_retries: int = 3) -> str:
        """Generate response from Gemini with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text
                else:
                    if hasattr(response, 'prompt_feedback'):
                        return f"Error: Response blocked. Feedback: {response.prompt_feedback}"
                    return "Error: Empty response received."
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                    continue
                return f"Error after {max_retries} attempts: {str(e)}"

    def generate_json(self, prompt: str, max_retries: int = 3) -> Optional[Dict]:
        """Generate and parse JSON response from Gemini."""
        json_prompt = prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown code blocks, no extra text."
        response = self.generate(json_prompt, max_retries)

        if response.startswith("Error"):
            return None

        return self._parse_json(response)

    def _parse_json(self, text: str) -> Optional[Dict]:
        """Parse JSON from various response formats."""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object or array
            json_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            return None
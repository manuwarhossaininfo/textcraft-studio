"""
Utility Functions
"""

import re
from typing import Optional


class Utils:
    """Utility helper functions."""

    @staticmethod
    def truncate_text(text: str, max_chars: int = 15000) -> str:
        """Truncate text to max characters while preserving sentence boundaries."""
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars]
        last_period = truncated.rfind('.')
        if last_period > max_chars * 0.7:
            return truncated[:last_period + 1]
        return truncated + "..."

    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text."""
        return len(text.split())

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if string is a valid URL."""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return url_pattern.match(url) is not None

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def get_tier_color(tier: str) -> str:
        """Get color for frequency tier badge."""
        tier_lower = tier.lower()
        if "essential" in tier_lower:
            return "#28a745"
        elif "advanced" in tier_lower or "editorial" in tier_lower:
            return "#fd7e14"
        elif "mastery" in tier_lower:
            return "#dc3545"
        return "#6c757d"

    @staticmethod
    def get_tier_emoji(tier: str) -> str:
        """Get emoji for frequency tier."""
        tier_lower = tier.lower()
        if "essential" in tier_lower:
            return "🟢"
        elif "advanced" in tier_lower or "editorial" in tier_lower:
            return "🟠"
        elif "mastery" in tier_lower:
            return "🔴"
        return "⚪"
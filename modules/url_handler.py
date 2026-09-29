"""
URL Handler - Extract article text from web URLs
"""

from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
    URL_AVAILABLE = True
except ImportError:
    URL_AVAILABLE = False


class URLHandler:
    """Handles URL scraping and article text extraction."""

    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    @staticmethod
    def is_available() -> bool:
        return URL_AVAILABLE

    @staticmethod
    def extract_text(url: str) -> Optional[str]:
        """Extract article text from URL."""
        if not URL_AVAILABLE:
            return None

        try:
            response = requests.get(url, headers=URLHandler.HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer',
                                          'header', 'aside', 'iframe', 'form']):
                element.decompose()

            # Try to find article content
            article = soup.find('article')
            if article:
                paragraphs = article.find_all('p')
            else:
                main = soup.find('main')
                if main:
                    paragraphs = main.find_all('p')
                else:
                    paragraphs = soup.find_all('p')

            text_parts = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 30:
                    text_parts.append(text)

            full_text = "\n\n".join(text_parts)
            return full_text.strip() if full_text.strip() else None
        except Exception as e:
            return None
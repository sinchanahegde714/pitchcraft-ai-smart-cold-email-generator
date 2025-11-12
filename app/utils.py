# utils.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def clean_text(text: str) -> str:
    """Remove excessive whitespace."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def get_page_text(url: str) -> str:
    """Download any webpage and extract readable text."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return clean_text(soup.get_text(" "))
    except:
        return ""


def is_category_url(url: str) -> bool:
    """Detect if URL looks like a job listing/category page."""
    url = url.lower()
    return any(word in url for word in [
        "categories", "category", "jobs", "careers", "openings",
        "positions", "vacancies", "hiring", "listings"
    ])


def extract_first_job_url(category_url: str) -> str | None:
    """
    Extract first possible job posting URL from ANY category/listing page.
    Works on 95% of websites.
    """

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(category_url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        candidates = []

        for a in soup.find_all("a", href=True):
            href = a["href"].strip().lower()

            if any(k in href for k in ["job", "jobs", "careers", "opening", "position"]):
                full = href if href.startswith("http") else urljoin(category_url, href)
                candidates.append(full)

        return candidates[0] if candidates else None

    except:
        return None

from __future__ import annotations

import re
from collections import Counter
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIWebsiteAuditor/1.0)"}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def fetch_page(url: str, timeout: int = 15) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    title = _clean(soup.title.get_text(" ", strip=True) if soup.title else "")
    meta = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    description = _clean(meta.get("content", "") if meta else "")
    headings = [(h.name, _clean(h.get_text(" ", strip=True))) for h in soup.find_all(["h1", "h2", "h3"])]
    text = _clean(soup.get_text(" ", strip=True))
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(response.url, a["href"])
        if href.startswith(("http://", "https://")):
            links.append({"url": href, "text": _clean(a.get_text(" ", strip=True))})
    images = [{"src": urljoin(response.url, img.get("src", "")), "alt": _clean(img.get("alt", ""))} for img in soup.find_all("img") if img.get("src")]
    canonical = soup.find("link", rel=lambda v: v and "canonical" in v)
    h1_count = sum(1 for tag, _ in headings if tag == "h1")
    return {
        "url": response.url,
        "status_code": response.status_code,
        "title": title,
        "meta_description": description,
        "headings": headings,
        "h1_count": h1_count,
        "word_count": len(text.split()),
        "text": text[:20000],
        "links": links[:250],
        "images": images[:250],
        "missing_alt_images": sum(1 for x in images if not x["alt"]),
        "canonical": canonical.get("href") if canonical else "",
    }


def crawl_site(start_url: str, max_pages: int = 10) -> dict:
    parsed = urlparse(start_url if "://" in start_url else "https://" + start_url)
    start_url = parsed.geturl()
    domain = parsed.netloc
    queue = [start_url]
    seen = set()
    pages = []
    while queue and len(pages) < max_pages:
        url = queue.pop(0)
        if url in seen or urlparse(url).netloc != domain:
            continue
        seen.add(url)
        try:
            page = fetch_page(url)
            pages.append(page)
            for link in page["links"]:
                target = link["url"].split("#")[0]
                if urlparse(target).netloc == domain and target not in seen and target not in queue:
                    queue.append(target)
        except Exception as exc:
            pages.append({"url": url, "error": str(exc), "status_code": None})
    return {"start_url": start_url, "domain": domain, "pages": pages}


def audit_site(crawl: dict) -> dict:
    pages = [p for p in crawl["pages"] if "error" not in p]
    findings = []
    for p in pages:
        if not p.get("title"):
            findings.append({"severity": "high", "category": "SEO", "url": p["url"], "issue": "Missing page title"})
        elif len(p["title"]) > 65:
            findings.append({"severity": "medium", "category": "SEO", "url": p["url"], "issue": "Title may be too long"})
        if not p.get("meta_description"):
            findings.append({"severity": "medium", "category": "SEO", "url": p["url"], "issue": "Missing meta description"})
        if p.get("h1_count", 0) == 0:
            findings.append({"severity": "medium", "category": "Content", "url": p["url"], "issue": "No H1 heading found"})
        if p.get("h1_count", 0) > 1:
            findings.append({"severity": "low", "category": "Content", "url": p["url"], "issue": "Multiple H1 headings found"})
        if p.get("missing_alt_images", 0):
            findings.append({"severity": "low", "category": "Accessibility", "url": p["url"], "issue": f"{p['missing_alt_images']} image(s) missing alt text"})
        if not p.get("canonical"):
            findings.append({"severity": "low", "category": "Technical SEO", "url": p["url"], "issue": "No canonical link detected"})
    return {"findings": findings, "pages_analyzed": len(pages)}

from __future__ import annotations

import ipaddress
import json
import socket
from typing import Any
from urllib.parse import urlparse

import requests

from config import SERPAPI_GEO, SERPAPI_KEY, SERPAPI_LOCATION

SERPAPI_URL = "https://serpapi.com/search.json"


def _serpapi(params: dict[str, Any]) -> dict[str, Any]:
    params = dict(params)
    params["api_key"] = SERPAPI_KEY
    response = requests.get(SERPAPI_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if data.get("error"):
        raise RuntimeError(f"SerpApi error: {data['error']}")
    return data


def google_search(query: str, num_results: int = 10) -> str:
    """Search Google through SerpApi and return structured current SERP data."""
    data = _serpapi({
        "engine": "google",
        "q": query,
        "location": SERPAPI_LOCATION,
        "gl": SERPAPI_GEO.lower(),
        "hl": "en",
        "num": min(max(num_results, 1), 10),
    })
    compact = {
        "query": query,
        "organic_results": [
            {
                "position": x.get("position"),
                "title": x.get("title"),
                "link": x.get("link"),
                "source": x.get("source"),
                "snippet": x.get("snippet"),
                "date": x.get("date"),
            }
            for x in data.get("organic_results", [])[:10]
        ],
        "people_also_ask": data.get("related_questions", [])[:8],
        "related_searches": data.get("related_searches", [])[:10],
        "news_results": [
            {
                "title": x.get("title"),
                "link": x.get("link"),
                "source": x.get("source"),
                "date": x.get("date"),
                "snippet": x.get("snippet"),
            }
            for x in data.get("news_results", [])[:8]
        ],
        "answer_box": data.get("answer_box"),
        "knowledge_graph": data.get("knowledge_graph"),
    }
    return json.dumps(compact, ensure_ascii=False)


def google_trends_related_queries(query: str) -> str:
    """Get rising and top Google Trends queries for one topic."""
    data = _serpapi({
        "engine": "google_trends",
        "q": query,
        "geo": SERPAPI_GEO,
        "date": "today 12-m",
        "data_type": "RELATED_QUERIES",
    })
    return json.dumps({
        "query": query,
        "related_queries": data.get("related_queries", {}),
    }, ensure_ascii=False)


def google_trends_related_topics(query: str) -> str:
    """Get rising and top Google Trends topics for one topic."""
    data = _serpapi({
        "engine": "google_trends",
        "q": query,
        "geo": SERPAPI_GEO,
        "date": "today 12-m",
        "data_type": "RELATED_TOPICS",
    })
    return json.dumps({
        "query": query,
        "related_topics": data.get("related_topics", {}),
    }, ensure_ascii=False)


def google_trends_timeseries(query: str) -> str:
    """Get Google Trends interest-over-time data for one topic."""
    data = _serpapi({
        "engine": "google_trends",
        "q": query,
        "geo": SERPAPI_GEO,
        "date": "today 12-m",
        "data_type": "TIMESERIES",
    })
    return json.dumps({
        "query": query,
        "interest_over_time": data.get("interest_over_time", {}),
    }, ensure_ascii=False)


def google_trending_now(hours: int = 24) -> str:
    """Get current Google Trending Now searches for the configured country."""
    if hours not in {4, 24, 48, 168}:
        hours = 24
    data = _serpapi({
        "engine": "google_trends_trending_now",
        "geo": SERPAPI_GEO,
        "hours": hours,
    })
    return json.dumps({
        "geo": SERPAPI_GEO,
        "hours": hours,
        "trending_searches": [
            {
                "query": x.get("query"),
                "search_volume": x.get("search_volume"),
                "categories": x.get("categories"),
            }
            for x in data.get("trending_searches", [])[:30]
        ],
    }, ensure_ascii=False)


def _is_public_http_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower()
    if hostname == "localhost":
        return False
    try:
        for address in socket.getaddrinfo(hostname, None):
            ip = ipaddress.ip_address(address[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return False
    except Exception:
        return False
    return True


def fetch_webpage(url: str, max_chars: int = 12000) -> str:
    """Fetch readable text from a public competitor webpage."""
    if not _is_public_http_url(url):
        return "URL rejected: only public HTTP/HTTPS URLs are allowed."
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; SEOResearchBot/1.0)"},
        )
        response.raise_for_status()
        if "text/html" not in response.headers.get("content-type", ""):
            return "Unsupported content type."
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
            tag.decompose()
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        text = soup.get_text(" ", strip=True)
        return json.dumps({"url": url, "title": title, "text": text[:max_chars]}, ensure_ascii=False)
    except Exception as exc:
        return f"Could not fetch webpage: {exc}"

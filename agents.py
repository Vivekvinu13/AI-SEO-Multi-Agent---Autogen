from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import OPENAI_MODEL
from tools import (
    fetch_webpage,
    google_search,
    google_trending_now,
    google_trends_related_queries,
    google_trends_related_topics,
    google_trends_timeseries,
)


def create_model_client():
    # Keep the client compatible with AutoGen 0.7.x / OpenAI API.
    # Do not send parallel_tool_calls when an agent has no tools.
    return OpenAIChatCompletionClient(model=OPENAI_MODEL)


def create_agents(model_client):
    research_agent = AssistantAgent(
        name="research_agent",
        description="Researches current SEO opportunities using Google Search and Google Trends.",
        model_client=model_client,
        tools=[
            google_search,
            google_trending_now,
            google_trends_related_queries,
            google_trends_related_topics,
            google_trends_timeseries,
            fetch_webpage,
        ],
        max_tool_iterations=10,
        reflect_on_tool_use=True,
        system_message="""
You are the Research Agent in an SEO content pipeline.

Use the live tools. Do not claim a topic is trending without evidence.
Research the exact topic, current/latest variations, Google Trends related
queries/topics, Trending Now when useful, Google SERPs, People Also Ask,
related searches, news, and up to 3 competitor pages when useful.

Return ONLY valid JSON:
{
  "topic": "...",
  "recommended_angle": "...",
  "trend_evidence": [{"signal": "...", "evidence": "...", "source": "..."}],
  "search_intent": "...",
  "primary_keyword": "...",
  "secondary_keywords": ["..."],
  "long_tail_keywords": ["..."],
  "people_also_ask": ["..."],
  "related_searches": ["..."],
  "competitors": [{"title": "...", "url": "...", "why_relevant": "..."}],
  "content_gaps": ["..."],
  "recommended_title": "...",
  "recommended_outline": ["..."],
  "sources": [{"title": "...", "url": "..."}],
  "confidence": "high|medium|low"
}
Do not fabricate URLs or statistics.
""",
    )

    writer_agent = AssistantAgent(
        name="content_writer_agent",
        description="Writes an SEO article from a research brief.",
        model_client=model_client,
        system_message="""
You are the Content Writer Agent.
Write a publication-ready article from the research brief.
Match search intent, use keywords naturally, use one H1 and logical H2/H3
headings, answer user questions, avoid filler and keyword stuffing, and do
not invent facts or citations.

Return ONLY valid JSON:
{
  "title": "...",
  "meta_title": "...",
  "meta_description": "...",
  "slug": "...",
  "article_markdown": "...",
  "faq": [{"question": "...", "answer": "..."}]
}
""",
    )

    seo_agent = AssistantAgent(
        name="seo_optimizer_agent",
        description="Audits and optimizes article SEO.",
        model_client=model_client,
        system_message="""
You are the SEO Optimization Agent.

Audit the article for search intent, title/meta, primary and semantic
keywords, headings, topical completeness, PAA coverage, featured snippets,
readability, keyword stuffing, repetition, internal/external linking,
FAQ/schema opportunities, trust signals, and unsupported claims.

Then rewrite the article to fix the issues.

Return ONLY valid JSON:
{
  "seo_score": 0,
  "audit": [{"issue": "...", "severity": "high|medium|low", "fix": "..."}],
  "keyword_plan": {"primary": "...", "secondary": ["..."], "used_naturally": true},
  "meta_title": "...",
  "meta_description": "...",
  "slug": "...",
  "schema_recommendations": ["..."],
  "internal_link_opportunities": ["..."],
  "external_source_opportunities": ["..."],
  "optimized_article_markdown": "..."
}

Never promise a ranking position.
""",
    )

    reviewer_agent = AssistantAgent(
        name="reviewer_agent",
        description="Performs final editorial and factual review.",
        model_client=model_client,
        system_message="""
You are the Final Reviewer Agent.
Review the research, draft, and SEO-optimized article. Fix factual
inconsistency, weak writing, repetition, unsupported claims, structural
problems, and SEO mistakes. Do not invent facts.

Return ONLY valid JSON:
{
  "final_seo_score": 0,
  "changes_made": ["..."],
  "remaining_recommendations": ["..."],
  "final_article_markdown": "..."
}
""",
    )

    return research_agent, writer_agent, seo_agent, reviewer_agent

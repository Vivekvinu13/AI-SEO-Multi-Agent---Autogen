from __future__ import annotations

import json

from agents import create_agents, create_model_client


def _last_text(result):
    for message in reversed(result.messages):
        content = getattr(message, "content", None)
        if isinstance(content, str) and content.strip():
            return content.strip()
    return ""


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:] if lines and lines[0].startswith("```") else lines
        lines = lines[:-1] if lines and lines[-1].strip() == "```" else lines
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


async def run_pipeline(topic: str) -> dict:
    model_client = create_model_client()
    try:
        research_agent, writer_agent, seo_agent, reviewer_agent = create_agents(model_client)

        research_result = await research_agent.run(task=f"""
Research this SEO topic using your live search and Google Trends tools:

{topic}

Return the structured research brief requested in your instructions.
""")
        research = _parse_json(_last_text(research_result))

        writer_result = await writer_agent.run(task=f"""
Create the article from this research brief:

{json.dumps(research, ensure_ascii=False, indent=2)}
""")
        writer = _parse_json(_last_text(writer_result))

        seo_result = await seo_agent.run(task=f"""
Research brief:
{json.dumps(research, ensure_ascii=False, indent=2)}

Article:
{json.dumps(writer, ensure_ascii=False, indent=2)}

Audit and optimize the article.
""")
        seo = _parse_json(_last_text(seo_result))

        reviewer_result = await reviewer_agent.run(task=f"""
Research brief:
{json.dumps(research, ensure_ascii=False, indent=2)}

Original article:
{json.dumps(writer, ensure_ascii=False, indent=2)}

SEO optimization:
{json.dumps(seo, ensure_ascii=False, indent=2)}

Perform the final review.
""")
        reviewer = _parse_json(_last_text(reviewer_result))

        return {
            "topic": topic,
            "research": research,
            "writer": writer,
            "seo": seo,
            "reviewer": reviewer,
        }
    finally:
        await model_client.close()

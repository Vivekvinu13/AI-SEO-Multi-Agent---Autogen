# SEO Intelligence Studio

A Streamlit + AutoGen project with two workspaces:

1. **SEO Content Generator** — Research → Write → SEO Optimize → Review using SerpApi/Google Trends.
2. **Website Auditor** — Crawl an accessible site and report basic SEO, metadata, heading, accessibility and canonical issues.

> Data/claim verification should use trusted reference sources. A crawler finding is not proof that a business claim or nutrition value is wrong.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
streamlit run app.py
```

Set `OPENAI_API_KEY` and `SERPAPI_KEY` in `.env`.

## Git

```bash
git init
git add .
git commit -m "Build SEO intelligence Streamlit app"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

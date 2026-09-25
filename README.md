# AI SEO Multi-Agent — AutoGen

An AI-powered **SEO research, content generation, optimization, and website auditing platform** built with **Microsoft AutoGen, OpenAI, SerpApi, and Streamlit**.

The application uses multiple specialized AI agents to research topics, generate SEO-optimized content, review the content, and audit websites for SEO, content, and potential factual inconsistencies.

---

## 🚀 Features

### 1. AI SEO Content Generator

Enter a topic and let the multi-agent workflow produce an SEO-focused article.

The workflow includes:

* 🔎 SEO research
* 📊 Keyword research
* 📈 Search-result analysis
* 🧩 Content-gap identification
* 📝 Article generation
* 🎯 SEO optimization
* 🔍 Final content review

The final output can include:

* Research findings
* Draft article
* SEO audit
* Optimized final article
* Structured JSON results

---

### 2. Multi-Agent Architecture

The application separates responsibilities between specialized AI agents.

```text
                    User Topic
                        │
                        ▼
              ┌───────────────────┐
              │  Research Agent   │
              │                   │
              │ Keywords          │
              │ SERP              │
              │ Competitors       │
              │ PAA               │
              │ Content Gaps      │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Content Writer    │
              │      Agent        │
              │                   │
              │ SEO Article       │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  SEO Optimizer    │
              │      Agent        │
              │                   │
              │ Keywords          │
              │ Headings          │
              │ Metadata          │
              │ Search Intent     │
              │ Content Gaps      │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  Reviewer Agent   │
              │                   │
              │ Quality           │
              │ Accuracy          │
              │ SEO               │
              │ Readability       │
              └─────────┬─────────┘
                        │
                        ▼
                  Final Article
```

---

## 🌐 Website Auditor

The project also supports website-level auditing.

Provide a website URL and the system can crawl a configurable number of pages and analyze the available content.

The website audit can identify potential issues related to:

### SEO

* Missing page titles
* Missing meta descriptions
* Heading structure
* Content quality
* Keyword-related issues
* Internal linking
* Search-intent alignment
* Structured data opportunities

### Content

* Thin content
* Repeated content
* Missing important information
* Content structure
* Page-level issues

### Consistency & Verification

The audit architecture is designed to identify potentially inconsistent information across pages.

Examples include:

* Different product information on different pages
* Conflicting nutritional information
* Different ingredient information
* Inconsistent specifications
* Conflicting numbers or measurements
* Claims that may require verification

The system should treat these findings as **potential discrepancies requiring verification**, rather than automatically declaring information false.

---

# 🧠 Agent Responsibilities

## Research Agent

The Research Agent gathers information needed to create an SEO-focused article.

Typical research includes:

* Primary keywords
* Secondary keywords
* Related keywords
* Search intent
* SERP results
* Competitor pages
* People Also Ask questions
* Content gaps
* Topics covered by competing pages
* Potential article structure

Search data is obtained using **SerpApi**.

---

## Content Writer Agent

The Content Writer receives the research output and creates the first article draft.

The writer focuses on:

* Search intent
* Clear structure
* Natural keyword usage
* Reader usefulness
* Headings
* Examples
* Readability
* Factual caution

The writer does not perform the primary SERP research itself.

---

## SEO Optimizer Agent

The SEO Optimizer audits and improves the generated article.

It can evaluate:

* Primary keyword usage
* Secondary keyword coverage
* Semantic relevance
* Search intent
* Title
* Meta title
* Meta description
* H1/H2/H3 structure
* Content depth
* Content gaps
* Featured-snippet opportunities
* People Also Ask coverage
* Internal-link opportunities
* External references
* Schema recommendations
* Readability
* Keyword stuffing
* Repetition
* Unsupported claims

The SEO score produced by the system is an **AI-generated audit score**.

It should not be interpreted as a prediction of a Google ranking.

---

## Reviewer Agent

The Reviewer performs the final quality check.

It reviews:

* Factual consistency
* Content quality
* SEO implementation
* Search intent
* Readability
* Structure
* Unsupported claims
* Potential keyword stuffing
* Overall completeness

The reviewer then produces the final version of the article.

---

# 🔎 SEO Research

The project uses **SerpApi** for search-engine research.

The research layer can be used to retrieve information such as:

* Search results
* Related search information
* Competitor URLs
* Search-result titles
* Search-result snippets
* People Also Ask data, where available

This information is passed to the AI agents as research context.

---

# 🏗️ Project Architecture

```text
seo_multi_agent/
│
├── app.py
├── agents.py
├── workflow.py
├── tools.py
├── audit.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── .env              # Local only - DO NOT COMMIT
├── .venv/            # Local virtual environment
└── __pycache__/      # Python generated files
```

---

# 📁 File Descriptions

## `app.py`

The Streamlit frontend.

Provides:

* SEO Content Generator
* Website Auditor
* Input forms
* Workflow execution
* Results display
* Research tabs
* Draft display
* SEO audit display
* Final article display
* Website audit findings
* JSON output/download

---

## `agents.py`

Contains the AI agent definitions and their responsibilities.

Typical agents include:

* Research Agent
* Content Writer Agent
* SEO Optimizer Agent
* Reviewer Agent

---

## `workflow.py`

Controls the SEO content-generation workflow.

The workflow coordinates the agents and passes information between them.

Typical flow:

```text
Topic
  ↓
Research
  ↓
Draft
  ↓
SEO Optimization
  ↓
Review
  ↓
Final Article
```

---

## `tools.py`

Contains tools used by the AI agents.

Examples include search/research functionality used to gather external SEO information.

---

## `audit.py`

Contains the website crawling and auditing functionality.

The website auditor is responsible for:

1. Accepting a website URL
2. Crawling pages
3. Extracting relevant page information
4. Auditing the pages
5. Producing structured findings

---

## `config.py`

Contains project configuration and environment-variable handling.

API keys and secrets should be loaded from `.env`.

---

# ⚙️ Requirements

Recommended environment:

* Python 3.11+
* Streamlit
* AutoGen AgentChat
* AutoGen Extensions
* OpenAI
* SerpApi

The exact Python packages and versions used by the project are defined in:

```text
requirements.txt
```

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Vivekvinu13/AI-SEO-Multi-Agent---Autogen.git
```

Move into the project:

```bash
cd AI-SEO-Multi-Agent---Autogen
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a local `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

Do **not** commit your `.env` file.

The repository should contain:

```text
.env.example
```

with placeholder values, while the real `.env` remains local.

Example `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

---

# ▶️ Running the Application

Start Streamlit with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open that URL in your browser.

---

# 📝 Using the SEO Content Generator

1. Start the application.
2. Select **SEO Content Generator**.
3. Enter a topic.

For example:

```text
Best running shoes for beginners
```

4. Click:

```text
Generate SEO Article
```

5. The system runs the agent workflow.

You can then inspect:

* Research
* Draft
* SEO Audit
* Final Article
* JSON output

---

# 🌐 Using the Website Auditor

1. Select **Website Auditor**.
2. Enter a website URL.

Example:

```text
https://example.com
```

3. Select the maximum number of pages to crawl.
4. Start the audit.

The application crawls the website and produces findings for the discovered pages.

Findings are categorized by severity, such as:

* High
* Medium
* Low

The audit also provides page-level information and structured JSON output.

---

# 🔍 Factual Consistency Auditing

Website auditing can be extended beyond traditional SEO.

For example, a product website might contain:

### Page A

```text
Serving size: 250 ml
Calories: 100
```

### Page B

```text
Serving size: 250 ml
Calories: 120
```

The system can identify this as a:

```text
Potential cross-page inconsistency
```

The correct workflow is then to verify the information against an authoritative source.

Potential authoritative sources may include:

* Official manufacturer documentation
* Government sources
* Regulatory databases
* Official product documentation
* Approved reference datasets

The AI should not automatically assume that one page is correct simply because another page contains different information.

---

# ⚠️ Important Accuracy Note

This project uses AI-generated analysis.

AI-generated SEO recommendations and audit findings should be reviewed before being used in production.

In particular:

* SEO scores are not Google ranking scores.
* AI-generated factual claims require verification.
* A detected inconsistency is not automatically proof that information is incorrect.
* Search results can change over time.
* Website content can change after an audit.
* Crawling may not discover every page on a website.
* Some websites may block automated requests.
* JavaScript-rendered content may not be available to a basic crawler.
* External data sources may contain errors.

For production use, important claims should be verified against trusted sources.

---

# 🔒 Security

Never commit API keys or other secrets.

The following files/directories should remain local:

```text
.env
.venv/
__pycache__/
*.pyc
```

The `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Before pushing to GitHub, verify:

```powershell
git status --ignored
```

You should see `.env` under ignored files.

You can also verify that `.env` is not tracked:

```powershell
git ls-files .env
```

If this command returns nothing, `.env` is not tracked by Git.

---

# 📦 GitHub Setup

Initialize Git:

```bash
git init
```

Add the project:

```bash
git add .
```

Check what will be committed:

```bash
git status
```

Create the first commit:

```bash
git commit -m "Initial SEO multi-agent application"
```

Set the main branch:

```bash
git branch -M main
```

Add the GitHub repository:

```bash
git remote add origin https://github.com/Vivekvinu13/AI-SEO-Multi-Agent---Autogen.git
```

Push:

```bash
git push -u origin main
```

---

# 🔄 Future Improvements

Possible future improvements include:

## SEO

* Google Search Console integration
* Google Analytics integration
* Keyword tracking
* Historical ranking tracking
* Competitor monitoring
* SERP position tracking
* Automatic internal-link suggestions
* Automatic schema generation

## Website Auditing

* Sitemap discovery
* Robots.txt analysis
* Canonical analysis
* Broken-link detection
* Image ALT analysis
* Page-speed analysis
* Core Web Vitals integration
* Duplicate-content detection
* Structured-data validation

## Factual Verification

* Product database integration
* Nutrition database integration
* Government/regulatory source verification
* Cross-page entity consistency
* Numerical consistency checking
* Claim-to-source mapping
* Evidence confidence scoring

## AI Architecture

* More specialized agents
* Human approval checkpoints
* Agent memory
* Evidence retrieval
* Source citations
* Confidence scoring
* Parallel research
* Better error handling
* Persistent audit history

---

# 🧩 Technology Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Application backend       |
| Streamlit  | Web interface             |
| AutoGen    | Multi-agent orchestration |
| OpenAI     | LLM-powered agents        |
| SerpApi    | Search/SEO research       |
| Git        | Version control           |
| GitHub     | Source-code repository    |

---

# 🎯 Project Goal

The goal of this project is to build an AI-powered SEO intelligence platform that goes beyond simple article generation.

The system combines:

```text
SEO Research
     +
Content Generation
     +
SEO Optimization
     +
Content Review
     +
Website Auditing
     +
Potential Fact/Consistency Detection
```

into a single application.

The longer-term objective is to provide a workflow where AI can research, create, audit, and improve web content while providing enough evidence and context for humans to review important decisions.

---

# 📄 License

Add your preferred license here.

For example:

```text
MIT License
```

If a license has not yet been selected, this section should be updated before publishing the project for external use.

---

# 👤 Author

**Vivek Vinu**

GitHub:

https://github.com/Vivekvinu13

Project:

https://github.com/Vivekvinu13/AI-SEO-Multi-Agent---Autogen

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
SERPAPI_GEO = os.getenv("SERPAPI_GEO", "IN")
SERPAPI_LOCATION = os.getenv("SERPAPI_LOCATION", "India")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env")

if not SERPAPI_KEY:
    raise RuntimeError("SERPAPI_KEY is missing. Add it to .env")

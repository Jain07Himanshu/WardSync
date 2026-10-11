# AI Provider Configuration & Switching Guide

The engine is engineered with a **provider-agnostic architecture** enabling switching between model providers without changing business logic or data pipelines.

---

## 1. Environment Variables Overview

Edit your local `.env` file to configure the active provider:

| Variable | Allowed Values | Description |
|---|---|---|
| `AI_PROVIDER` | `openai`, `gemini`, `anthropic`, `mock` | Active provider implementation |
| `AI_MODEL` | Custom model ID or empty | Override default model ID |
| `OPENAI_API_KEY` | String (`sk-...`) | OpenAI API secret key |
| `GEMINI_API_KEY` | String | Google Gemini API secret key |
| `ANTHROPIC_API_KEY` | String | Anthropic Claude API secret key |
| `REQUEST_TIMEOUT_SECONDS` | Integer (default: 30) | HTTP request timeout |
| `MAX_RETRIES` | Integer (default: 3) | Maximum retry attempts on 429/502 |
| `BACKOFF_FACTOR` | Float (default: 1.5) | Exponential backoff multiplier |

---

## 2. Supported Providers

### A. OpenAI
- **Provider identifier**: `openai`
- **Default model**: `gpt-4o-mini` (or `gpt-4o`)
- **SDK**: Official `openai` Python SDK (v1.x)
- **Configuration in `.env`**:
  ```ini
  AI_PROVIDER=openai
  AI_MODEL=gpt-4o-mini
  OPENAI_API_KEY=your_openai_api_key_here
  ```
- **Error Handling**: Catches `AuthenticationError` (401), `RateLimitError` (429 with exponential backoff), and `APIConnectionError`.

### B. Google Gemini
- **Provider identifier**: `gemini`
- **Default model**: `gemini-2.5-flash`
- **SDK**: Official `google-genai` Python SDK
- **Configuration in `.env`**:
  ```ini
  AI_PROVIDER=gemini
  AI_MODEL=gemini-2.5-flash
  GEMINI_API_KEY=your_gemini_api_key_here
  ```
- **Features**: Native JSON schema response mode with strict types.

### C. Anthropic Claude
- **Provider identifier**: `anthropic`
- **Default model**: `claude-3-5-sonnet-20241022`
- **SDK**: Official `anthropic` Python SDK
- **Configuration in `.env`**:
  ```ini
  AI_PROVIDER=anthropic
  AI_MODEL=claude-3-5-sonnet-20241022
  ANTHROPIC_API_KEY=your_anthropic_api_key_here
  ```
- **Features**: Explicit JSON schema prompting with strict markdown stripping.

### D. Deterministic Mock Mode (Offline Development & CI)
- **Provider identifier**: `mock`
- **Default model**: `mock-civic-analyzer-v1`
- **Configuration in `.env`**:
  ```ini
  AI_PROVIDER=mock
  ```
- **Guarantees**:
  - Requires **zero API keys** and zero external internet connectivity.
  - Fully deterministic across unit tests, CI pipelines, and demo setups.
  - Generates realistic, schema-validated Mumbai civic observations across categories (roads, drainage, water supply, waste, streetlights).
  - Explicitly labeled with `ai_provider: "mock"` and `mock_flag: true`.

---

## 3. Strict Credential Verification

If an API key is missing or blank when that provider is requested:
1. The engine **never fabricates a successful response**.
2. It raises a `ConfigurationError` explaining which key is missing.
3. The API returns HTTP `503 Service Unavailable` with guidance:
   ```json
   {
     "error": "ConfigurationError",
     "message": "AI Provider is set to 'gemini', but GEMINI_API_KEY is not configured.",
     "hint": "Set GEMINI_API_KEY in .env or switch to AI_PROVIDER=mock for offline development."
   }
   ```

# Troubleshooting & Known Limitations

## 1. Troubleshooting Guide

### Issue: `ConfigurationError: OPENAI_API_KEY is not configured` (or 503 error)
- **Cause**: The active provider is set to `openai` (or `gemini`/`anthropic`), but no valid API key was found in environment variables or `.env`.
- **Solution**:
  1. Add your key to `.env`: `OPENAI_API_KEY=sk-...`
  2. Or switch to offline mock mode for testing without charges:
     ```ini
     AI_PROVIDER=mock
     ```

### Issue: `ProviderError: OpenAI authentication failed: 401 Unauthorized`
- **Cause**: An invalid, expired, or non-OpenAI key was provided in `OPENAI_API_KEY`.
- **Solution**: Check that the key starts with `sk-` and has active credits on platform.openai.com, or switch to `AI_PROVIDER=mock`.

### Issue: `RateLimitError (429)` on external AI calls
- **Behavior**: The engine automatically executes up to 3 retries with exponential backoff (`BACKOFF_FACTOR = 1.5`).
- **Solution**: If quotas are exceeded on free tier accounts, increase `BACKOFF_FACTOR` in `.env` or throttle the ingestion queue.

### Issue: `413 Request Entity Too Large` on document upload
- **Cause**: File exceeds the configured limit (default: 10MB).
- **Solution**: Adjust `FILE_UPLOAD_MAX_BYTES` in `.env`.

---

## 2. Known Limitations & Architectural Boundaries

1. **Scanned Images without Text Layers in PDFs**:
   - `pypdf` extracts native text streams. Scanned image-only PDFs without an embedded OCR text layer will return a notice: `[PDF contains no extractable text layer or is scanned image only]`. Tesseract OCR or multimodal vision models can be plugged in for scanned documents.
2. **Paywalled and Anti-Bot News Sites**:
   - The engine strictly respects ethical scraping guidelines, HTTP terms, and rate limits. It does not bypass paywalls, captcha challenges, or login authentication.
3. **Location Resolution Granularity**:
   - The embedded resolver maps Mumbai Metropolitan Region landmarks, stations, corridors, and 24 BMC wards. Locations outside mapped regions fall back to normalized text names without fabricating coordinates.
4. **Human Review on Sensitive Actions**:
   - Actions involving public infrastructure, hazardous conditions, or official escalation are marked with `PENDING_REVIEW` and must be approved by an authorized user before field mobilization.

# Repository instructions

## Project overview

This is a small Flask application for testing GPT-6 Astra text, image analysis,
image generation, and image editing through the OpenAI Responses API.

- `app.py` contains the Flask server and API integration.
- `templates/index.html` contains the browser UI and client-side streaming logic.
- `generated_images/` contains generated output and must not be treated as source.
- `main.py` is an older command-line prototype; keep changes focused on `app.py`
  unless the task explicitly includes the CLI.

## Development

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

The local application runs at `http://localhost:5000`.

## Verification

For Python-only changes, run:

```powershell
python -m py_compile app.py
```

For UI or request-flow changes, also test image upload, analysis, generation,
editing, streamed status updates, error handling, and generated-image display.
Avoid paid API calls unless they are necessary for the requested verification.

## Security and privacy

- Never read, print, commit, or expose `.env` values or API keys.
- Keep `OPENAI_API_KEY` in environment variables or deployment secrets.
- Do not place secrets in browser JavaScript, HTML, logs, generated files, or errors.
- Preserve server-side API calls so credentials never reach the browser.
- Keep Flask debug mode disabled in public deployments.
- Validate uploaded file type and size before processing it.
- Treat user prompts and model output as untrusted content; do not inject them as
  raw HTML.

## Implementation guidance

- Preserve the newline-delimited JSON streaming contract between `/chat` and the
  browser unless both sides are updated together.
- Keep progress messages factual; do not claim to expose private chain-of-thought.
- Use stable prompt-cache keys only for requests that share reusable prefixes.
- Return useful user-facing errors without leaking credentials or internal details.
- Keep changes small and avoid adding frameworks or dependencies without a clear
  benefit to this compact application.

## Hugging Face deployment

Use a Docker Space for the Flask app, listen on port `7860`, and store
`OPENAI_API_KEY` as a Hugging Face Space secret. Before making the Space public,
add authentication or user-provided credentials, rate limiting, upload limits,
spending controls, and generated-image cleanup.

## Future product plan

Develop the project into a focused interior-design visualizer rather than a
general-purpose image-model chat interface. Its core value should be helping
users quickly visualize renovation choices using photographs of their rooms.
Specially, this product is intended for investors, new home purchasers, 

Prioritize these capabilities:

1. A before-and-after image comparison.
2. Masked editing so users can select the exact region to change.
3. Material and design-style presets.
4. Multiple generated alternatives for each request.
5. Renovation cost estimates and saved project history.
6. Support for multiple model and API providers.
7. Customer user input interface for data mining, gets context about the user such as
  city of the project, theme, goal, project, age, design style. The 

Keep future interface and architecture decisions aligned with this product
identity. Prefer features that improve realistic renovation visualization over
unrelated general chat functionality.

To build trustworthy applications, the architecture must include robust guardrails, such as rigorous input validation and sanitization, to protect against malicious attacks, and policy enforcement mechanisms to ensure compliance

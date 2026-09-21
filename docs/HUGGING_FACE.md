# Hugging Face Docker Space launch guide

This repository is configured as a Hugging Face Docker Space on port `7860`.
The Space runs the Flask application directly; Docker Compose, Redis, MinIO, and
Kubernetes are optional deployment targets and are not started by Hugging Face.

## 1. Create the Space

1. Create a new Space at <https://huggingface.co/new-space>.
2. Select **Docker** as the SDK.
3. Start with **Private** visibility while validating the deployment.
4. Upload or push the complete repository.

## 2. Configure secrets

In **Settings → Repository secrets**, add:

| Secret | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI analysis, moderation, and image generation |
| `APP_SECRET_KEY` | Signs browser sessions; use a long random value |
| `APP_PASSWORD` | Password for the private showcase |

Add `ANTHROPIC_API_KEY` only if Anthropic analysis is enabled. Vertex AI requires
Google workload credentials and is better configured after the first launch.

Never add API keys to repository Variables, README files, Docker build arguments,
or source code.

## 3. Configure variables

In **Settings → Variables**, add:

| Variable | Recommended value |
| --- | --- |
| `APP_USERNAME` | A non-default showcase username |
| `COOKIE_SECURE` | `true` |
| `TRUST_PROXY_HOPS` | `1` |
| `ALLOW_PUBLIC_ACCESS` | `false` |
| `DAILY_REQUEST_LIMIT` | `25` during the private pilot |
| `IMAGE_RETENTION_HOURS` | `6` for ephemeral showcase output |

Keep `ALLOW_PUBLIC_ACCESS=false` for invitation-only testing. Setting it to
`true` makes the app anonymous and allows visitors to spend the Space owner's API
credits. The current login is a shared showcase account, not yet a customer
identity system.

## 4. Validate before changing visibility

- Confirm the Space build finishes without errors.
- Open `/health/live` and verify `{"status":"ok"}`.
- Log in and test analysis, preview generation, high-quality generation, editing,
  streaming errors, and generated-image display.
- Confirm the API provider dashboard has project-level budgets and alerts.
- Confirm logs contain no prompts, uploaded image data, credentials, or internal
  exception details.
- Restart the Space and verify that losing generated images is acceptable.
- Add a license before offering the repository for reuse or duplication.

## 5. Publish intentionally

- **Private**: only collaborators can use the app and see its source.
- **Protected**: the app is public but its source remains private; this requires an
  eligible Hugging Face plan.
- **Public**: anyone can use the app, inspect the source, clone it, or duplicate the
  Space.

For a brand showcase, start private with invited testers. Move to public only
after adding individual accounts or a strict invitation/quota mechanism. A public
Space should not expose an unrestricted image-generation account funded by the
owner.

## Storage note

The container writes temporary images to `/tmp/generated_images`. They disappear
when the Space restarts. To persist them, configure `S3_BUCKET`, `S3_ENDPOINT_URL`,
`S3_REGION`, `S3_ACCESS_KEY_ID`, and `S3_SECRET_ACCESS_KEY` using a compatible
object-storage provider. Access and secret keys belong in Repository secrets.

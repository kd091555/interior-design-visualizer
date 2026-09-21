# Privacy notice

Last updated: September 9, 2026

This interior-design visualizer processes the room photo and instructions you submit
to create an analysis or renovation visualization.

## What is processed

- Your room photograph, written request, and generated result.
- Basic operational data needed for authentication, security, rate limiting, and
  troubleshooting. The application does not intentionally log image contents or API
  credentials.

Only upload a photo you own or have permission to use. Do not upload photographs of
people, private documents, visible addresses, access codes, financial information, or
other sensitive data.

## AI providers

Uploaded photos and instructions are sent to OpenAI for safety moderation and AI
processing. If the server operator enables another analysis provider, relevant inputs
may also be sent to that configured provider. Processing performed by an external AI
provider is governed by that provider's terms and data-retention policies; deleting a
file from this application does not delete copies a provider may be required or
permitted to retain.

## Storage and deletion

The application does not intentionally save the original uploaded room photograph as
a source file. It exists temporarily in the browser, request memory, and provider
request while the task is processed.

Generated images are stored on local disk or configured S3-compatible object storage
so they can be displayed. They are automatically deleted after the retention period
configured by the operator, which is 24 hours by default. Cached result links expire
separately and do not contain the original photograph.

This is an early public-beta notice and should be reviewed with qualified privacy
counsel before commercial launch, especially where local law requires additional
rights, consent, or contact information.

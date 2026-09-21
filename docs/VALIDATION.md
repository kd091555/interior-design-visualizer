# Portfolio validation

Reviewed September 21, 2026. This is a prototype, not a production certification.

## Automated checks

The local Python compilation check and 38 unittest cases pass. Provider responses
are mocked; no paid inference was used for this review. The suite covers:

- Login, CSRF, generated-image authentication, and safe HTTP errors.
- Invalid uploads, image format verification, privacy acknowledgement, mask
  normalization, and masks without alpha channels.
- Input/output moderation rejection and known prompt-policy patterns.
- Intent routing, configured model routing, image editing, and variant limits.
- Similarity rejection before saving, retention cleanup, result cache reuse,
  estimated budget reservations, and errors inside the NDJSON stream.
- Presence of browser controls for source selection, masking, plans, and estimates.

The browser checks inspect rendered HTML/JavaScript. They are not automated browser
interaction tests, and do not establish that upload gestures, canvas painting,
mobile layout, or incremental rendering work in every browser.

The current Pillow version emits deprecation warnings for `Image.getdata()` in
the similarity helper. Tests pass, but that helper will need updating before
adopting a Pillow version that removes the method.

## Not verified in this review

- Live provider availability, image quality, or exact preservation outside masks.
- Real Redis, S3/MinIO, Docker, Kubernetes, or Hugging Face deployments.
- A full security audit, penetration test, or exhaustive credential detection.
- A publishable before-and-after example: local evaluation images have not been
  cleared for redistribution and are excluded from Git.

## Reproducing a visual example

Use a room photo you own or have permission to publish, without people, addresses,
documents, or identifying details. Upload it, optionally paint a wall mask, and ask:

> Change only the selected wall finish to warm ivory plaster. Preserve the room
> layout, ceiling, windows, floor, lighting, and camera view.

Live generation incurs provider charges. Inspect the result for unintended changes;
publish the source and result together with the exact prompt, model identifier,
date, attribution, and any observed defects. Label the result as an AI concept.
Do not present a hand-edited illustration or mocked test image as live model output.

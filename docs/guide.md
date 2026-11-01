---
url: /site/guide.md
description: Getting started with the public Civitai site API.
---

> Documentation index: https://developer.civitai.com/llms.txt — every page on this site has a markdown version at its URL + `.md`.

# Site API Guide

This section covers everything you need to start building against the Civitai
site API: generating a token, making your first request, paginating results,
handling errors, and working with AIR identifiers. It is also where the
**`civitai` CLI** is documented.

## The REST API

* [Getting started](https://developer.civitai.com/site/guide/getting-started.md) — create a token and make your first call.
* [Authentication](https://developer.civitai.com/site/guide/authentication.md) — how bearer tokens work and when they're required.
* [Pagination](https://developer.civitai.com/site/guide/pagination.md) — `page` vs. `cursor` and the 1000-offset cap.
* [Errors](https://developer.civitai.com/site/guide/errors.md) — response shape and HTTP status codes.
* [AIR identifiers](https://developer.civitai.com/site/guide/air.md) — the canonical URN format for Civitai resources.

For a per-endpoint breakdown (parameters, response fields, examples), see the
[Reference](https://developer.civitai.com/site/reference.md).

## The `civitai` CLI

The same binary reads these endpoints, downloads model files, and runs
generations on your own account.

* [CLI](https://developer.civitai.com/site/guide/cli.md) — install it, then the read and download commands.
* [CLI credentials and scopes](https://developer.civitai.com/site/guide/cli-auth.md) — OAuth vs a personal API key, and
  why a default browser login cannot spend Buzz.
* [Generating images from the CLI](https://developer.civitai.com/site/guide/cli-generate.md) — **spends real Buzz**. The
  money contract, `--dry-run`, `--max-cost`, waiting and downloading.
* [Choosing a model](https://developer.civitai.com/site/guide/cli-generate-models.md) — `--checkpoint` vs `--ecosystem`,
  silent model substitution, and image-to-image.
* [Raw generation graphs](https://developer.civitai.com/site/guide/cli-generation-graphs.md) — `--print-input` /
  `--input`, and the only route to a seed.
* [Tracking and cancelling generations](https://developer.civitai.com/site/guide/cli-workflows.md) — finding a job,
  reading what failed, and what cancelling does to a charge.
* [Scripting the CLI with `--json`](https://developer.civitai.com/site/guide/cli-json.md) — the output guarantees beyond
  the read endpoints.
* [CLI terminal output](https://developer.civitai.com/site/guide/cli-output.md) — the colour precedence, and what the
  human renderers guarantee about text a stranger uploaded.
* [CLI troubleshooting](https://developer.civitai.com/site/guide/cli-troubleshooting.md) — **look the error message up
  here.**

To author and ship a Civitai App with the same binary, see the
[Apps guide](https://developer.civitai.com/apps/guide.md).

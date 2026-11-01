---
url: /site/reference.md
description: Civitai site API reference — per-resource endpoint documentation.
---

> Documentation index: https://developer.civitai.com/llms.txt — every page on this site has a markdown version at its URL + `.md`.

# Reference

All endpoints below live under `https://civitai.com/api/v1/`.

| Resource | Endpoints |
|----------|-----------|
| [Models](https://developer.civitai.com/site/reference/models.md) | `GET /models`, `GET /models/{id}` |
| [Model versions](https://developer.civitai.com/site/reference/model-versions.md) | `GET /model-versions/{id}`, `GET /model-versions/by-hash/{hash}`, `POST /model-versions/by-hash`, `POST /model-versions/by-hash/ids`, `GET /model-versions/mini/{id}` |
| [Images](https://developer.civitai.com/site/reference/images.md) | `GET /images` |
| [Posts](https://developer.civitai.com/site/reference/posts.md) | `GET /posts/{id}` |
| [Articles](https://developer.civitai.com/site/reference/articles.md) | `GET /articles`, `GET /articles/{id}` |
| [Collections](https://developer.civitai.com/site/reference/collections.md) | `GET /collections`, `GET /collections/{id}` |
| [Creators](https://developer.civitai.com/site/reference/creators.md) | `GET /creators` |
| [Tags](https://developer.civitai.com/site/reference/tags.md) | `GET /tags` |
| [Users](https://developer.civitai.com/site/reference/users.md) | `GET /me`, `GET /users` |
| [Permissions](https://developer.civitai.com/site/reference/permissions.md) | `GET /permissions/check` |
| [Vault](https://developer.civitai.com/site/reference/vault.md) | `GET /vault/get`, `GET /vault/all`, `GET /vault/check-vault`, `POST /vault/toggle-version` |
| [Enums](https://developer.civitai.com/site/reference/enums.md) | `GET /enums` |

## Conventions used on this page

* **Base URL:** `https://civitai.com/api/v1`
* **Content type:** All responses are `application/json; charset=utf-8`.
* **Auth class** (shown on each endpoint):
  * *Public* — no token required.
  * *Mixed* — works without a token, but some parameters or response fields require one.
  * *Authenticated* — 401 without a valid token.
* **Caching:** Public endpoints set `Cache-Control: public, s-maxage=300, stale-while-revalidate=150`; authenticated calls skip the cache.
* **Region gating:** Responses may be filtered to SFW-only content regardless of the `nsfw` param when the request comes from a restricted region or Civitai's "green" domain. This is silent — you just see fewer results.

See the [Guide](https://developer.civitai.com/site/guide.md) for cross-cutting topics (authentication,
pagination, errors, AIR identifiers) and the [CLI](https://developer.civitai.com/site/guide/cli.md) for calling
these endpoints from the terminal.

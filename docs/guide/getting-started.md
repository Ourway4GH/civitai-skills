---
url: /site/guide/getting-started.md
description: Create an API token and make your first request to the Civitai site API.
---

> Documentation index: https://developer.civitai.com/llms.txt — every page on this site has a markdown version at its URL + `.md`.

# Getting started

## 1. Generate an API token

API tokens are managed from your Civitai account page:

1. Sign in to [civitai.com](https://civitai.com).
2. Open [Account settings](https://civitai.com/user/account).
3. Scroll to the **API Keys** section and click **Add API key**.
4. Give the key a name and copy the generated token — it's shown only once.

Store the token somewhere safe. Treat it like a password.

## 2. Make your first request

Most site API endpoints are public — you can call them without a token:

```bash
curl "https://civitai.com/api/v1/models?limit=1"
```

Try it right here:

Response (truncated):

```json
{
  "items": [
    {
      "id": 827184,
      "name": "WAI-illustrious-SDXL",
      "type": "Checkpoint",
      "creator": { "username": "WAI0731" },
      "modelVersions": [ /* ... */ ]
    }
  ],
  "metadata": {
    "nextCursor": "75363|932023|257749",
    "nextPage": "https://civitai.com/api/v1/models?limit=1&cursor=..."
  }
}
```

## 3. Make an authenticated request

Some endpoints require a token — for example `/me`, which identifies the caller:

```bash
export CIVITAI_TOKEN="your-token-here"

curl -H "Authorization: Bearer $CIVITAI_TOKEN" \
  "https://civitai.com/api/v1/me"
```

```json
{
  "id": 12345,
  "username": "you",
  "tier": "founder",
  "status": "active",
  "isMember": true,
  "subscriptions": ["monthly"]
}
```

Set a token via the **Token** button in the navbar, then try it here:

A few endpoints (`GET /models` with the `favorites` or `hidden` flag, for
example) also require authentication even though the base endpoint is public.
See [Authentication](https://developer.civitai.com/site/guide/authentication.md) for the full list.

## Next steps

* [Authentication](https://developer.civitai.com/site/guide/authentication.md) — token formats, query-param fallback, 401 behavior.
* [Pagination](https://developer.civitai.com/site/guide/pagination.md) — walking through large result sets.
* [AIR identifiers](https://developer.civitai.com/site/guide/air.md) — the URN format used throughout Civitai (and the Orchestration API).
* [Reference](https://developer.civitai.com/site/reference.md) — parameters and response fields for every endpoint.

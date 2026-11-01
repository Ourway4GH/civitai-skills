---
name: civitai-site-api
description: Civitai Site REST API 与 AIR (AI Resource Identifier) 资源检索与操作全景技能。涵盖 Models、Model Versions、Images、Posts、Vault、游标/页码分页机制以及标准错误诊断。
agent_created: true
---

# Civitai Site REST API 与资源检索技能 (civitai-site-api)

本技能提供 Civitai 平台官方公开 REST API (`https://civitai.com/api/v1`) 的标准操作范式。涵盖全量资源的检索过滤、以 Hash 反查模型版本、AIR URN 解析，以及 Vault 私有收藏库管理。

---

## 一、API 认证与基础请求规范

- **Base URL**: `https://civitai.com/api/v1`
- **认证机制**: 在请求 Header 携带 Bearer Token 或通过 Query 参数传入：
  - Header: `Authorization: Bearer <API_KEY>`
  - Query: `?token=<API_KEY>`（仅在只读或下载端点使用，优先推荐 Header）
- **频率限制 (Rate Limits)**:
  - 匿名调用：极低阈值，易触发 HTTP 429。
  - 认证用户：常规只读请求具备宽裕限额；高频轮询建议维持在 $\ge 1	ext{s}$ 间隔。

---

## 二、AIR (AI Resource Identifier) URN 规范

Civitai 定义了全局统一的 AI 资源唯一定位格式（AIR URN），在模型检索、工作流调度与跨端通信中作为通用强类型标识：

```text
urn:air:{ecosystem}:{type}:{source}:{sourceId}@{versionId}
```

### 字段解析与示例：
| 字段 | 说明 | 常见取值 |
| :--- | :--- | :--- |
| `ecosystem` | 基础模型生态 | `sd1`, `sd2`, `sdxl`, `flux1`, `flux2`, `anima`, `pony` |
| `type` | 资产类型 | `checkpoint`, `lora`, `textualinversion`, `controlnet`, `vae` |
| `source` | 托管平台/来源 | `civitai` (官方), `local` |
| `sourceId` | 模型主 ID (Model ID) | 如 `2458426` (Anima) |
| `versionId` | 模型具体版本 ID | 标识具体 safetensors 文件版本的 ID |

- **完整 URN 示例**：
  `urn:air:anima:checkpoint:civitai:2458426@2763293`
- **简写形式**（常用于 CLI 与快速索引）：
  `civitai:2458426` 或 `civitai:2458426@2763293`

---

## 三、核心端点调用范例与参数规则

### 1. 模型搜索与过滤 (`GET /models`)
支持按生态、类别、创作者及热度排序搜索全网公开模型：
```bash
curl -s -H "Authorization: Bearer $CIVITAI_API_KEY"   "https://civitai.com/api/v1/models?types=LORA&baseModels=SDXL%201.0&sort=Most%20Downloaded&limit=10"
```
- **核心查询参数**：
  - `limit`: 默认 20，最大 100；
  - `page`: 分页页码；
  - `query`: 关键词检索；
  - `types`: `Checkpoint`, `TextualInversion`, `LORA`, `DoRA`, `Controlnet`, `Upscaler`, `VAE`；
  - `sort`: `Highest Rated`, `Most Downloaded`, `Newest`;
  - `nsfw`: 是否包含成人内容（`None`, `Soft`, `Mature`, `X`）。

### 2. 通过文件 Hash 反查模型版本 (`GET /model-versions/by-hash/{hash}`)
在本地拥有 safetensors 文件时，计算其 SHA256 或 AutoV2/AutoV3 哈希，精准反查其在 Civitai 上的模型元数据与推荐提示词：
```bash
curl -s "https://civitai.com/api/v1/model-versions/by-hash/E32D497D7D"
```
- 支持 Hash 算法：`AutoV1`, `AutoV2`, `SHA256`, `CRC32`, `BLAKE3`。

### 3. 获取精选图片与生成元数据 (`GET /images`)
获取社区高质量出图记录，包含完整的 Generation Prompts、Seed、Sampler 与 LoRA 权重：
```bash
curl -s "https://civitai.com/api/v1/images?modelId=2458426&sort=Most%20Reactions&limit=5"
```
- 响应中的 `meta` 字段包含了生成该图所使用的全部提示词结构与参数，可用于复现或反推提示词组合。

### 4. Vault (私人保险箱) 管理 (`/vault`)
- `GET /vault`: 列出个人保险箱内已收藏的模型版本与存储容量占用；
- `POST /vault/toggle-version`: 将指定 `modelVersionId` 加入或移出 Vault。

---

## 四、分页与错误处理规范

### 1. 两种分页机制
- **页码分页 (Page-based)**：响应中包含 `metadata.currentPage` 与 `metadata.totalPages`，递增 `page` 即可遍历。
- **游标分页 (Cursor-based)**：多用于 `images` 等高频写入流。响应中包含 `metadata.nextCursor`，下一页请求附带 `?cursor=<nextCursor>`。当 `nextCursor` 为 null 时表示已到达末尾。

### 2. HTTP 状态码映射
- `200 OK`: 请求成功；
- `400 Bad Request`: 参数不合法（如未对特殊字符进行 URL 编码）；
- `401 Unauthorized`: 未提供 API Token 或 Token 已过期失效；
- `403 Forbidden`: 访问了未授权的模型、受限内容或被禁止的 NSFW 分级；
- `404 Not Found`: 资源 ID 不存在；
- `429 Too Many Requests`: 触发请求频率限制，必须退避（Exponential Backoff）。

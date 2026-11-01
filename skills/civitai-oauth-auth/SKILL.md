---
name: civitai-oauth-auth
description: Civitai OAuth 2.0 + PKCE 认证机制与安全资金管理技能。涵盖第三方应用授权时序、Scopes 权限掩码、Buzz 额度限制（Buzz Spend Limits）与退款机制。
agent_created: true
---

# Civitai OAuth 2.0 PKCE 认证与资金安全技能 (civitai-oauth-auth)

本技能提炼自 Civitai 官方 OAuth 体系文档，规范第三方客户端、桌面端应用及 AI Agent 如何安全地代表用户获取授权，执行模型下载、元数据读写及受控的 Buzz（平台算力代币）消费。

---

## 一、授权架构与 PKCE 时序

Civitai OAuth 2.0 强制要求使用 **Authorization Code Grant + PKCE (Proof Key for Code Exchange)**，杜绝任何 Client Secret 泄露风险：

```
[ 客户端 / Agent ]              [ 浏览器 / 用户 ]              [ Civitai OAuth Server ]
       │                                │                                │
       │ 1. 生成 code_verifier          │                                │
       │    计算 code_challenge (S256)  │                                │
       │                                │                                │
       │ 2. 引导用户访问授权 URL ───────┼───────────────────────────────>│
       │    /oauth/authorize?           │                                │
       │    client_id=...&              │                                │
       │    code_challenge=...&         │                                │
       │    scope=...                   │                                │
       │                                │ 3. 用户审核 Scope 并在 Web 授权│
       │                                │                                │
       │ 4. 接收重定向携带的 code <──────┴────────────────────────────────┤
       │                                                                 │
       │ 5. POST /oauth/token (code + code_verifier) ───────────────────>│
       │                                                                 │
       │ 6. 返回 access_token, refresh_token, expires_in <───────────────┤
```

---

## 二、OAuth 端点一览

| 端点用途 | 路径 | 方法 | 说明 |
| :--- | :--- | :--- | :--- |
| **授权入口** | `https://civitai.com/oauth/authorize` | GET | 唤起用户 Web 授权面板 |
| **令牌交换与刷新** | `https://civitai.com/api/v1/oauth/token` | POST | 兑换或续期 access_token |
| **用户画像查询** | `https://civitai.com/api/v1/oauth/userinfo` | GET | 获取当前授权用户的基本资料 |
| **撤销授权** | `https://civitai.com/api/v1/oauth/revoke` | POST | 吊销已有令牌 |

---

## 三、Scopes 权限掩码与最小权限原则

Civitai 内部采用 64 位无符号整型（uint64）位掩码管理权限，在授权面板中呈现为清晰的功能预设：

### 预设角色划分（Presets）：
1. **Read Profile (`profile`)**: 读取用户名、头像、粉丝数等公开资料；
2. **Read Content (`content:read`)**: 读取用户的私有收藏、Vault 内容、隐藏帖子；
3. **Write Content (`content:write`)**: 代表用户发布帖子、上传图片模型；
4. **Generate / Spend Buzz (`generate`)**: 授权触发云端出图与算力任务，**直接涉及账户代币扣减**。

---

## 四、Buzz 资金安全与额度管理（Buzz Spend Limits）

当第三方应用申请了 `generate` 权限时，Civitai 提供严格的多层资金安全屏障：

1. **用户自定单日/单次限额**：
   - 用户在 OAuth 授权界面可明确指定该应用允许消费的最大 Buzz 上限（例如每天 500 Buzz）。
   - 一旦超出限额，生成请求将直接返回 `402 Payment Required` 或特定的限额拒绝代码。
2. **幂等性保障 (Idempotency Key)**：
   - 任何涉及资金扣除的生图请求，必须在请求头或 Payload 附带唯一 UUID 幂等键，防止因网络抖动造成重复计费。
3. **失败自动退款**：
   - 若 Orchestration 平台由于节点故障、模型加载失败或上游报错中断任务，扣除的 Buzz 将在毫秒级内自动回滚至用户余额。

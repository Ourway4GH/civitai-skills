---
name: civitai-mcp-integration
description: Civitai 官方 Model Context Protocol (MCP) 架构与工具协同技能。指导 Agent 如何连接远程 Civitai MCP 服务，调度模型检索、参数读取与平台生成工具。
agent_created: true
---

# Civitai MCP 架构与工具编排技能 (civitai-mcp-integration)

本技能提炼自 Civitai 官方 MCP (Model Context Protocol) 规范，阐明如何将 AI Agent（DSH、Claude Desktop、Cursor 等）接入 Civitai 远程平台 MCP 服务，将数十万开源模型与云端生成管线转换为 LLM 可理解的标准化 Tools。

---

## 一、MCP 服务连接与配置

Civitai 官方提供了两种形态的 MCP 接入方式：

### 1. Stdio 模式（本地 CLI / 代理包）
通过全局安装的 CLI 启动 stdio 通信通道：
```json
{
  "mcpServers": {
    "civitai": {
      "command": "civitai",
      "args": ["mcp"],
      "env": {
        "CIVITAI_API_KEY": "YOUR_CIVITAI_API_KEY"
      }
    }
  }
}
```

### 2. 远程 SSE / HTTP 模式
直接连接 Civitai 托管的生产环境 MCP 端点：
```json
{
  "mcpServers": {
    "civitai-platform": {
      "url": "https://developer.civitai.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_CIVITAI_API_KEY"
      }
    }
  }
}
```

---

## 二、Civitai 核心 MCP Tools 矩阵

Civitai MCP Server 暴露的工具划分为 4 大核心领域：

### 1. 资源发现 (Discovery Tools)
- `search_models(query, type, base_model, limit)`: 模糊或精确搜索平台上的 Checkpoint / LoRA / VAE；
- `get_model_details(model_id)`: 获取指定模型的完整版本列表、触发词、推荐设置及使用协议；
- `get_model_version(version_id)`: 查询特定权重版本的 safetensors 下载地址与哈希验证值；
- `resolve_air(air_urn)`: 将标准的 `urn:air:...` 字符串直接解析为可用的元数据实体。

### 2. 生成意图与参数提取 (Generation Tools)
- `get_generation_parameters(image_id)`: 从一张展示图中精准抽取 Prompt、Negative Prompt、Seed、CFG、Sampler、Steps；
- `estimate_cost(params)`: 评估使用特定云端模型生成所需消耗的 Buzz 费用；
- `submit_generation_job(workflow)`: 向 Orchestrator 提交生图或生视频任务。

### 3. 用户状态与资产 (User & Asset Tools)
- `get_current_user()`: 检查当前登录用户的账户昵称与权限；
- `get_buzz_balance()`: 实时读取账户可用的 Buzz 余额；
- `list_vault_items()`: 浏览保存在私人 Vault 里的个人精选模型版本。

### 4. 平台反馈 (Feedback Tools)
- `send_platform_feedback(category, message)`: 遇到工具故障或模型异常时，向 Civitai 平台直报 Issue。

---

## 三、Agent 调度最佳实践

1. **先搜后用原则**：
   - 避免向用户盲目索要模型 ID。Agent 应当先调用 `search_models` 或 `resolve_air` 拿到确切的 `version_id` 和训练触发词（Trained Words）。
2. **参数校验与提示词适配**：
   - 查询到模型的触发词（如 Anima 的 `@artist` 规范或特定角色 Trigger words）后，自动重构提示词，再传递给后续生成环节。
3. **Buzz 扣费预检**：
   - 在执行可能产生计费的操作前，必须通过 `estimate_cost` 与 `get_buzz_balance` 确保账户余额充足并符合用户预期。

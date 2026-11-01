# Civitai Developer Ecosystem & Agent Skills
> Complete documentation archive, REST API references, OAuth 2.0 PKCE specs, MCP server guides, and structured AI Agent skills for Civitai.

本仓库是针对 [Civitai 开发者平台](https://developer.civitai.com/)（Site API / OAuth / Reference / MCP）构建的**离线原生文档知识库与高结构化 AI Agent 技能包**集合。

---

## 目录结构

```text
.
├── docs/                           # 官方原生 Markdown 完整归档 (37 篇无损文档)
│   ├── guide/                      # 开发入门、CLI 工具链、出图与错误诊断
│   ├── oauth/                      # OAuth 2.0 PKCE 认证时序、端点与 Buzz 限制
│   ├── reference/                  # 官方 REST API 资源手册 (Models, Images, Posts...)
│   └── mcp/                        # Model Context Protocol 服务与 Tools 规范
├── skills/                         # 提炼出的 AI Agent 标准技能包
│   ├── civitai-site-api/           # 1. 核心 REST API 检索与 AIR URN 规范
│   ├── civitai-oauth-auth/         # 2. OAuth 2.0 PKCE 认证与 Buzz 资金管理
│   ├── civitai-mcp-integration/    # 3. Civitai 平台 MCP 服务与工具编排
│   └── civitai-cli-workflows/      # 4. Civitai Go CLI 命令行与原生生成工作流
└── scripts/
    └── fetch_civitai_docs.py       # 文档自动化抓取与结构同步脚本
```

---

## 四大技能包一览

| 技能名称 | 适用领域 | 核心能力与关键操作 |
| :--- | :--- | :--- |
| **`civitai-site-api`** | REST API & 资源检索 | 模型/版本/图片/帖子元数据检索、文件 Hash 逆向反查、AIR URN (`urn:air:...`) 解析、Vault 个人保险箱管理 |
| **`civitai-oauth-auth`** | 身份鉴权与安全 | 基于 PKCE 的授权时序、Scopes 权限掩码控制、Buzz 消费配额与安全扣减、失败自动回滚机制 |
| **`civitai-mcp-integration`** | MCP 协议与 Agent 协同 | 官方 Stdio/SSE 接入配置、Discovery/Generation/Asset Tools 编排、Agent 提示词先验补全 |
| **`civitai-cli-workflows`** | 终端工具与云端生成 | Go 官方 CLI 环境配置、`civitai generate` 管道调用、UNIX `--json` 纯数据交互、故障错误码诊断 |

---

## 官方原始文档同步来源

所有 `docs/` 内容直接从 `https://developer.civitai.com/site/` 原生提取，并通过 `Accept: text/markdown` 保留了完整的 Markdown 原始排版与技术细节。

---

## License
MIT License.

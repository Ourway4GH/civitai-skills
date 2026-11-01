---
name: civitai-cli-workflows
description: Civitai 官方 Go CLI 工具链与自动化生成工作流技能。涵盖终端检索、下载、civitai generate 管道编排、纯 JSON 脚本自动化及常见故障诊断。
agent_created: true
---

# Civitai CLI 命令行与原生工作流技能 (civitai-cli-workflows)

本技能系统总结 Civitai 官方编译型 Go CLI (`civitai`) 的工程实践，为运维与开发提供终端快速检索模型、鉴权下载、脚本批量执行与无界面（Headless）云端生成能力。

---

## 一、CLI 快速安装与身份验证

### 1. 登录与 Token 配置
```bash
# 方式 A：交互式设备码登录（在浏览器中点确认）
civitai auth login

# 方式 B：通过环境变量或参数传入 API 密钥（推荐用于自动化脚本）
export CIVITAI_API_KEY="your_api_token_here"
civitai whoami
```

### 2. 身份验证状态检查
`civitai whoami` 会输出当前绑定的用户名、生效的 Scopes 以及账户当前 Buzz 余额。

---

## 二、核心命令行操作

### 1. 模型搜索与版本解析
```bash
# 检索 SDXL 风格 LoRA
civitai models search "Ghibli style" --type LORA --ecosystem sdxl

# 查看模型详情与所有版本 ID
civitai models get 2458426
```

### 2. 安全鉴权下载 (Download)
直接解析模型并拉取最新或指定版本的权重文件：
```bash
# 下载指定版本至当前目录
civitai download 2458426 --version 2763293 --dir ./models/diffusion_models

# 校验并断点续传
civitai download 2458426 -c
```

### 3. 云端直接生成 (`civitai generate`)
支持纯终端驱动 Civitai 云端算力进行高质量出图：
```bash
# 预估成本（Dry run，不实际扣除 Buzz）
civitai generate --checkpoint "urn:air:sdxl:checkpoint:civitai:101055"   --prompt "masterpiece, 1girl, scenic landscape"   --dry-run

# 执行生成并自动等待下载产物
civitai generate --checkpoint "civitai:101055"   --prompt "masterpiece, highly detailed portrait"   --steps 25   --cfg 7.0   --wait   --out ./output.png
```

---

## 三、脚本化集成规范 (`--json`)

CLI 设计原生支持 UNIX 管道与自动化代理调度：
- 当传入 `--json` 标志时，CLI 保证 **stdout 严格输出合法 JSON**，所有人类可读的提示和日志重定向至 **stderr**：
  ```bash
  # 提取模型版本中所有 safetensors 文件的直链
  civitai models get 2458426 --json | jq '.modelVersions[0].files[] | select(.name | endswith(".safetensors")) | .downloadUrl'
  ```

---

## 四、常见报错与诊断代码 (Troubleshooting)

| 错误信息 / 场景 | 原因排查 | 解决方案 |
| :--- | :--- | :--- |
| `ERR_NO_AUTH` | 未找到有效 API 凭证 | 检查环境变量 `CIVITAI_API_KEY` 或重新执行 `civitai auth login` |
| `ERR_MODEL_SUBSTITUTED` | 请求的 Checkpoint 离线，服务端尝试自动替换 | 检查 `--ecosystem` 兼容性，避免服务端静默降级 |
| `ERR_INSUFFICIENT_BUZZ` | 账户可用 Buzz 不足 | 充值 Buzz 或降低 Steps / Resolution 规模 |
| `ERR_WORKFLOW_TIMEOUT` | 队列拥堵导致超时 | 使用 `civitai workflows list` 查询长任务，增加超时等待阈值 |

# WiseStudio 部署分析报告

## 1. 部署模型

**引入自定义部署模型：混合模式（Hybrid）**

- **本地化部署**：所有核心服务（PostgreSQL、Redis、Forgejo、Chatwoot、Unoserver、OpenClaw Gateway）运行在用户本地 macOS/Windows 主机上，使用 Docker Compose 管理
- **Cloudflare 隧道**：通过 `cloudflared` 提供临时公网访问能力（用于 Telegram Webhook 等渠道）
- **数据持久化**：`~/WiseStudio/setup/data` 作为挂载卷.persist数据库和配置

**不是 SaaS**：用户完全拥有基础设施控制权，数据不出本地。

---

## 2. 系统要求

### 主机平台

| 平台 | 最低要求 | 测试版本 |
|------|----------|----------|
| macOS | Apple Silicon 或 Intel | Ventura+ (ARM64/AMD64) |
| Windows | Windows 10/11 | PowerShell 7+ |

### 核心依赖

| 工具 | 版本要求 | 用途 |
|------|----------|------|
| Docker | 24+ | 容器化运行所有服务 |
| Docker Compose | v2+ | 编排多容器应用 |
| `gh` CLI | 2.x | 安装脚本认证与 Release 下载 |

### 本地开发工具（推荐安装）

| 工具 | 用途 |
|------|------|
| `obsidian` CLI | `memory-server` 搜索后端 |
| Browser (Chrome/Firefox) | 访问 Web UI 与 Webhook 重定向 |

### 默认安装目录

- macOS: `~/WiseStudio/setup`
- Windows: `~/WiseStudio/setup`

---

## 3. 架构概览

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              Docker Compose (wiselaw-net)                      │
├────────────────────────────────────────────────────────────────────────────────┤
│                                         │                                      │
│  ┌─────────────┐  ┌───────────┐  ┌────┴─────┐  ┌───────────┐  ┌─────────────┐ │
│  │  PostgreSQL │  │   Redis   │  │  Forgejo   │  │  Chatwoot │  │  OpenClaw   │ │
│  │   (pg17)    │  │  (alpine) │  │  (v10)     │  │  (latest) │  │  (gateway)  │ │
│  │    :13100   │  │   :13101  │  │   :13200   │  │   :13300  │  │   :18789    │ │
│  └─────────────┘  └───────────┘  └──────┬─────┘  └─────┬─────┘  └─────────────┘ │
│                                          │              │                        │
│                     ┌────────────────────┼──────────────┼─────────────┐         │
│                     │                    │              │             │         │
│              ┌──────┴───────┐   ┌────────┴──────┐  ┌───┴──────┐    │           │
│              │  forgejo-init│   │ forgejo-mcp   │  │unoserver │    │           │
│              │  (one-shot)  │   │   :13202      │  │  :19031   │    │           │
│              └──────────────┘   └───────────────┘  └──────────┘    │           │
│                                                                     │           │
│              ┌──────────────────────────────────────────────────────┘           │
│              │               Cloudflare Tunnel                                 │
│              │                cloudflared                                       │
│              │              (临时公网访问)                                       │
│              └──────────────────────────────────────────────────────────────────┘
│
├────────────────────────────────────────────────────────────────────────────────┤
│                              Host App Layer                                    │
├────────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  Obsidian     │  │  Web UI         │  │  Memory      │  │  Desktop API    │ │
│  │  Desktop App  │  │  localhost:19010│  │  Server      │  │  localhost:19020│ │
│  └───────────────┘  └─────────────────┘  └───────┬──────┘  └─────────────────┘ │
│                                                  │                              │
│                                       ┌──────────┴──────────┐                   │
│                                       │  Memory-Server      │                   │
│                                       │  (外部客户端搜索)    │                   │
│                                       └─────────────────────┘                   │
└────────────────────────────────────────────────────────────────────────────────┘
```

### 组件分类

#### 1. 数据服务 (131xx)
- **PostgreSQL (pgvector)**：向量数据库，用于语义搜索
- **Redis**：缓存与会话存储（仅 localhost:13101）

#### 2. 代码与 CI/CD (132xx)
- **Forgejo (Git + Actions)**：自托管 Git + CI/CD Runner，作为 "cognitive infra"
- **Forgejo MCP**：提供 REST API 到 Forgejo 的映射

#### 3. 客服与通信 (133xx)
- **Chatwoot**：自托管客服平台，支持多渠道（Telegram/Slack/Facebook）

#### 4. 文档处理 (19031)
- **Unoserver**：pandoc + LibreOffice 集成服务，用于文档转换

#### 5. AI Sandbox (18789)
- **OpenClaw Gateway**：AI Agent 控制平面，支持 Claude Code/OpenCode

#### 6. 可观测性 (19040+)
- **Langfuse**（可选）：LLM Token 监控与观测

#### 7. 辅助工具
- **Cloudflare Tunnel**：临时公网暴露（用于 Webhook）
- **Tunnel Monitor**：监控 URL 变化并自动重配置 webhook

---

## 4. 依赖与集成

### Docker 依赖链（启动顺序）

```
postgres (healthy)
  ↓
forgejo (healthy)
  ↓
forgejo-init (one-shot)
  ├─→ forgejo-mcp
  └─→ chatwoot-init (建表 + default admin)
        ↓
      chatwoot + chatwoot-sidekiq
        ↓
      cloudflared (设置 Telegram webhook)
        ↓
      tunnel-monitor (监控 URL 再配置)
```

### 外部集成

| 集成点 | 配置方 | 说明 |
|--------|--------|------|
| Telegram Bot | `secrets/telegram-bot-token` | 自动设置 webhooks |
| SMTP | Chatwoot env | 邮件通知（QQ/Outlook 等） |
| npm registry | 镜像源切换 | cn/global 自动检测 |
| Docker Hub | `docker.1ms.run` | -cn 区域加速 |

---

## 5. 产品市场推断

### 目标用户画像

#### 1. 法律科技团队（核心）

**证据：**
- 项目名 `wiselaw` + `wisestudio`：明确执法场景品牌一致性
- 预置 **Chatwoot 客服系统**：用于律所/客户沟通
- **文档转换服务**：法律文书格式化、对比修订
- 使用 `pgvector`：法律案例向量检索需求
- 许可协议中强调 **本土化部署**：符合中国数据合规要求

#### 2. AI Agent 工程师

**证据：**
- 自主维护 **OpenClaw Gateway**（非第三方（如 Fly.io））
- 集成 **Forgejo Actions CI/CD**：可扩展工作流
- 沙箱镜像支持 `Claude Code` / `OpenCode` / `agent-browser`
- 子项目（`unoserver`）提供 MCP 协议接口

#### 3. 企业级自部署客户

**证据：**
- 代码仓库为 **Private**（限制访问）
- 无 SaaS 版本说明，强调本地 `data/` 持久化
- 支持国内镜像源（`REGION=cn`）

---

## 6. 核心技术特征

| 特征 | 实现方式 | 战略意义 |
|------|----------|----------|
| **自托管优先** | 全部服务 Docker Compose 本地运行 | 降低用户心理门槛（数据可控） |
| **可升级性** | `VERSION` 文件 + CalVer 规范 | 易于维护与版本回退 |
| **无障碍安装** | `gh` CLI 一键下载 Release + 自动平台检测 | 降低技术门槛 |
| **模块化拆分** | 多个独立 compose 文件（runner/langfuse） | 适配不同需求（太极端用户可跳过 Langfuse） |
| **跨平台支持** | `setup-mac.sh` + `setup-windows.ps1` | 本地化与扩展性 |
| **可观测性** | Langfuse / tunnel-monitor / healthcheck | 企业运维友好 |

---

## 7. 部署后使用场景

1. **法律智能助手**  
   - 用户通过 `localhost:19010` 访问 Web 前端  
   - 客服消息经 Telegram webhook → Chatwoot → 已接入 Agent  
   - 语义搜索后端使用 `memory-server` → `Obsidian Desktop` → PostgreSQL pgvector

2. **文书自动化**  
   - 模板生成：Markdown → HTML/PDF（Unoserver）  
   - 版本对比：生成修订版 DOCX（Unoserver compare API）

3. **CI/CD 智能审计**  
   - Forgejo Actions 触发 Agent 编排（OpenClaw Sandbox）  
   - 代码提交 → 自动 `opencode-ai`/`agent-browser` 执行测试/格式化

---

## 总结

**WiseStudio** 是一个以 **法律科技** 为核心的 **AI Agent 基础设施**，通过：

- 本地 Docker Compose 实现 **零信任自部署**
- Chatwoot + Telegram + Forgejo 构建 **法定代表沟通闭环**
- OpenClaw Sandbox + pgvector 提供 **AI 原生能力**

**市场定位**：服务希望将法律知识库与 AI Agent 深度集成，同时需要 **100% 数据主权** 的律所/法律科技团队。

# WiseLaw Studio (Wise-Studio) - Product Feature Analysis

## Product Overview

**WiseLaw Studio** is a modern legal tech platform designed as an AI-powered legal workspace that operates as a "digital employee" rather than a traditional tool or chatbot. The platform enables AI agents to work like real legal colleagues—operating computers, handling documents, managing communications, and completing legal tasks autonomously.

**Core Philosophy:** "Your first legal digital employee" — AI that is continuously online, proactively perceptive, autonomously decision-making, and supervisable.

The product is built as a **Turborepo monorepo** containing multiple applications:
- **Web App** (`apps/web`): Next.js web application (port 3000) - status dashboard
- **Desktop Client** (`apps/desktop`): Electron-based desktop application (port 3002) - main workspace
- **Admin Panel** (`apps/admin`): Management and analytics dashboard (port 3003)
- **Gateway** (`apps/gateway`): Communication channel integration service
- **Docs** (`apps/docs`): Documentation site (port 3001)
- **Landing Page** (`apps/landing-page`): Marketing site

---

## Core Features

### 1. AI-Powered Code Agent (OpenCode Integration)

The platform integrates **OpenCode AI** as its core execution engine, providing:
- **Code generation and execution** capabilities for legal tasks
- **Session-based task management** with persistent context
- **Human-in-the-Loop (HITL)** for critical decision points
- **Task decomposition and scheduling** with todo lists
- **Full audit trail** with execution tracking and logging

**Key Implementation:**
- OpenCode server runs natively on the host machine
- Type-safe IPC communication between Electron main process and renderer
- Session isolation per workspace with directory-based state management
- Support for both OAuth and API key authentication for AI providers

### 2. Multi-Channel Communication Hub

**Gateway Service** provides unified communication across multiple channels:
- **Telegram** - Bot-based messaging with webhook support
- **WhatsApp** - Baileys library integration with QR pairing
- **Email** - IMAP/SMTP with full MIME parsing
- **Lark/Feishu** - Enterprise collaboration platform
- **Slack** - Socket mode and webhook support

**Features:**
- Intelligent message routing based on sender/session
- Chatwoot integration for unified inbox management
- Per-sender session isolation for context preservation
- Configurable DM policies (open/allowlist/pairing)
- Media handling with size limits and format support

### 3. Workspace & Context Management

**Desktop Application** provides a sophisticated workspace system:
- **Multiple workspaces** with isolated contexts
- **Host path mapping** for local file system access
- **Output directories** for agent-generated content
- **Context paths** for additional reference materials
- **Real-time file watching** with automatic refresh
- **File preview panel** with support for multiple formats

**Workspace Features:**
- Git repository cloning and management
- Context mounting (files/directories) for agent awareness
- Session switching between different tasks/channels
- Collapsible panels for sessions, output, context, and skills

### 4. Skills & MCP (Model Context Protocol) System

**Skills Framework:**
- **User skills** - Custom skills defined by users
- **Market skills** - Pre-built skills from marketplace
- **WiseLaw skills** - Domain-specific legal skills
- Skills can be enabled/disabled per workspace
- Skills include workflow definitions and constraints

**MCP Integration:**
- **Local MCP servers** - Command-based tools
- **Remote MCP servers** - HTTP-based services
- Server enable/disable controls
- Timeout and environment configuration

### 5. AI Provider Abstraction

**AI Provider Factory** supports multiple LLM providers:
- **Anthropic** (Claude) - Direct API and OAuth
- **OpenAI** (GPT) - Direct API and OAuth
- **Google** (Gemini) - Direct API
- **xAI** (Grok) - Direct API
- **Mistral** - Direct API
- **OpenRouter** - Aggregated provider access
- **OpenAI-compatible providers:**
  - DeepSeek
  - Moonshot/Kimi
  - GLM (Zhipu)
  - MiniMax
  - Alibaba/Qwen (DashScope)
  - DeepInfra

**Authentication Strategy:**
- OAuth credentials → Routed through OpenCode SDK proxy
- API key credentials → Direct @ai-sdk/* package usage
- Provider caching with invalidation on config changes
- Custom baseURL support for proxy/relay configurations

### 6. Scheduling & Automation Engine

**Issue Schedules** for automated task execution:
- **Scheduled tasks** - One-off execution at specific time
- **Cron tasks** - Recurring execution with cron expressions
- **Retry logic** - Configurable retry on failure
- **Execution limits** - Max executions and end dates
- **Status tracking** - Success/failure/cancelled states

**Scheduler Features:**
- Integration with Forgejo issue tracking
- Automatic issue creation from schedules
- Execution count and last run tracking
- Enable/disable controls with reason tracking

### 7. Database & Persistence

**SQLite Database** with Drizzle ORM:
- **Workspaces** - Workspace configurations and mappings
- **Channel Messages** - Multi-channel message storage
- **Channel Accounts** - Communication account configs
- **Channel Sessions** - Per-sender session isolation
- **Issue Schedules** - Scheduled task definitions

**Data Models:**
- JSON-based flexible config storage
- Timestamp tracking for all entities
- Status enums for state management
- Unique constraints for data integrity

### 8. Admin & Analytics

**Admin Panel** provides:
- System status monitoring
- Usage analytics with Recharts visualizations
- User management with Better Auth
- S3 integration for file storage
- WebSocket support for real-time updates

---

## Technical Stack

### Frontend
- **Next.js 16.1.0** with App Router
- **React 19** with strict TypeScript
- **Tailwind CSS** with custom design system
- **Radix UI** primitives
- **Framer Motion** for animations
- **Lucide React** icons
- **next-intl** for internationalization
- **Sonner** for toast notifications
- **Zustand** for state management
- **TanStack Query** for data fetching

### Desktop
- **Electron** with Next.js renderer
- **better-sqlite3** for local database
- **electron-builder** for packaging
- **electron-updater** for auto-updates
- **electron-log** for logging
- **IPC** with type-safe wrappers

### Backend Services
- **OpenCode Server** - AI agent runtime
- **Gateway Service** - Communication channel hub
- **Memory Server** - Long-term memory and retrieval
- **Forgejo Client** - Git repository management
- **Chatwoot Client** - Unified inbox integration

### Build & Tooling
- **Bun** v1.3.2 package manager
- **Turborepo** for monorepo management
- **TypeScript** 5.9.2 (strict mode)
- **Vitest** for testing
- **Playwright** for E2E testing
- **Drizzle Kit** for database migrations
- **ESLint** with strict rules
- **Prettier** for formatting
- **Husky** for git hooks
- **Commitlint** for commit messages

### AI/ML Integration
- **Vercel AI SDK** (ai package)
- **@ai-sdk/* providers** - Anthropic, OpenAI, Google, xAI, Mistral
- **@openrouter/ai-sdk-provider**
- **ai-sdk-provider-opencode-sdk** - OpenCode proxy
- **Zod** for schema validation

---

## AI/LLM Capabilities

### 1. Multi-Provider Support

The platform supports **10+ AI providers** through a unified abstraction:
- Direct API integration via @ai-sdk/* packages
- OAuth proxy through OpenCode SDK
- OpenAI-compatible endpoint support
- Provider-specific configuration (baseURL, options)

### 2. Agent Configuration

**Agent Config Service** provides:
- **Per-agent model selection** - Different models for different agents
- **System prompt customization** - User and default system prompts
- **Agent modes** - Primary, subagent, or all-purpose
- **Skill enablement** - Per-agent skill activation
- **MCP server configuration** - Tool integration
- **Permission controls** - Action-level permissions

### 3. Task Execution

**AI-Powered Task Management:**
- Natural language to structured task conversion
- Automatic todo list generation with priorities
- Schedule inference (immediate/scheduled/cron)
- Issue title and description generation
- Language-aware output (matches input language)

### 4. Context Engineering

**Multi-Layer Context:**
- **AGENT.md** - Agent role and identity
- **SKILL.md** - Skill definitions and workflows
- **MCP** - Tool and protocol definitions
- **Memory** - Long-term knowledge retrieval
- **Session** - Conversation history and state
- **Workspace Context** - File system and project awareness

### 5. Human-in-the-Loop

**HITL Integration:**
- Critical decision pause points
- Human confirmation for risky actions
- Session handoff between AI and human
- Audit trail for all decisions

---

## Target Users/Use Cases

### Primary Users
- **Law Firms** - Small to medium-sized practices
- **Corporate Legal Departments** - In-house legal teams
- **Legal Service Providers** - Contract review, compliance services
- **Solo Practitioners** - Individual lawyers needing AI assistance

### Use Cases

#### 1. Legal Research
- Regulation and statute retrieval
- Case law analysis and precedent finding
- Legal opinion drafting
- Jurisdiction-specific research

#### 2. Contract Review
- Clause identification and extraction
- Risk flagging and annotation
- Modification suggestions
- Redline generation

#### 3. Due Diligence
- Information collection and aggregation
- Document organization and categorization
- Report generation
- Data extraction from multiple sources

#### 4. Document Drafting
- Contract and agreement creation
- Legal opinion writing
- Brief and motion drafting
- Template-based document generation

#### 5. Document Management
- Case file organization
- Version control and tracking
- Document classification
- Search and retrieval

#### 6. Daily Operations
- Email processing and triage
- Meeting note summarization
- Calendar and schedule management
- Client communication handling

#### 7. Multi-Modal Processing
- Speech-to-text transcription
- Image/text recognition (OCR)
- PDF/Word/PPT parsing and generation
- Format conversion

#### 8. Knowledge Management
- Knowledge base RAG queries
- Precedent retrieval
- Firm-specific guidance
- Citation and source tracking

#### 9. Compliance
- Regulatory compliance checking
- Risk assessment
- Rule matching and validation
- Audit preparation

#### 10. Cross-Session Memory
- Experience accumulation
- Pattern learning
- Knowledge persistence
- Continuous improvement

---

## Key Differentiators

### 1. True Digital Employee vs. Assistant

**Unlike traditional legal tech:**
- **Not a tool collection** - Integrated workspace
- **Not a chatbot** - Autonomous action capability
- **Not passive** - Proactive event-driven operation
- **Not cloud-only** - Local execution with data control

### 2. Code Agent Foundation

**Built on OpenCode:**
- Full code execution capabilities
- Real file system operations
- Actual application interaction
- Genuine task completion (not simulation)

### 3. Event-Driven Architecture

**Three Operation Modes:**
- **Passive Response** - Direct human instruction
- **Event-Driven** - Email/message/file change triggers
- **Scheduled Patrol** - Rule-based periodic checks

### 4. Local-First Design

**Data Sovereignty:**
- Sensitive legal data stays local
- Agent operates on real local files
- No cloud black box
- Full audit and compliance control

### 5. Continuous Operation

**24/7 Availability:**
- Always-on event monitoring
- Background task execution
- Asynchronous result delivery
- No "session timeout" limitations

### 6. Comprehensive Channel Integration

**Unified Communications:**
- 6+ communication channels supported
- Single configuration interface
- Per-sender session isolation
- Chatwoot integration for team collaboration

### 7. Extensible Skills System

**Modular Capabilities:**
- User-defined skills
- Marketplace skills
- Domain-specific (legal) skills
- MCP protocol for tool integration

### 8. Flexible AI Provider Support

**No Vendor Lock-in:**
- 10+ AI providers supported
- OAuth and API key options
- Provider switching without code changes
- Cost optimization through provider selection

### 9. Production-Ready Architecture

**Enterprise Features:**
- Monorepo with shared packages
- Type-safe IPC and APIs
- Comprehensive testing (unit + E2E)
- Auto-updates and versioning
- Multi-platform support (macOS, Windows, Linux)

### 10. AI-First Development Philosophy

**Design Principles:**
- Agent capability first, UI second
- Proactive over reactive
- Local over cloud
- Traceable, intervenable, auditable

---

## Competitive Positioning

| Competitor | Category | WiseLaw Studio Differentiation |
|------------|----------|-------------------------------|
| **Manus** | General Cloud Agent | Local execution + Legal domain specialization |
| **Claude Code / Cursor** | Developer Tools | Legal professional focus vs. developer focus |
| **Copilot for M365** | In-App Assistant | Independent digital employee vs. embedded helper |
| **Traditional RPA** | Rule Automation | LLM-driven semantic understanding vs. rigid scripts |

---

## Maturity Assessment

### Current State (v1.x)
- ✅ Core Code Agent functionality operational
- ✅ Multi-channel communication gateway
- ✅ Workspace and context management
- ✅ AI provider abstraction layer
- ✅ Basic scheduling and automation
- ✅ Skills and MCP framework
- ⚠️ UI/UX still evolving
- ⚠️ Documentation comprehensive but scattered

### Roadmap Indicators
- v2.0: Enhanced event perception layer
- v3.0: Autonomous decision-making capabilities
- Ongoing: Legal domain skill expansion

---

## Technical Quality Indicators

- **TypeScript strict mode** with `noUncheckedIndexedAccess`
- **Comprehensive testing** with Vitest and Playwright
- **Monorepo best practices** with Turborepo
- **Modern React patterns** (App Router, Server Components)
- **Type-safe IPC** between Electron processes
- **Database migrations** with Drizzle Kit
- **CI/CD automation** with GitHub Actions
- **AI workflow automation** with Claude Code and GitHub Copilot

---

*Analysis completed: 2026-03-15*
*Repository: wiselaw-ai/wise-studio*
*Analysis depth: Source code review + documentation analysis*

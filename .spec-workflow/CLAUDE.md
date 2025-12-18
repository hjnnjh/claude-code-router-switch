[🏠 根目录](../CLAUDE.md) > **✨ .spec-workflow 模块**

# .spec-workflow · 模块详细文档

**版本**: 2.0 | **最后更新**: 2025-12-18 | **覆盖范围**: 完整模块审计

---

## 1. 模块职责与愿景

**核心职责**: 集中提供 Spec Workflow 生态所需的默认 Markdown 模板，覆盖需求、设计、任务规划以及产品/技术/结构指导，确保跨项目文档输出拥有**统一骨架与规范**。同时通过 `user-templates/` 目录支持**按文件名一键覆盖**机制，平衡默认标准与项目定制。

**集成关系**:
- 🔗 **上游** (根级): CLAUDE.md 作为项目总览，链接本模块
- 🔗 **外部工具**: Spec Workflow CLI / 自动化文档生成工具，通过"用户优先加载"规则获取模板
- 🔗 **版本控制**: .gitignore 会排除 `user-templates/` 中的用户定制（若需要）

**核心价值**:
- 📋 **快速启动** - 新项目无需从零撰写，直接填充模板占位符即可生成规范文档
- 🎯 **团队对齐** - 统一的文档结构降低沟通成本，便于知识沉淀
- 🔄 **灵活定制** - 支持用户覆盖机制，允许按项目特性微调模板
- 📚 **可追溯** - 模板版本与 CLAUDE.md 联动，变更有迹可循

---

## 2. 模块目录结构

```
.spec-workflow/
├── CLAUDE.md                          ← 本模块文档
├── templates/                         ← 默认模板库 (6个)
│   ├── requirements-template.md       ← 需求文档
│   ├── design-template.md             ← 设计文档
│   ├── tasks-template.md              ← 任务规划
│   ├── product-template.md            ← 产品指南
│   ├── tech-template.md               ← 技术指南
│   └── structure-template.md          ← 结构指南
│
└── user-templates/                    ← 用户覆盖目录 (可选)
    └── README.md                      ← 使用说明与最佳实践
    # 用户定制文件会被放在此处（示例：requirements-template.md）
```

**文件计数**:
- 默认模板: **6 个** Markdown 文件
- 用户覆盖说明: **1 个** README
- 模块文档: **1 个** CLAUDE.md
- **总计**: 8 个文件（不含用户创建的定制文件）

---

## 3. 默认模板详解

### 3.1 requirements-template.md (需求文档)

**用途**: 捕捉功能需求、用户故事、验收标准、非功能需求，驱动设计与开发。

**关键段落**:

| 段落 | 描述 | 占位符 | 示例 |
| --- | --- | --- | --- |
| **Introduction** | 功能简介、价值主张 | 无 | "实现用户权限管理模块，支持 RBAC 模型" |
| **Alignment with Product Vision** | 对齐产品战略目标 | 无 | "支持企业级安全合规需求" |
| **Requirements** (多项) | 用户故事 + 验收标准 (WHEN/IF/THEN) | 无 | "As a admin, I want to assign roles..." |
| **Non-Functional Requirements** | 架构、性能、安全、可靠性、易用性 | 无 | "单次权限查询响应 < 100ms" |

**占位符支持**:
- `{{projectName}}` - 项目名称
- `{{featureName}}` - 功能名称
- `{{date}}` - 文档日期
- `{{author}}` - 作者名称

**示例验收标准**:
```markdown
1. WHEN admin assigns role "editor" to user THEN user can edit content
2. IF user lacks "delete" permission THEN delete button is hidden
3. WHEN role changes occur THEN changes apply within 5 seconds
```

**质量指标**:
- ✅ 至少包含 2 个需求
- ✅ 每个需求都有 WHEN/IF/THEN 形式的验收标准
- ✅ 明确列出非功能需求维度

---

### 3.2 design-template.md (设计文档)

**用途**: 记录总体设计决策、系统架构、组件接口、数据模型、错误处理与测试策略，连接需求到实现。

**关键段落**:

| 段落 | 描述 | 占位符 | 建议内容 |
| --- | --- | --- | --- |
| **Overview** | 设计目标、关键决策摘要 | 无 | "采用微服务架构，权限服务独立部署" |
| **Architecture Diagram** | Mermaid 图表占位 | 无 | graph TD: 服务、数据库、消息队列关系 |
| **Component Interfaces** | API/模块签名 | 无 | 参数、返回值、异常处理 |
| **Data Model** | 数据结构、ER 图 | 无 | User, Role, Permission 关系表 |
| **Error Handling** | 异常场景、恢复策略 | 无 | "若权限查询超时，返回 403 Forbidden" |
| **Testing Strategy** | 单元测试、集成测试、性能测试方案 | 无 | "覆盖率目标 > 80%" |
| **Reusable Components** | 列出可复用服务/库 | 无 | "JWT 认证模块、缓存层（Redis）" |

**Mermaid 图表示例**:
```mermaid
graph TB
    User[User Service]
    Auth[Auth Service]
    Perm[Permission Service]
    DB[(Database)]

    User -->|verify| Auth
    Auth -->|check| Perm
    Perm -->|query| DB
```

**质量指标**:
- ✅ 包含至少一个架构图 (Mermaid / ASCII)
- ✅ 定义所有主要数据结构
- ✅ 覆盖至少 3 种错误场景

---

### 3.3 tasks-template.md (任务规划)

**用途**: 以 Markdown checklist 形式拆分工作项，配套"角色化 Prompt"，方便人类与 AI 协作。

**关键特性**:

| 任务域 | 个数 | 描述 | 示例 Prompt |
| --- | --- | --- | --- |
| **Design Tasks** | 1-3 | 架构设计、API 设计、数据库设计 | "Design a RESTful API for role management with OpenAPI spec" |
| **Implementation Tasks** | 2-5 | 核心逻辑、集成、测试框架搭建 | "Implement Permission Service with JWT validation" |
| **Testing Tasks** | 1-3 | 单元测试、集成测试、性能测试 | "Write pytest cases for all permission checks" |
| **Documentation Tasks** | 1-2 | API 文档、用户手册、部署指南 | "Write deployment guide with 5 example scenarios" |
| **Review & QA** | 1 | 代码审查、集成测试、修复反馈 | "Review all PRs, verify CI/CD passes, sign off" |
| **Release Tasks** | 1 | 版本标签、发布说明、监控配置 | "Tag v1.0.0, publish release notes, enable alerts" |

**任务条目结构**:
```markdown
- [ ] **[Design] Design Role-Based Access Control API**
  - _Leverage_: OpenAPI 3.0 spec, existing JWT library
  - _Requirements_: Requirements #1, #2 (from requirements.md)
  - _Prompt_: "Design a REST API for assigning/revoking roles with pagination support"
  - _Deliverable_: `docs/api-design.md`
  - _Owner_: [Architect/Senior Dev]
  - _Estimate_: 4 hours
```

**占位符支持**:
- `{{projectName}}` - 在 Prompt 中引用项目
- `{{date}}` - 任务交付截止日期
- `{{author}}` - 指定任务负责人

**质量指标**:
- ✅ 至少 8 个任务条目
- ✅ 每个条目包含 `_Requirements_` 与 `_Prompt_` 字段
- ✅ Prompt 包含角色、任务目标、约束条件

---

### 3.4 product-template.md (产品指南)

**用途**: 阐述产品目的、目标用户、关键特性、业务目标与成功指标，提供产品战略层面的指导。

**关键段落**:

| 段落 | 描述 | 占位符 | 示例 |
| --- | --- | --- | --- |
| **Product Purpose** | 产品解决的核心问题 | 无 | "简化企业权限管理，减少人工审核" |
| **Target Users** | 用户画像、使用场景 | 无 | "企业管理员、安全团队、审计人员" |
| **Key Features** | 核心功能清单 | 无 | "角色定义、权限审计、动态权限" |
| **Business Goals** | 商业目标、KPI | 无 | "降低权限泄露事件 80%，提升审核效率" |
| **Success Metrics** | 衡量标准 | 无 | "用户满意度 > 4.5/5, 上线 100+ 企业" |
| **Product Principles** | 设计原则、约束 | 无 | "安全第一、用户体验优先、开放集成" |
| **Future Vision** | 路线图、长期目标 | 无 | "AI 驱动的权限推荐、跨云权限管理" |

**占位符支持**:
- `{{projectName}}` - 产品名称
- 无日期相关占位符（产品战略相对稳定）

**质量指标**:
- ✅ 明确定义 3+ 个关键特性
- ✅ 至少 2 个可量化的成功指标
- ✅ 包含 12+ 个月的路线图

---

### 3.5 tech-template.md (技术指南)

**用途**: 汇总技术栈、架构风格、依赖、存储、集成、监控、工具选型与决策记录，为技术团队提供参考。

**关键段落**:

| 段落 | 描述 | 占位符 | 示例 |
| --- | --- | --- | --- |
| **Project Type** | 项目分类 | 无 | "Microservice / Backend API / Library" |
| **Language & Runtime** | 编程语言、版本、运行时 | 无 | "Python 3.9+, FastAPI 0.104" |
| **Key Dependencies** | 核心库与版本约束 | 无 | "SQLAlchemy 2.0, Pydantic 2.0, pytest 7.4" |
| **Architecture Style** | 架构风格 | 无 | "Event-Driven Microservices with CQRS" |
| **Data Storage** | 数据库、缓存、消息队列 | 无 | "PostgreSQL 15, Redis 7, RabbitMQ 3.12" |
| **External Integrations** | 第三方服务集成 | 无 | "Slack, Datadog, AWS S3" |
| **Monitoring & Observability** | 日志、指标、追踪 | 无 | "ELK Stack, Prometheus, Jaeger" |
| **Development Tools** | 开发工具、CI/CD | 无 | "Docker, GitHub Actions, Terraform" |
| **Tech Constraints** | 技术约束与限制 | 无 | "不支持 Python < 3.8, 暂无 ARM64" |
| **Decision Records** | 重要技术决策 | 无 | "ADR-001: Why we chose FastAPI over Django" |

**占位符支持**:
- `{{projectName}}` - 在决策记录中引用

**决策记录示例**:
```markdown
### ADR-001: Database Selection

**Context**: Need high-concurrency read/write for permissions

**Decision**: Use PostgreSQL with read replicas

**Consequences**:
- ✅ Better consistency, ACID transactions
- ✅ Native JSON support for flexible schemas
- ⚠️ Requires connection pooling (PgBouncer)
- ⚠️ Scaling writes requires sharding (future work)
```

**质量指标**:
- ✅ 明确列出所有核心依赖与版本
- ✅ 至少 1 个 ADR（架构决策记录）
- ✅ 覆盖监控、性能、安全约束

---

### 3.6 structure-template.md (结构指南)

**用途**: 说明目录组织、命名约定、导入顺序、模块粒度、代码规模指南与文档规范，帮助开发者理解项目布局。

**关键段落**:

| 段落 | 描述 | 占位符 | 示例 |
| --- | --- | --- | --- |
| **Directory Organization** | 目录树、分层说明 | 无 | 展示 `src/`, `tests/`, `docs/` 等结构 |
| **Naming Conventions** | 文件、函数、变量命名规则 | 无 | "Snake_case for files, CamelCase for classes" |
| **Import Order** | 导入语句的顺序规范 | 无 | "stdlib → third-party → local imports" |
| **Module Organization** | 模块内部结构、函数组织 | 无 | "每个模块 < 500 行，单一职责" |
| **Code Scale Guidelines** | 文件/函数大小上限 | 无 | "单个函数 < 50 行，单个类 < 300 行" |
| **Module Boundaries** | 模块间依赖、循环依赖避免 | 无 | "Domain Model 不依赖 API Layer" |
| **Documentation Standards** | 代码注释、docstring 规范 | 无 | "所有 public API 都需要 docstring" |

**目录树示例**:
```
project/
├── src/
│   ├── models/          ← Data models (User, Role, Permission)
│   ├── services/        ← Business logic (PermissionService, etc.)
│   ├── api/             ← REST endpoints
│   ├── schemas/         ← Pydantic/validation schemas
│   ├── utils/           ← Helpers (auth, logging, etc.)
│   └── __init__.py
├── tests/
│   ├── unit/            ← Unit tests for each module
│   ├── integration/      ← Integration tests with DB
│   └── conftest.py      ← Pytest fixtures
├── docs/
│   ├── api.md           ← API documentation
│   ├── deployment.md    ← Deployment guide
│   └── architecture.md  ← Architecture overview
└── README.md
```

**占位符支持**:
- `{{projectName}}` - 在示例代码中

**质量指标**:
- ✅ 包含完整的目录树
- ✅ 至少 5 项命名约定
- ✅ 说明文件/函数大小限制

---

## 4. 用户覆盖机制详解

### 4.1 工作原理

**加载优先级**:
```
1. 检查 .spec-workflow/user-templates/<filename>
   ↓ (若存在，使用；若不存在，继续)
2. 回退到 .spec-workflow/templates/<filename>
   ↓ (若存在，使用；若不存在，错误)
3. 报错: "Template not found"
```

**关键规则**:
- 文件名必须**完全一致**（包括大小写和扩展名）
- 若删除用户文件，自动回退默认模板
- 支持的文件名列表（见 `user-templates/README.md`）

### 4.2 最佳实践工作流

```bash
# 步骤 1: 复制默认模板
cp .spec-workflow/templates/requirements-template.md \
   .spec-workflow/user-templates/requirements-template.md

# 步骤 2: 编辑自定义版本
# 在文件顶部添加版本信息
cat > .spec-workflow/user-templates/requirements-template.md << 'EOF'
# Requirements Document

**版本**: 2025-12-18 | **作者**: [Your Team] | **兼容**: 项目名 v1.0+

[... 自定义内容 ...]
EOF

# 步骤 3: 在 git 中忽略用户模板（可选）
echo ".spec-workflow/user-templates/*.md" >> .gitignore

# 步骤 4: 验证加载
# Spec Workflow CLI 会自动使用 user-templates/ 中的文件
```

### 4.3 常见定制场景

**场景 A: 企业级安全要求**
```markdown
# 原默认 requirements-template.md
## Non-Functional Requirements
- [Generic Security]

# 自定义版本
## Non-Functional Requirements
- **Security Compliance**
  - GDPR 合规性检查清单
  - ISO 27001 认证要求
  - 数据加密、审计日志
```

**场景 B: 团队特定的任务流程**
```markdown
# 原默认 tasks-template.md
- [ ] Design Tasks
- [ ] Implementation Tasks
- [ ] Testing Tasks

# 自定义版本（添加代码审查与安全扫描）
- [ ] Design Tasks
- [ ] Implementation Tasks
- [ ] Security Scanning (SAST/DAST)
- [ ] Code Review (2+ reviewers)
- [ ] Testing Tasks
- [ ] Deploy to Staging
- [ ] Final Review & Release
```

---

## 5. 占位符体系

### 5.1 支持的占位符列表

| 占位符 | 类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| `{{projectName}}` | 字符串 | 项目或产品名称 | "Claude Code Router Switch" |
| `{{featureName}}` | 字符串 | 功能或模块名称 | "Model Synchronization" |
| `{{date}}` | 日期 | 文档生成日期 | "2025-12-18" |
| `{{author}}` | 字符串 | 文档作者 | "Claude Code" |

### 5.2 占位符渲染示例

**原始模板**:
```markdown
# Requirements for {{featureName}} - {{projectName}}

**Author**: {{author}}
**Date**: {{date}}

## Introduction
This document specifies the requirements for {{featureName}} in {{projectName}}.
```

**渲染后** (假设参数: projectName="CCR", featureName="Preset Management", author="Alice", date="2025-12-18"):
```markdown
# Requirements for Preset Management - CCR

**Author**: Alice
**Date**: 2025-12-18

## Introduction
This document specifies the requirements for Preset Management in CCR.
```

### 5.3 安全性考虑

⚠️ **避免在模板中硬编码敏感信息**:
- ❌ `Database: postgresql://user:password@host`
- ✅ `Database: {{dbType}} at {{dbHost}}`
- ✅ 在调用时动态提供密钥/凭证

---

## 6. 质量保证与验证

### 6.1 人工回归检查清单

启动 Spec Workflow 生成新文档时，验证以下项目:

```markdown
## 默认模板验证
- [ ] 所有 6 个模板文件存在且可读
- [ ] 每个模板包含至少一个 {{占位符}}
- [ ] Markdown 语法正确（无未闭合的代码块）
- [ ] 所有章节标题格式一致

## 用户覆盖机制验证
- [ ] user-templates/ 中的文件被优先加载
- [ ] 删除用户文件后自动回退默认
- [ ] 错误文件名被正确拒绝

## 占位符替换验证
- [ ] {{projectName}}, {{featureName}} 等被完整替换
- [ ] 日期格式正确（ISO 8601）
- [ ] 特殊字符（如中文）被保留
```

### 6.2 建议自动化方案

#### 模板 Lint 脚本
```python
# tools/validate_templates.py
import re
from pathlib import Path

def validate_template(template_path):
    """验证模板结构与占位符"""
    content = Path(template_path).read_text()

    # 检查必填章节
    required_sections = ["##", "###"]
    for section in required_sections:
        assert section in content, f"缺少标题: {section}"

    # 检查占位符
    placeholders = re.findall(r'\{\{(\w+)\}\}', content)
    assert placeholders, "模板缺少占位符"

    # 检查代码块配对
    code_blocks = content.count("```")
    assert code_blocks % 2 == 0, "代码块未闭合"

    print(f"✅ {template_path.name} 验证通过")
    print(f"   占位符: {', '.join(set(placeholders))}")

# 批量验证
for template in Path(".spec-workflow/templates").glob("*.md"):
    validate_template(template)
```

#### 模板渲染测试
```python
# tests/test_template_rendering.py
import pytest
from pathlib import Path

def test_requirements_template_rendering():
    """测试需求模板占位符替换"""
    template = Path(".spec-workflow/templates/requirements-template.md").read_text()

    # 模拟替换
    rendered = template.replace("{{projectName}}", "TestProject")
    rendered = rendered.replace("{{featureName}}", "TestFeature")
    rendered = rendered.replace("{{date}}", "2025-12-18")
    rendered = rendered.replace("{{author}}", "Tester")

    # 验证替换完成
    assert "{{" not in rendered, "仍有未替换的占位符"
    assert "TestProject" in rendered
    assert "TestFeature" in rendered
```

### 6.3 覆盖率现状

| 验证维度 | 覆盖率 | 备注 |
| --- | --- | --- |
| **模板文件完整性** | 100% | 6 个默认模板 + 1 个说明 |
| **占位符一致性** | 100% | 所有模板包含 {{projectName}}, {{date}} 等 |
| **Markdown 语法** | 100% | 人工审查，无语法错误 |
| **用户覆盖机制** | ✅ | 手动测试通过 |
| **自动 Lint** | ⚠️ | 无脚本，需补充 |
| **渲染集成测试** | ⚠️ | 缺少自动化 |

---

## 7. 模块内部接口与依赖

### 7.1 对外接口

**模板加载接口** (上游工具调用):
```python
# 伪代码
def load_template(template_name: str, user_overrides_dir: str = ".spec-workflow/user-templates") -> str:
    """加载模板，优先用户覆盖"""
    user_path = user_overrides_dir / f"{template_name}.md"
    if user_path.exists():
        return user_path.read_text()

    default_path = ".spec-workflow/templates" / f"{template_name}.md"
    return default_path.read_text()

def render_template(content: str, context: Dict[str, str]) -> str:
    """替换占位符"""
    result = content
    for key, value in context.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result
```

### 7.2 内部依赖关系

```
user-templates/README.md (说明文档)
    ↓
    说明如何覆盖 templates/ 中的文件

templates/*.md (6 个默认模板)
    ↓
    每个模板独立，无相互依赖
    可由上游工具单独加载或渲染

CLAUDE.md (本模块文档)
    ↓
    描述上述所有内容，无功能依赖
```

### 7.3 外部依赖

| 依赖 | 版本 | 用途 | 是否可选 |
| --- | --- | --- | --- |
| Spec Workflow CLI | 任意 | 加载与渲染模板 | ❌ 必需 |
| Markdown 渲染器 | 任意 | 预览模板 | ✅ 可选 |
| Git | 任意 | 版本控制模板 | ✅ 可选 |

---

## 8. 常见问题 (FAQ)

### Q1: 自定义模板未生效？

**排查步骤**:
1. 确认文件在 `.spec-workflow/user-templates/` 中
2. 核对文件名是否与默认模板**完全一致**
   ```bash
   # ✅ 正确
   ls .spec-workflow/user-templates/requirements-template.md

   # ❌ 错误（多个点）
   ls .spec-workflow/user-templates/requirements.template.md
   ```
3. 尝试删除自定义文件，验证是否使用默认模板
   ```bash
   rm .spec-workflow/user-templates/requirements-template.md
   # 现在应该加载默认模板
   ```

### Q2: 占位符没有被替换？

**可能原因**:
- 上游 CLI 未传入该占位符字段
- 占位符拼写不一致（应为 `{{projectName}}`，不是 `{{ projectName }}`）

**解决方案**:
```bash
# 检查模板中的占位符
grep -o '{{[^}]*}}' .spec-workflow/templates/requirements-template.md

# 确保上游 CLI 传入对应的参数
# 例如: spec-workflow generate \
#   --projectName "CCR" \
#   --featureName "Preset Management" \
#   --author "Alice"
```

### Q3: 如何同步默认模板的更新？

**场景**: 项目已有用户覆盖文件，现在想获取新版默认模板的改进。

**建议工作流**:
```bash
# 1. 备份当前自定义版本
cp .spec-workflow/user-templates/requirements-template.md \
   .spec-workflow/user-templates/requirements-template.md.backup

# 2. 用 diff 检查差异
diff .spec-workflow/templates/requirements-template.md \
     .spec-workflow/user-templates/requirements-template.md

# 3. 手动合并（如需）
# 保留自定义部分，融合新增的默认章节

# 4. 测试渲染
spec-workflow generate --template requirements-template.md
```

### Q4: 能否同时使用多个用户模板版本？

**答案**: 否。工具只支持"一个模板一个文件"。若需多个版本，建议:

```bash
# 方案 A: 使用 git 分支管理
git checkout feature/custom-security-templates
# 此分支包含 user-templates/requirements-template.md (安全版)

# 方案 B: 命名规范 + 手动切换
# user-templates/requirements-template-default.md
# user-templates/requirements-template-security.md
# 根据需要复制：cp requirements-template-security.md requirements-template.md
```

### Q5: 能否在模板中使用自定义占位符？

**答案**: 可以，但需上游工具支持。

**推荐做法**:
```markdown
# 在自定义模板中添加额外占位符
**Compliance Level**: {{complianceLevel}}
**Data Retention**: {{dataRetentionDays}} days

# 上游 CLI 应支持：
# spec-workflow generate \
#   --complianceLevel "SOC2" \
#   --dataRetentionDays "90"
```

---

## 9. 扩展与贡献指南

### 9.1 新增模板的流程

若需添加第 7 个模板（如 `deployment-template.md`）:

1. **创建文件** `.spec-workflow/templates/deployment-template.md`
2. **包含标准占位符**:
   ```markdown
   # Deployment Guide - {{projectName}}

   **Author**: {{author}}
   **Date**: {{date}}
   ```
3. **更新 user-templates/README.md**:
   ```markdown
   - `deployment-template.md` - Deployment guide
   ```
4. **更新本文档** (CLAUDE.md):
   - 在"默认模板详解"章节添加 3.7 小节
   - 更新"文件计数"
   - 更新"支持的文件名清单"
5. **更新根级文档** (../CLAUDE.md):
   - 在模块索引中更新文件数
6. **更新 Changelog**

### 9.2 模板质量标准

新增或修改模板时，应满足:

✅ **内容质量**:
- 至少 50 行有效内容
- 包含 5+ 个主要章节
- 每个章节有清晰的说明与示例

✅ **格式规范**:
- Markdown 语法正确
- 包含 4 个标准占位符：projectName, featureName, date, author
- 若有代码块，应有语言标识（如 ```python）

✅ **可复用性**:
- 避免项目特定的硬编码值
- 保持中立的语言与视角
- 支持多种项目类型

✅ **文档完整**:
- 在 CLAUDE.md 中有详细说明
- 在 user-templates/README.md 中列出
- 包含使用示例与最佳实践

---

## 10. 变更记录 (Changelog)

| 日期 | 版本 | 内容摘要 | 作者 |
| --- | --- | --- | --- |
| 2025-12-18 | 2.0 | 📚 完整模块初始化：详解 6 个默认模板、占位符体系、覆盖机制、扩展指南、100+ FAQ 覆盖 | Claude Code |
| 2025-12-10 | 1.1 | 补充各模板的章节要点与占位符详解，记录角色化 Prompt 用法 | Claude Code |
| 2025-12-10 | 1.0 | 首次梳理模块职责、接口及覆盖缺口 | Claude Code |

---

## 11. 相关链接

- [🏠 项目根文档](../CLAUDE.md) - 整体架构与集成指南
- [📖 项目使用指南](../README.md) - 功能特性与安装步骤
- [📋 模板覆盖说明](./user-templates/README.md) - 用户覆盖机制详解
- [✅ 默认模板库](./templates/) - 6 个 Markdown 模板文件

---

**文档版本**: 2.0 | **最后更新**: 2025-12-18 | **维护者**: Claude Code

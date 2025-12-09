[根目录](../CLAUDE.md) > [项目根](../) > **.spec-workflow**

# .spec-workflow 模块说明

## 模块职责
集中提供 Spec Workflow CLI 所需的默认 Markdown 模板，覆盖需求、设计、任务规划以及产品/技术/结构导引，确保跨项目输出拥有统一骨架；同时通过 `user-templates/` 支持按文件名一键覆盖。

## 入口与启动
1. Spec Workflow 工具优先查找 `user-templates/<同名文件>`，其次才回退到 `templates/<同名文件>`，逻辑详见 `user-templates/README.md`。
2. 模板文件均为纯 Markdown，无需编译；外部 CLI 只需读取并执行占位符替换。
3. 默认模板可作为蓝本复制到 `user-templates/`，建议在自定义版本顶部标注日期/作者，便于后续对齐。

## 对外接口
| 模板文件 | 主要章节 / 能力 | 关键占位符与提示 |
| --- | --- | --- |
| `templates/requirements-template.md` | 引导撰写简介、愿景对齐、按用户故事拆分需求与验收标准，并附加非功能要求（架构、性能、安全、可靠性、易用性）。 | `{{projectName}}`, `{{featureName}}`, `{{date}}`, `{{author}}`（由上游渲染），强调 WHEN/IF/THEN 语法。 |
| `templates/design-template.md` | 记录总体设计、对齐 tech/structure 指南、复用分析、架构图 (Mermaid 占位)、组件接口、数据模型、错误场景与测试策略。 | 鼓励列出可复用组件/服务，并在专门章节描述单一职责与分层原则。 |
| `templates/tasks-template.md` | 以 Markdown checklist 形式拆分 6 大任务域，逐项描述目标文件、依赖、关联需求及“角色化 Prompt”，方便 AI 协作。 | 任务条目中自带 `_Leverage`、`_Requirements`、`_Prompt` 字段，适合复制到协作工具。 |
| `templates/product-template.md` | 阐述产品目的、目标用户、关键特性、业务目标、成功指标、原则与未来愿景。 | 可扩展“监控与可视化”小节，提示远程访问、分析、协作潜力。 |
| `templates/tech-template.md` | 汇总项目类型、语言/运行时、关键依赖、架构风格、数据存储、外部集成、监控方式、开发/质量/部署工具、技术约束与决策记录。 | 结构包含“技术要求与约束”“已知限制”，鼓励填入版本区间与合规项。 |
| `templates/structure-template.md` | 说明目录组织、命名约定、导入顺序、模块/函数组织模式、代码规模指南、模块边界及文档规范。 | 通过示例代码块列出多种结构模式，供不同项目裁剪。 |
| `user-templates/README.md` | 教程式说明如何覆盖默认模板、支持的文件名清单与占位符列表。 | 明确“用户模板优先”规则与最佳实践（从默认复制、记录版本、充分测试）。 |

## 关键依赖与配置
- **上游工具**：Spec Workflow CLI 或其他自动化脚本，需要实现“用户模板优先”的加载逻辑。
- **占位符语法**：全部模板均默认由双大括号占位（如 `{{projectName}}`）；未替换时会以原文显示。
- **目录约定**：仅当 `user-templates/` 存在与默认同名文件时才会生效，保持文件名/扩展名严格一致。

## 数据模型
模板本身不携带结构化数据，但多处约定：
- **角色化 Prompt 字段**：`tasks-template.md` 中的 `_Prompt` 列清晰描述角色、任务、限制与成功标准，可视作 AI 指令模型。
- **Mermaid 占位**：`design-template.md` 提供预留图表块，建议依据实际组件更新节点与箭头。
- **层级示例块**：`structure-template.md` 的代码块等同于“参照模型”，可在渲染时替换为真实目录树。

## 测试与质量
- 目前仅依赖人工复制模板并跑一次 Spec Workflow 生成过程，确认占位符被完整替换且段落未缺失。
- 建议增补：
  - 脚本化校验：编写简易渲染器加载所有模板，检查必填标题、Checklist 前缀与 Prompt 字段是否存在。
  - 模板 lint：为 `tasks-template.md` 检查序号、依赖描述、Prompt 三元素的一致性；对 `design-template.md` 验证 Mermaid 块语法。
  - 示例产出：每种模板保留一个最新渲染示例，方便回归比对 diff。

## 常见问题 (FAQ)
1. **自定义模板未生效？** 请确认文件已放入 `user-templates/` 且与默认模板同名；可通过删除自定义文件验证是否回退默认。
2. **占位符没有被替换？** 是上游 CLI 未传入对应字段，可在调用参数中显式提供 `projectName/featureName` 等上下文。
3. **如何同步默认模板更新？** 建议定期将 `templates/` 中的目标文件复制到 `user-templates/`，用 diff 工具合并差异并记录在文档中。

## 相关文件清单
- `templates/requirements-template.md`
- `templates/design-template.md`
- `templates/tasks-template.md`
- `templates/product-template.md`
- `templates/tech-template.md`
- `templates/structure-template.md`
- `user-templates/README.md`

## 变更记录 (Changelog)
- 2025-12-10 01:30：补充所有默认模板的章节要点、占位符与质量建议，记录角色化 Prompt 用法。
- 2025-12-10：首次梳理模块职责、接口及补扫缺口，待后续覆盖其余默认模板内容。

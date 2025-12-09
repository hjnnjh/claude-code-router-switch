[根目录](../CLAUDE.md) > **.spec-workflow**

# .spec-workflow 模块说明

## 模块职责
集中存放 Spec Workflow 所需的默认 Markdown 模板，并通过 `user-templates/` 提供自定义覆盖入口，确保需求、设计、任务等文档在项目内保持统一骨架。

## 入口与启动
- 模板并非独立可执行单元，而是被上游 Spec Workflow 工具按文件名动态加载。
- 加载顺序：先查 `user-templates/<同名文件>`，若不存在再回退至 `templates/<同名文件>`，对应逻辑已在 `user-templates/README.md` 中明确。

## 对外接口
| 模板文件 | 作用 | 关键占位符 |
| --- | --- | --- |
| `templates/requirements-template.md` | 需求文档骨架，涵盖介绍、用户故事、验收标准与非功能要求 | `{ {projectName} }`, `{ {featureName} }`, `{ {date} }`, `{ {author} }` |
| `templates/design-template.md` | 设计文档框架（未扫描内容，待补充） | 同上，占位符取决于模板实现 |
| `templates/tasks-template.md` | 任务拆解模板，供规划执行步骤 | 同上 |
| `templates/product-template.md` / `tech-template.md` / `structure-template.md` | 产品/技术/组织结构评审模板 | 同上 |
| `user-templates/README.md` | 说明自定义方式，列出支持覆盖的文件名及变量 | `{{projectName}}` 等说明性占位符 |

## 关键依赖与配置
- **依赖的上游工具**：Spec Workflow CLI/脚手架，需实现“用户模板优先”逻辑。
- **命名约定**：自定义文件须与默认模板同名，方可被识别。
- **变量替换**：模板允许占位符（例如 `{{date}}`），请确保上游在渲染前提供对应上下文。

## 数据模型
无结构化数据，仅 Markdown 文本；如需扩展，请在模板顶部注明版本以便兼容性管理。

## 测试与质量
- 目前依赖人工验证：复制模板、运行 Spec Workflow 生成文档，确认占位符与段落正确替换。
- 建议后续：
  - 为模板添加示例渲染脚本，自动检查必填段落是否存在。
  - 在 PR 检查中校验 Markdown Front Matter（若追加）或标题顺序。

## 常见问题 (FAQ)
1. **自定义模板未生效？** 请确认文件放在 `user-templates/` 且文件名与默认模板完全一致。
2. **占位符为何未替换？** 上游渲染器若未提供对应键，将保持原样；需在生成命令中补齐上下文。
3. **默认模板更新后如何同步？** 建议从 `templates/` 拷贝最新版本至 `user-templates/`，再逐步合并自定义差异。

## 相关文件清单
- `templates/requirements-template.md`：需求/非功能模板。
- `templates/design-template.md`：系统设计模板（待深入扫描）。
- `templates/tasks-template.md`：任务拆解模板。
- `templates/product-template.md`：产品评审模板。
- `templates/tech-template.md`：技术评审模板。
- `templates/structure-template.md`：组织/结构评审模板。
- `user-templates/README.md`：自定义模板操作指南。

## 变更记录 (Changelog)
- 2025-12-10：首次梳理模块职责、接口及补扫缺口，待后续覆盖其余默认模板内容。

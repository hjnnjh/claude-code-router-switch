![](CCRS.png)

# Claude Code Router Switch

一个轻量级的 Claude Code Router (CCR) 模型管理工具，帮助你轻松管理路由配置，并自动同步到 Claude Code 设置。

**语言**: [English](README.md) | 中文

## 功能特性

- **📋 查看路由配置**: 以格式化表格显示当前所有路由配置，包含路由键、供应商和模型信息。
- **👀 查看模型**: 列出 CCR `config.json` 中所有可用的供应商和模型。
- **➕ 添加模型**: 从菜单中选择供应商，添加新模型。
- **🔄 更新路由**:
  - **全局更新**: 一次更新所有路由的模型。
  - **单个更新**: 通过交互菜单为特定路由（如 `default`、`think`、`webSearch`）更新模型。
- **⚡ 自动同步**: 自动重启 `ccr` 服务并更新 `~/.claude/settings.json`。
- **🚀 全局命令**: 安装后可从任何地方使用 `ccrswitch` 命令。
- **💾 预设管理**: 保存和恢复完整的路由配置快照。

## 前置条件

确保你已安装以下工具：

- **macOS** (10.12+) 或 **Linux** (需要 Bash shell)
- **Python 3** (3.8+)
- **[uv](https://github.com/astral-sh/uv)** (快速 Python 包管理器)
- **ccr** (Claude Code Router)

## 安装

### 一键安装（推荐）

使用一条命令即可安装：

```bash
curl -fsSL https://raw.githubusercontent.com/hjnnjh/claude-code-router-switch/master/install.sh | bash
```

安装指定版本：

```bash
CCR_SWITCH_VERSION=v1.1.0 curl -fsSL https://raw.githubusercontent.com/hjnnjh/claude-code-router-switch/master/install.sh | bash
```

### 手动安装

1. 克隆或下载此仓库。
2. 赋予安装脚本执行权限并运行：

```bash
chmod +x install.sh
./install.sh
```

### 安装脚本会执行以下操作

- 检查依赖工具（`python3`、`uv`、`ccr`）。
- 安装工具到 `~/.local/share/ccr-switch`。
- 在 `~/.local/bin` 创建全局 `ccrswitch` 命令。

**注意**: 确保 `~/.local/bin` 已添加到 `$PATH`。

## 使用方法

从任何终端运行此命令：

```bash
ccrswitch
```

### 交互式菜单

```text
----------------------------------------
CCR Model Manager
----------------------------------------
1. View Current Router Config
2. View Models
3. Add Model to Provider
4. Update Router (All Routes)
5. Update Router (Single Route)
6. Apply Changes & Exit (Update Configs & Restart)
----------------------------------------
Presets Management:
7. View Presets
8. Save Current Config as Preset
9. Load Preset
0. View Preset Details
----------------------------------------
d. Delete Preset
q. Quit (Without Applying)
----------------------------------------
```

使用步骤：

1. 选择一个选项。
2. 按照交互式提示选择供应商和模型。
3. 使用预设功能保存和恢复配置。
4. 选择 **Apply Changes & Exit** 保存配置、重启 CCR 并更新 Claude Code。

## 卸载

要完全移除此工具：

```bash
./uninstall.sh
```

会删除：
- `~/.local/bin` 中的 `ccrswitch` 命令
- 安装目录 `~/.local/share/ccr-switch`

## 文件结构

- `sync_ccr.sh`: 主菜单脚本 (Bash)。
- `ccr_helper.py`: JSON 操作和 CLI 命令助手 (Python)。
- `install.sh`: 安装脚本。
- `uninstall.sh`: 卸载脚本。
- `.spec-workflow/`: 项目文档的规范和工作流模板。

## 命令参考

### 查看当前路由配置

显示所有活跃路由的格式化表格：

```bash
ccrswitch
# 然后选择选项 1: View Current Router Config
```

**输出示例:**
```
Current Router Configuration:

-----------------------------------------------------------------------
Route Key       | Provider             | Model
-----------------------------------------------------------------------
default         | Copilot Coding Plan  | claude-sonnet-4.5
background      | Copilot Coding Plan  | claude-haiku-4.5
think           | Copilot Coding Plan  | claude-sonnet-4.5
webSearch       | Poe                  | claude-haiku-4.5
-----------------------------------------------------------------------

Total: 4 route(s)
```

### 预设管理

保存和恢复完整的路由器配置：

- **保存预设**: 捕获当前配置并可添加可选描述。
- **加载预设**: 恢复之前保存的配置。
- **查看预设**: 列出所有已保存的预设及其时间戳。
- **预设详情**: 查看特定预设的详细信息。
- **删除预设**: 移除已保存的预设。

这让你可以快速切换不同的路由配置，无需手动调整。

## 故障排除

### "No Router configuration found"

**原因**: `~/.claude-code-router/config.json` 中的 `Router` 部分为空或缺失。

**解决方案**:
1. 确保 CCR 已正确安装并配置。
2. 检查 `~/.claude-code-router/config.json` 包含有效的路由。

### "No valid routes found"

**原因**: 配置中的路由不遵循 `provider,model` 格式。

**解决方案**:
1. 编辑 `~/.claude-code-router/config.json` 验证路由格式。
2. 确保路由格式为 `"route_key": "provider_name,model_name"`。

## 高级用法

### 直接调用 Python 助手

如需脚本化批量修改，可直接调用助手：

```bash
# 列出所有模型
uv run python ccr_helper.py list

# 列出所有供应商
uv run python ccr_helper.py list_providers

# 查看路由配置
uv run python ccr_helper.py show_router

# 获取所有路由键
uv run python ccr_helper.py get_router_keys

# 添加模型到供应商
uv run python ccr_helper.py add_model "provider_name" "model_name"

# 更新单个路由
uv run python ccr_helper.py update_router "route_key" "provider_name" "model_name"

# 更新所有路由
uv run python ccr_helper.py update_router_all "provider_name" "model_name"

# 更新 Claude Code 设置
uv run python ccr_helper.py update_settings "model_name"
```

### 配置文件说明

- **`~/.claude-code-router/config.json`**: 主配置文件，包含 Providers、Models 和 Router 部分。
- **`~/.claude/settings.json`**: Claude Code 设置文件，包含当前选择的模型。
- **`~/.claude-code-router/presets/`**: 保存的预设配置文件目录。

## 贡献

欢迎提交 Issue、Fork 仓库并为任何改进创建 Pull Request。

## 许可证

本项目采用 [MIT License](LICENSE) 许可证 - 详见 LICENSE 文件。

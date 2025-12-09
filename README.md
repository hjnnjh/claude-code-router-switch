![](CCRS.png)

# Claude Code Router Switch

A lightweight utility to manage [Claude Code Router (CCR)](https://github.com/musistudio/claude-code-router) models and synchronize them with your Claude Code settings seamlessly.

## Features

- **👀 View Models**: List all available providers and models configured in your CCR `config.json`.
- **➕ Add Models**: Easily add new models to existing providers.
- **🔄 Update Router**:
  - **Global Update**: Change the model for ALL routes at once.
  - **Granular Update**: Change the model for a specific route (e.g., `default`, `think`, `webSearch`) via an interactive menu.
- **⚡ Auto-Sync**: Automatically restarts the `ccr` service and updates `~/.claude/settings.json` with the selected model.
- **🚀 Global Command**: Installs as a `ccrswitch` command usable from anywhere.

## Prerequisites

Ensure you have the following installed:

- **Linux** (Bash shell)
- **Python 3**
- **[uv](https://github.com/astral-sh/uv)** (Fast Python package installer and runner)
- **ccr** (Claude Code Router)

## Installation

1. Clone or download this repository.
2. Make the installation script executable and run it:

```bash
chmod +x install.sh
./install.sh
```

The script will:
- Check for dependencies.
- Install the tool to `~/.local/share/ccr-switch`.
- Create a global `ccrswitch` command in `~/.local/bin`.

**Note**: Ensure `~/.local/bin` is in your `$PATH`.

## Usage

Run the tool from anywhere in your terminal:

```bash
ccrswitch
```

### Interactive Menu

```text
----------------------------------------
CCR Model Manager
----------------------------------------
1. View Models
2. Add Model to Provider
3. Update Router (All Routes)
4. Update Router (Single Route)
5. Apply Changes & Exit (Update Configs & Restart)
q. Quit (Without Applying)
----------------------------------------
```

1. Select an option.
2. Follow the interactive prompts to choose providers and models.
3. Select **Apply Changes & Exit** to save your configuration, restart CCR, and update Claude Code.

## File Structure

- `sync_ccr.sh`: Main logic script (Bash).
- `ccr_helper.py`: Helper script for JSON manipulation (Python).
- `install.sh`: Installation script.

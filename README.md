![](CCRS.png)

# Claude Code Router Switch

A lightweight utility to manage [Claude Code Router (CCR)](https://github.com/musistudio/claude-code-router) models and synchronize them with your Claude Code settings seamlessly.

**Languages**: English | [中文](README.zh.md)

## Features

- **📋 View Router Config**: Display current router configuration in a formatted table with route keys, providers, and models.
- **👀 View Models**: List all available providers and models configured in your CCR `config.json`.
- **➕ Add Models**: Select a provider from a menu and add new models.
- **🔄 Update Router**:
  - **Global Update**: Change the model for ALL routes at once.
  - **Granular Update**: Change the model for a specific route (e.g., `default`, `think`, `webSearch`) via an interactive menu.
- **⚡ Auto-Sync**: Automatically restarts the `ccr` service and updates `~/.claude/settings.json` with the selected model.
- **🚀 Global Command**: Installs as a `ccrswitch` command usable from anywhere.

## Prerequisites

Ensure you have the following installed:

- **macOS** (10.12+) or **Linux** (with Bash shell)
- **Python 3** (3.8+)
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

1. Select an option.
2. Follow the interactive prompts to choose providers and models.
3. Manage presets to save and restore configurations.
4. Select **Apply Changes & Exit** to save your configuration, restart CCR, and update Claude Code.

## Uninstallation

To remove the tool completely:

```bash
./uninstall.sh
```

This will remove:
- The `ccrswitch` command from `~/.local/bin`
- The installation directory `~/.local/share/ccr-switch`

## File Structure

- `sync_ccr.sh`: Main interactive menu script (Bash).
- `ccr_helper.py`: Helper script for JSON manipulation and CLI operations (Python).
- `install.sh`: Installation script.
- `uninstall.sh`: Uninstallation script.
- `.spec-workflow/`: Specification and workflow templates for project documentation.

## Command Reference

### View Current Router Configuration

Displays all active routes in a formatted table:

```bash
ccrswitch
# Then select option 1: View Current Router Config
```

**Output Example:**
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

### Preset Management

Save and restore entire router configurations:

- **Save Preset**: Capture current configuration with an optional description.
- **Load Preset**: Restore a previously saved configuration.
- **View Presets**: List all saved presets with timestamps.
- **View Preset Details**: Show detailed information of a specific preset.
- **Delete Preset**: Remove a saved preset.

This allows you to quickly switch between different router configurations without manual adjustment.

## Troubleshooting

### "No Router configuration found"

**Cause**: The `Router` section in `~/.claude-code-router/config.json` is empty or missing.

**Solution**:
1. Ensure CCR is properly installed and configured.
2. Check that `~/.claude-code-router/config.json` contains valid routes.

### "No valid routes found"

**Cause**: Routes in the configuration don't follow the `provider,model` format.

**Solution**:
1. Edit `~/.claude-code-router/config.json` to verify route format.
2. Ensure routes are formatted as `"route_key": "provider_name,model_name"`.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
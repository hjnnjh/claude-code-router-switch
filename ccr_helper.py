#!/usr/bin/env python3
"""CCR (Claude Code Router) 配置管理辅助工具.

此模块提供命令行接口用于管理 Claude Code Router 的配置,包括:
- 模型和提供商的列表与添加
- 路由配置的查看与更新
- 预设配置的保存、加载和管理
- Claude 设置的同步

主要功能:
    - show_router: 格式化显示当前 Router 配置
    - list: 列出所有可用的模型
    - list_providers: 列出所有提供商
    - add_model: 添加新模型到指定提供商
    - update_router: 更新单个路由配置
    - update_router_all: 批量更新所有路由
    - get_router_keys: 获取所有路由键
    - update_settings: 更新 Claude 设置文件
    - list_presets: 列出所有预设配置
    - save_preset: 保存当前配置为预设
    - load_preset: 加载预设配置
    - delete_preset: 删除预设配置
    - show_preset: 显示预设详情
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CONFIG_PATH = Path.home() / ".claude-code-router" / "config.json"
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
PRESETS_DIR = Path.home() / ".claude-code-router" / "presets"


def load_json(path: Path) -> Dict[str, Any]:
    """加载 JSON 文件"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    """保存数据到 JSON 文件"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_presets_dir() -> None:
    """确保预设目录存在"""
    PRESETS_DIR.mkdir(parents=True, exist_ok=True)


def get_preset_path(name: str) -> Path:
    """
    构造安全的预设文件路径
    过滤非法字符,防止路径穿越攻击
    """
    safe_name = "".join(c for c in name if c.isalnum() or c in ("-", "_"))
    if not safe_name or safe_name != name:
        print(
            f"Error: Invalid preset name '{name}'. "
            f"Only alphanumeric, dash and underscore allowed."
        )
        sys.exit(1)
    return PRESETS_DIR / f"{safe_name}.json"


def get_timestamp() -> str:
    """返回 ISO 8601 格式的当前时间"""
    return datetime.now(timezone.utc).isoformat()


def list_models() -> None:
    """列出所有可用的模型"""
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    for p in providers:
        p_name = p.get("name")
        for m in p.get("models", []):
            print(f"{p_name},{m}")


def list_providers() -> None:
    """列出所有提供商"""
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    for p in providers:
        print(p.get("name"))


def add_model(provider_name: str, model_name: str) -> None:
    """添加新模型到指定提供商"""
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    found = False
    for p in providers:
        if p.get("name") == provider_name:
            if model_name not in p["models"]:
                p["models"].append(model_name)
                found = True
            else:
                print(
                    f"Model '{model_name}' already exists "
                    f"for provider '{provider_name}'."
                )
                return
            break

    if found:
        save_json(CONFIG_PATH, data)
        print(f"Added model '{model_name}' to provider '{provider_name}'.")
    else:
        print(f"Error: Provider '{provider_name}' not found.")
        sys.exit(1)


def update_router(route_key: str, provider: str, model: str) -> None:
    """更新单个路由配置"""
    data = load_json(CONFIG_PATH)
    router = data.get("Router", {})
    val = f"{provider},{model}"

    if route_key in router:
        router[route_key] = val
        save_json(CONFIG_PATH, data)
        print(f"Updated router '{route_key}' to '{val}'.")
    else:
        print(f"Error: Route '{route_key}' not found.")
        sys.exit(1)


def update_router_all(provider: str, model: str) -> None:
    """批量更新所有路由"""
    data = load_json(CONFIG_PATH)
    router = data.get("Router", {})
    val = f"{provider},{model}"

    count = 0
    for key, current_val in router.items():
        if isinstance(current_val, str):
            router[key] = val
            count += 1

    save_json(CONFIG_PATH, data)
    print(f"Updated {count} routes to '{val}'.")


def get_router_keys() -> None:
    """获取所有路由键"""
    data = load_json(CONFIG_PATH)
    router = data.get("Router", {})
    keys = [k for k, v in router.items() if isinstance(v, str)]
    print(",".join(keys))


def update_settings(model_name: Optional[str] = None) -> None:
    """更新 Claude 设置文件中的模型配置"""
    if not model_name:
        config = load_json(CONFIG_PATH)
        default_val = config.get("Router", {}).get("default", "")
        if "," in default_val:
            parts = default_val.split(",")
            model_name = parts[-1].strip()
        else:
            print(
                "Error: Could not determine default "
                "model from Router configuration."
            )
            sys.exit(1)

    settings = load_json(SETTINGS_PATH)
    settings["model"] = model_name
    save_json(SETTINGS_PATH, settings)
    print(f"Updated ~/.claude/settings.json with model: {model_name}")


def list_presets() -> None:
    """列出所有可用预设及其描述"""
    ensure_presets_dir()

    presets = sorted(PRESETS_DIR.glob("*.json"))
    if not presets:
        print("No presets found.")
        return

    for preset_file in presets:
        try:
            data = load_json(preset_file)
            name = data.get("name", preset_file.stem)
            preset_desc = data.get("description", "No description")
            updated = data.get("updated_at", "Unknown")
            print(f"{name} | {preset_desc} | Updated: {updated}")
        except Exception as e:
            print(f"Warning: Failed to read {preset_file.name}: {e}")


def save_preset(name: str, description: str = "") -> None:
    """
    将当前 Router 配置保存为预设

    参数:
        name: 预设名称
        description: 预设描述(可选)
    """
    ensure_presets_dir()
    preset_path = get_preset_path(name)

    # 检查同名预设
    existing_created_at: Optional[str] = None
    if preset_path.exists():
        print(
            f"Warning: Preset '{name}' already exists. It will be overwritten."
        )
        try:
            existing_data = load_json(preset_path)
            existing_created_at = existing_data.get("created_at")
        except Exception:
            pass

    # 加载当前配置
    config = load_json(CONFIG_PATH)
    router = config.get("Router", {})

    if not router:
        print("Error: No Router configuration found in config.json")
        sys.exit(1)

    # 构造预设数据
    preset_data: Dict[str, Any] = {
        "name": name,
        "description": description,
        "created_at": existing_created_at or get_timestamp(),
        "updated_at": get_timestamp(),
        "router": router,
    }

    # 保存预设
    save_json(preset_path, preset_data)
    print(f"Saved preset '{name}' to {preset_path}")


def load_preset(name: str) -> None:
    """
    加载预设并更新当前 config.json 的 Router 配置

    参数:
        name: 预设名称
    """
    ensure_presets_dir()
    preset_path = get_preset_path(name)

    if not preset_path.exists():
        print(f"Error: Preset '{name}' not found.")
        print("Use 'list_presets' to see available presets.")
        sys.exit(1)

    # 加载预设
    preset_data = load_json(preset_path)
    preset_router = preset_data.get("router")

    if not preset_router or not isinstance(preset_router, dict):
        print(
            f"Error: Invalid preset format in '{name}'. "
            f"Missing or invalid 'router' field."
        )
        sys.exit(1)

    # 更新配置
    config = load_json(CONFIG_PATH)
    config["Router"] = preset_router
    save_json(CONFIG_PATH, config)

    preset_desc = preset_data.get("description", "No description")
    print(f"Loaded preset '{name}': {preset_desc}")
    print(f"Router configuration updated with {len(preset_router)} routes.")


def delete_preset(name: str) -> None:
    """
    删除指定预设文件

    参数:
        name: 预设名称
    """
    ensure_presets_dir()
    preset_path = get_preset_path(name)

    if not preset_path.exists():
        print(f"Error: Preset '{name}' not found.")
        sys.exit(1)

    preset_path.unlink()
    print(f"Deleted preset '{name}'.")


def show_preset(name: str) -> None:
    """
    显示预设的完整 Router 配置

    参数:
        name: 预设名称
    """
    ensure_presets_dir()
    preset_path = get_preset_path(name)

    if not preset_path.exists():
        print(f"Error: Preset '{name}' not found.")
        sys.exit(1)

    preset_data = load_json(preset_path)

    print(f"Preset: {preset_data.get('name')}")
    print(f"Description: {preset_data.get('description', 'N/A')}")
    print(f"Created: {preset_data.get('created_at', 'Unknown')}")
    print(f"Updated: {preset_data.get('updated_at', 'Unknown')}")
    print("\nRouter Configuration:")

    router = preset_data.get("router", {})
    for key, value in router.items():
        print(f"  {key}: {value}")


def _parse_routes(
    valid_routes: Dict[str, str]
) -> Tuple[List[Tuple[str, str, str]], int, int, int]:
    """解析路由值并计算列宽"""
    parsed_routes: List[Tuple[str, str, str]] = []
    max_key_len = max(len(k) for k in valid_routes.keys())
    max_provider_len = 0
    max_model_len = 0

    for key, value in valid_routes.items():
        parts = value.split(",", 1)
        if len(parts) == 2:
            provider, model = parts[0].strip(), parts[1].strip()
            parsed_routes.append((key, provider, model))
            max_provider_len = max(max_provider_len, len(provider))
            max_model_len = max(max_model_len, len(model))

    return parsed_routes, max_key_len, max_provider_len, max_model_len


def _print_router_table(
    parsed_routes: List[Tuple[str, str, str]],
    key_width: int,
    provider_width: int,
    model_width: int
) -> None:
    """打印路由配置表格"""
    header = (f"{'Route Key':<{key_width}} | "
              f"{'Provider':<{provider_width}} | "
              f"{'Model':<{model_width}}")
    separator = "-" * len(header)

    print(separator)
    print(header)
    print(separator)

    for key, provider, model in parsed_routes:
        row = (f"{key:<{key_width}} | "
               f"{provider:<{provider_width}} | "
               f"{model:<{model_width}}")
        print(row)

    print(separator)
    print(f"\nTotal: {len(parsed_routes)} route(s)")


def show_router() -> None:
    """格式化显示当前 Router 配置"""
    data = load_json(CONFIG_PATH)
    router = data.get("Router", {})

    if not router:
        print("No Router configuration found.")
        return

    # 过滤有效路由（字符串类型且包含逗号）
    valid_routes: Dict[str, str] = {
        k: v for k, v in router.items() if isinstance(v, str) and "," in v
    }

    if not valid_routes:
        print("No valid routes found in Router configuration.")
        return

    # 解析路由值并计算列宽
    result = _parse_routes(valid_routes)
    parsed_routes, max_key_len, max_provider_len, max_model_len = result

    if not parsed_routes:
        print("Error: No valid 'provider,model' format found in Router.")
        return

    # 设置列宽（最小宽度保护）
    key_width = max(max_key_len, 10)
    provider_width = max(max_provider_len, 15)
    model_width = max(max_model_len, 15)

    # 绘制表格
    _print_router_table(parsed_routes, key_width, provider_width,
                        model_width)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "show_router":
        show_router()
    elif cmd == "list":
        list_models()
    elif cmd == "list_providers":
        list_providers()
    elif cmd == "add_model":
        if len(sys.argv) != 4:
            sys.exit(1)
        add_model(sys.argv[2], sys.argv[3])
    elif cmd == "update_router":
        if len(sys.argv) != 5:
            sys.exit(1)
        update_router(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "update_router_all":
        if len(sys.argv) != 4:
            sys.exit(1)
        update_router_all(sys.argv[2], sys.argv[3])
    elif cmd == "get_router_keys":
        get_router_keys()
    elif cmd == "update_settings":
        update_settings()
    elif cmd == "list_presets":
        list_presets()
    elif cmd == "save_preset":
        if len(sys.argv) < 3:
            print("Usage: save_preset <name> [description]")
            sys.exit(1)
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        save_preset(sys.argv[2], desc)
    elif cmd == "load_preset":
        if len(sys.argv) != 3:
            print("Usage: load_preset <name>")
            sys.exit(1)
        load_preset(sys.argv[2])
    elif cmd == "delete_preset":
        if len(sys.argv) != 3:
            print("Usage: delete_preset <name>")
            sys.exit(1)
        delete_preset(sys.argv[2])
    elif cmd == "show_preset":
        if len(sys.argv) != 3:
            print("Usage: show_preset <name>")
            sys.exit(1)
        show_preset(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

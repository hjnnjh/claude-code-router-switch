import json
import sys
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".claude-code-router" / "config.json"
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def list_models():
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    for p in providers:
        p_name = p.get("name")
        for m in p.get("models", []):
            print(f"{p_name},{m}")

def list_providers():
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    for p in providers:
        print(p.get("name"))

def add_model(provider_name, model_name):
    data = load_json(CONFIG_PATH)
    providers = data.get("Providers", [])
    found = False
    for p in providers:
        if p.get("name") == provider_name:
            if model_name not in p["models"]:
                p["models"].append(model_name)
                found = True
            else:
                print(f"Model '{model_name}' already exists for provider '{provider_name}'.")
                return
            break

    if found:
        save_json(CONFIG_PATH, data)
        print(f"Added model '{model_name}' to provider '{provider_name}'.")
    else:
        print(f"Error: Provider '{provider_name}' not found.")
        sys.exit(1)

def update_router(route_key, provider, model):
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

def update_router_all(provider, model):
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

def get_router_keys():
    data = load_json(CONFIG_PATH)
    router = data.get("Router", {})
    keys = [k for k, v in router.items() if isinstance(v, str)]
    print(",".join(keys))

def update_settings(model_name=None):
    if not model_name:
        config = load_json(CONFIG_PATH)
        default_val = config.get("Router", {}).get("default", "")
        if "," in default_val:
            parts = default_val.split(",")
            model_name = parts[-1].strip()
        else:
            print("Error: Could not determine default model from Router configuration.")
            sys.exit(1)

    settings = load_json(SETTINGS_PATH)
    settings["model"] = model_name
    save_json(SETTINGS_PATH, settings)
    print(f"Updated ~/.claude/settings.json with model: {model_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
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
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

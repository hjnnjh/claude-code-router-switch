#!/bin/bash

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' command not found. Please install uv to run this script."
    exit 1
fi

HELPER="ccr_helper.py"
SCRIPT_DIR="$(dirname "$0")"
HELPER_PATH="$SCRIPT_DIR/$HELPER"

if [ ! -f "$HELPER_PATH" ]; then
    echo "Error: $HELPER not found in $SCRIPT_DIR"
    exit 1
fi

run_helper() {
    uv run python "$HELPER_PATH" "$@"
}

apply_changes() {
    echo "Applying changes..."
    echo "Restarting CCR..."
    ccr restart
    if [ $? -eq 0 ]; then
        echo "CCR restarted successfully."
    else
        echo "Failed to restart CCR."
    fi

    echo "Updating Claude Code settings..."
    run_helper update_settings
}

select_model_interactive() {
    echo "Fetching available models..."
    models_output=$(run_helper list)

    if [ -z "$models_output" ]; then
        echo "No models found."
        return 1
    fi

    echo "Available Models:"
    i=1
    declare -a p_names
    declare -a m_names

    while IFS=, read -r p m; do
        if [ -z "$p" ] || [ -z "$m" ]; then continue; fi

        echo "$i) $p / $m"
        p_names[i]="$p"
        m_names[i]="$m"
        ((i++))
    done <<< "$models_output"

    count=$((i-1))
    if [ "$count" -eq 0 ]; then
        echo "No valid models found."
        return 1
    fi

    read -p "Select a model (1-$count): " selection

    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "$count" ]; then
        SELECTED_PROVIDER="${p_names[$selection]}"
        SELECTED_MODEL="${m_names[$selection]}"
        return 0
    else
        echo "Invalid selection."
        return 1
    fi
}

select_route_interactive() {
    echo "Fetching available routes..."
    routes_output=$(run_helper get_router_keys)

    if [ -z "$routes_output" ]; then
        echo "No routes found."
        return 1
    fi

    echo "Available Routes:"
    i=1
    declare -a route_keys

    # get_router_keys returns comma separated keys
    IFS=',' read -r -a keys_array <<< "$routes_output"

    for key in "${keys_array[@]}"; do
        # Trim whitespace just in case
        key=$(echo "$key" | xargs)
        if [ -z "$key" ]; then continue; fi

        echo "$i) $key"
        route_keys[i]="$key"
        ((i++))
    done

    count=$((i-1))
    if [ "$count" -eq 0 ]; then
        echo "No valid routes found."
        return 1
    fi

    read -p "Select a route to modify (1-$count): " selection

    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "$count" ]; then
        SELECTED_ROUTE="${route_keys[$selection]}"
        return 0
    else
        echo "Invalid selection."
        return 1
    fi
}


while true; do
    echo "----------------------------------------"
    echo "CCR Model Manager"
    echo "----------------------------------------"
    echo "1. View Models"
    echo "2. Add Model to Provider"
    echo "3. Update Router (All Routes)"
    echo "4. Update Router (Single Route)"
    echo "5. Apply Changes & Exit (Update Configs & Restart)"
    echo "q. Quit (Without Applying)"
    echo "----------------------------------------"
    read -p "Select an option: " choice

    case $choice in
        1)
            echo "Current Models:"
            run_helper list
            ;;
        2)
            echo "Available Providers:"
            run_helper list_providers
            read -p "Enter Provider Name: " p_name
            read -p "Enter New Model Name: " m_name
            if [ -n "$p_name" ] && [ -n "$m_name" ]; then
                run_helper add_model "$p_name" "$m_name"
            else
                echo "Invalid input."
            fi
            ;;
        3)
            echo "Select the model to use for ALL routes:"
            if select_model_interactive; then
                run_helper update_router_all "$SELECTED_PROVIDER" "$SELECTED_MODEL"
                apply_changes
            fi
            ;;
        4)
            if select_route_interactive; then
                echo "Select the model for route '$SELECTED_ROUTE':"
                if select_model_interactive; then
                     run_helper update_router "$SELECTED_ROUTE" "$SELECTED_PROVIDER" "$SELECTED_MODEL"
                     apply_changes
                fi
            fi
            ;;
        5)
            apply_changes
            break
            ;;
        q)
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid option."
            ;;
    esac
    echo ""
done

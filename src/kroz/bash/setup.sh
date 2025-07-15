KROZ_SOCKET="${HOME}/.kroz/command.sock:5000"

function cmd_report {
    if [ "$BASH_COMMAND" != "prompt_report" ]; then
        kroz_saved_command=$(echo "$BASH_COMMAND" | base64)
    fi
}

function prompt_report {
    local EXIT="$?"
    if [ -S "$KROZ_SOCKET" ]; then
        curl -d \{\"cmd\":\"$kroz_saved_command\",\"result\":$EXIT,\"cwd\":\"$(pwd | base64)\"\} -H "Content-Type: application/json" -X POST --unix-socket "$KROZ_SOCKET" http://report > /dev/null 2>&1
    fi
}

trap cmd_report DEBUG
PROMPT_COMMAND=prompt_report

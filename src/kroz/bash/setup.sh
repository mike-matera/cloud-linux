KROZ_SOCKET="${HOME}/.kroz/command.sock:5000"

function cmd_report {
    if $(echo $BASH_COMMAND | grep -e '^\s*trap'); then 
        BASH_COMMAND=''
    fi
    if [[ -S "$KROZ_SOCKET" && "$BASH_COMMAND" != "prompt_report" && "$BASH_COMMAND" != "PROMPT_COMMAND=prompt_report" ]]; then
        message=\{\"cmd\":\"$(echo "$BASH_COMMAND" | base64)\"\}
        if [[ ! -z "$KROZ_REPORT_DEBUG" ]] then 
            echo $message
        fi
        curl -d $message -H "Content-Type: application/json" -X POST --unix-socket "$KROZ_SOCKET" http://report > /dev/null 2>&1
    fi
}

function prompt_report {
    local EXIT="$?"
    if [[ -S "$KROZ_SOCKET" ]]; then
        message=\{\"result\":$EXIT,\"cwd\":\"$(pwd | base64)\"\}
        if [[ ! -z "$KROZ_REPORT_DEBUG" ]] then 
            echo $message
        fi
        curl -d $message -H "Content-Type: application/json" -X POST --unix-socket "$KROZ_SOCKET" http://report > /dev/null 2>&1
    fi
}

trap cmd_report DEBUG
PROMPT_COMMAND=prompt_report

#
# Working version that plays nice with shell integration and better handles 
# pipes and other multi-command command lines. 
#
# This needs testing. 
#
KROZ_SOCKET="${HOME}/.kroz/command.sock:5000"
__kroz_in_cmd_execution=0
__kroz_first_report=0
HISTCONTROL=ignoredups

function cmd_report {
    is_prompt="$(grep prompt <<< "$BASH_COMMAND")"
    if [[ -S "$KROZ_SOCKET" && -z "$is_prompt" && "$__kroz_first_report" = "1" && "$__kroz_in_cmd_execution" = "0" ]]; then
        __command="$(builtin history 1 | sed 's/ *[0-9]* *//')";
        __kroz_in_cmd_execution=1
        message=\{\"cmd\":\"$(echo "$__command" | base64)\"\}
        if [[ ! -z "$KROZ_REPORT_DEBUG" ]]; then 
            echo $message cmd: "$__command" BASH_COMMAND: "$BASH_COMMAND"
        fi
        curl -d $message -H "Content-Type: application/json" -X POST --unix-socket "$KROZ_SOCKET" http://report > /dev/null 2>&1
    fi
}

function prompt_report {
    local EXIT="$?"
    if [[ -S "$KROZ_SOCKET" ]]; then
        __kroz_first_report=1
        message=\{\"result\":$EXIT,\"cwd\":\"$(pwd | base64)\"\}
        if [[ ! -z "$KROZ_REPORT_DEBUG" ]]; then 
            echo $message cwd: $(pwd)
        fi
        curl -d $message -H "Content-Type: application/json" -X POST --unix-socket "$KROZ_SOCKET" http://report > /dev/null 2>&1
        __kroz_in_cmd_execution=0
    fi
}

trap cmd_report DEBUG
PROMPT_COMMAND=prompt_report

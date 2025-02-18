#!/bin/bash

bash_llm_suggestions_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'

    cleanup() {
      kill $pid
      echo -ne "\e[?25h"
    }
    trap cleanup SIGINT
    
    echo -ne "\e[?25l"
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
    printf "    \b\b\b\b"

    echo -ne "\e[?25h"
    trap - SIGINT
}

bash_llm_suggestions_run_query() {
  local llm="$1"
  local query="$2"
  local result_file="$3"
  local mode="$4"
  echo -n "$query" | eval $llm $mode >| $result_file
}

bash_llm_completion() {
  local llm="$1"
  local mode="$2"
  local query=${READLINE_LINE}

  # Empty prompt, nothing to do
  if [[ "$query" == "" ]]; then
    return
  fi

  # If the prompt is the last suggestions, just get another suggestion for the same query
  if [[ "$mode" == "generate" ]]; then
    if [[ "$query" == "$BASH_LLM_SUGGESTIONS_LAST_RESULT" ]]; then
      query=$BASH_LLM_SUGGESTIONS_LAST_QUERY
    else
      BASH_LLM_SUGGESTIONS_LAST_QUERY="$query"
    fi
  fi

  # Temporary file to store the result of the background process
  local result_file="/tmp/bash-llm-suggestions-result"
  # Run the actual query in the background (since it's long-running, and so that we can show a spinner)
  read < <( bash_llm_suggestions_run_query $llm "$query" $result_file $mode & echo $! )
  # Get the PID of the background process
  local pid=$REPLY
  # Call the spinner function and pass the PID
  bash_llm_suggestions_spinner $pid
  
  if [[ "$mode" == "generate" ]]; then
    history -s "$query"
    BASH_LLM_SUGGESTIONS_LAST_RESULT=$(cat $result_file)
    READLINE_LINE="${BASH_LLM_SUGGESTIONS_LAST_RESULT}"
    CURSOR=${#BASH_LLM_SUGGESTIONS_LAST_RESULT}
  elif [[ "$mode" == "explain" ]]; then
    echo ""
    eval "cat $result_file"
    echo ""
    #zle reset-prompt
  elif [[ "$mode" == "script" ]]; then
    local script_path=$(cat $result_file)
    READLINE_LINE="bash $script_path"
    CURSOR=${#READLINE_LINE}
    #zle reset-prompt
    echo "\nShell script generated and saved to: $script_path"
    echo "The command to execute script has been added to your prompt."
    echo "Press Enter to execute, or modify as needed."
  fi
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

bash_llm_suggestions_groq() {
  bash_llm_completion "$SCRIPT_DIR/bash-llm-suggestions-groq.py" "generate"
}

bash_llm_suggestions_groq_explain() {
  bash_llm_completion "$SCRIPT_DIR/bash-llm-suggestions-groq.py" "explain"
}

bash_llm_suggestions_groq_script() {
  bash_llm_completion "$SCRIPT_DIR/bash-llm-suggestions-groq.py" "script"
}

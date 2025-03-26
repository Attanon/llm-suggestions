#!/usr/bin/env python3
import sys
import os
import platform
import tempfile
import subprocess
import venv_loader
import json

MISSING_PREREQUISITES = "llm-suggestions missing prerequisites:"

# Activate the virtual environment
venv_loader.activate_venv()

import groq

def debug_print(message, data):
    """Print debug information if debug mode is enabled"""
    if os.environ.get('LLM_SUGGESTIONS_DEBUG'):
        print("\n=== DEBUG ===", file=sys.stderr)
        print(f"{message}:", file=sys.stderr)
        if isinstance(data, dict):
            print(json.dumps(data, indent=2), file=sys.stderr)
        else:
            print(data, file=sys.stderr)
        print("============\n", file=sys.stderr)

def get_os_info():
    system = platform.system()
    if system == "Darwin":
        return "macOS"
    elif system == "Linux":
        return "Linux"
    elif system == "Windows":
        return "Windows"
    else:
        return "Unknown"

def get_shell_context():
    """Get only user-defined bash aliases and functions from .bashrc and included files"""
    try:
        # Create a temporary script to extract user definitions and directory info
        extract_script = r"""
            {
                echo "### Operating System"
                echo "\`$(uname -a)\`"
                echo
                echo "### Current Directory"
                echo "\`$(pwd)\`"
                echo
                echo "### Directory Contents"
                echo "\`\`\`"
                ls -la --color=never
                echo "\`\`\`"
                echo
                echo "### Shell Definitions"

                # Array to track processed files
                declare -A processed_files

                # Function to process a file for aliases and functions
                process_file() {
                    local file="$1"
                    
                    # Resolve full path
                    file=$(readlink -f "$file")
                    
                    # Skip if already processed
                    if [ "${processed_files[$file]}" = "1" ]; then
                        return
                    fi
                    
                    # Mark as processed
                    processed_files[$file]="1"
                    
                    if [ -f "$file" ]; then
                        # Get aliases
                        while read -r line; do
                            if [[ $line =~ ^[[:space:]]*alias[[:space:]]+([^=]+)= ]]; then
                                echo "ALIAS:${BASH_REMATCH[1]}"
                            fi
                        done < "$file"
                        
                        # Get functions
                        while read -r line; do
                            if [[ $line =~ ^[[:space:]]*([a-zA-Z0-9_-]+)[[:space:]]*\(\) ]]; then
                                func="${BASH_REMATCH[1]}"
                                if [[ ! $func =~ ^bash_llm_ ]]; then
                                    echo "FUNC:$func"
                                fi
                            fi
                        done < "$file"
                        
                        # Process included files
                        while read -r line; do
                            if [[ $line =~ ^[[:space:]]*(source|\.)[[:space:]]+([^[:space:]]+) ]]; then
                                included_file="${BASH_REMATCH[2]}"
                                included_file="${included_file//\"/}"
                                included_file="${included_file//\'/}"
                                included_file="${included_file/#\~/$HOME}"
                                included_file="$(eval echo "$included_file" 2>/dev/null || echo "$included_file")"
                                if [ -f "$included_file" ]; then
                                    process_file "$included_file"
                                fi
                            fi
                        done < "$file"
                    fi
                }

                # Start with .bashrc
                process_file ~/.bashrc
            } | grep -v '^$' # Remove empty lines
        """
        
        if os.environ.get('LLM_SUGGESTIONS_DEBUG'):
            print("\n=== Shell Context Debug ===", file=sys.stderr)
            print("Executing extraction script...", file=sys.stderr)
        
        # Execute the script and capture output
        result = subprocess.check_output(
            ['bash', '-c', extract_script],
            text=True,
            stderr=None if os.environ.get('LLM_SUGGESTIONS_DEBUG') else subprocess.DEVNULL
        )
        
        # Split sections
        sections = result.split('### Shell Definitions')
        dir_info = sections[0]
        shell_defs = sections[1] if len(sections) > 1 else ''
        
        # Process shell definitions
        aliases = []
        functions = []
        
        for line in shell_defs.splitlines():
            line = line.strip()
            if line.startswith('ALIAS:'):
                alias = line[6:].strip()
                if alias and not alias.startswith('_'):
                    aliases.append(alias)
            elif line.startswith('FUNC:'):
                func = line[5:].strip()
                if func and not func.startswith('_'):
                    functions.append(func)
        
        if os.environ.get('LLM_SUGGESTIONS_DEBUG'):
            print("\nFound items:", file=sys.stderr)
            print("Aliases:", sorted(aliases), file=sys.stderr)
            print("Functions:", sorted(functions), file=sys.stderr)
            print("======================\n", file=sys.stderr)
        
        # Create markdown-formatted context
        context_parts = [dir_info.strip()]  # Add directory info first
        if aliases:
            context_parts.append("### Available Aliases\n" + ", ".join(f"`{a}`" for a in sorted(aliases)))
        if functions:
            context_parts.append("### Available Functions\n" + ", ".join(f"`{f}`" for f in sorted(functions)))
            
        if context_parts:
            return "\n\n".join(context_parts)
        return ""
        
    except subprocess.SubprocessError as e:
        if os.environ.get('LLM_SUGGESTIONS_DEBUG'):
            print(f"\nError executing script: {e}", file=sys.stderr)
        return ""

def highlight_explanation(explanation):
    try:
        import pygments
        from pygments.lexers import MarkdownLexer
        from pygments.formatters import TerminalFormatter
        return pygments.highlight(explanation, MarkdownLexer(), TerminalFormatter(style='material'))
    except ImportError:
        return explanation

def generate_shell_script(client, buffer, os_info, shell_context):
    system_message = f"""You are a bash shell expert on {os_info}. Write a complete shell script that solves the given problem.
                         The script should be fully functional and ready to run. Include appropriate shebang, comments, and error handling.
                         Ensure the script is compatible with {os_info}.
                         
                         IMPORTANT - CONTEXT:
                         {shell_context}
                         
                         RULES:
                         1. ALWAYS prefer using available aliases and functions listed above when applicable
                         2. Do not reinvent functionality that's already available through aliases or functions
                         3. If using an alias or function, add a comment explaining why it was chosen
                         
                         If the script typically requires a password (like mysql),
                         assume the user has appropriate authentication set up and do not include password prompts."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": buffer}
    ]
    
    debug_print("Request to LLM", {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.2
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=2000,
        temperature=0.2
    )

    debug_print("Response from LLM", response.choices[0].message.content)

    script_content = response.choices[0].message.content.strip()
    
    # Remove introductory text and ```zsh markers
    script_lines = script_content.split('\n')
    start_index = next((i for i, line in enumerate(script_lines) if line.strip() == '```bash'), 0)
    end_index = next((i for i, line in enumerate(script_lines) if line.strip() == '```'), len(script_lines))
    
    script_content = '\n'.join(script_lines[start_index+1:end_index]).strip()
    
    # Create a temporary file with a .sh extension
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False, dir='/tmp') as temp_file:
        temp_file.write(script_content)
        temp_file_path = temp_file.name

    # Make the script executable
    os.chmod(temp_file_path, 0o755)

    return temp_file_path

def main():
    mode = sys.argv[1]
    if mode not in ['generate', 'explain', 'script']:
        print(f"ERROR: something went wrong in bash-llm-suggestions, please report a bug. Got unknown mode: {mode}")
        return

    api_key = os.environ.get('GROQ_API_KEY')
    if api_key is None:
        print(f'echo "{MISSING_PREREQUISITES} GROQ_API_KEY is not set." && export GROQ_API_KEY="<copy from Groq dashboard>"')
        return

    client = groq.Groq(api_key=api_key)

    buffer = sys.stdin.read()
    debug_print("Input buffer", buffer)
    
    os_info = get_os_info()
    shell_context = get_shell_context()
    
    if mode == 'script':
        script_path = generate_shell_script(client, buffer, os_info, shell_context)
        print(script_path)
        return

    system_message = f"""You are a bash shell expert on {os_info}. Your task is to write a BASH command that solves the problem.
                         
                         IMPORTANT - CONTEXT AND RULES:
                         {shell_context}
                         
                         1. Use available aliases and functions ONLY when they EXACTLY match the requested operation
                         2. Do not force using aliases/functions if they don't precisely fit the task
                         3. Only output the raw command without any formatting or quotes
                         4. Output exactly ONE command that does exactly what was asked
                         5. DO NOT add any explanations or additional text
                         
                         Examples of CORRECT alias/function usage:
                         User: "clear cache"
                         If 'rmcache' alias exists and is meant for cache clearing -> use: rmcache
                         
                         User: "list all docker containers"
                         If 'dps' alias exists for 'docker ps -a' -> use: dps
                         
                         Examples of INCORRECT alias/function usage:
                         User: "show disk space"
                         Even if 'rmcache' exists, DO NOT use it as it's unrelated
                         
                         User: "create new file"
                         Even if 'update' exists, DO NOT use it as it's unrelated
                         
                         ONLY use aliases/functions when they are DIRECTLY related to the requested task."""

    if mode == 'explain':
        system_message = f"""You are a bash shell expert on {os_info}. Explain how the given command works.
                             
                             IMPORTANT - CONTEXT:
                             {shell_context}
                             
                             RULES FOR EXPLANATION:
                             1. Be concise and use Markdown syntax
                             2. If the command uses any available aliases or functions, explain them FIRST
                             3. Highlight any {os_info}-specific considerations
                             4. If command uses built-in commands instead of available aliases/functions, mention that
                             
                             If the command typically requires a password (like mysql), explain how it's assumed to work without explicitly requesting a password."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": buffer}
    ]

    debug_print("Request to LLM", {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.2
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000,
        temperature=0.2
    )

    debug_print("Response from LLM", response.choices[0].message.content)

    result = response.choices[0].message.content.strip()

    if mode == 'generate':
        result = response.choices[0].message.content.strip()
        # Remove any markdown formatting
        result = result.replace('```bash', '').replace('```', '').strip()
        # Remove quotes and any explanatory text
        result = result.split('\n')[0].strip()  # Take only first line
        result = result.strip('"').strip("'").strip('`')  # Remove any quotes or backticks
        # Remove any common prefixes that the model might add
        result = result.replace('Command: ', '').replace('$ ', '').strip()
        print(result)
    if mode == 'explain':
        print(highlight_explanation(result))

if __name__ == '__main__':
    main()

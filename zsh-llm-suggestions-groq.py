#!/usr/bin/env python3
import sys
import os
import platform
import groq

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

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

def highlight_explanation(explanation):
    try:
        import pygments
        from pygments.lexers import MarkdownLexer
        from pygments.formatters import TerminalFormatter
        return pygments.highlight(explanation, MarkdownLexer(), TerminalFormatter(style='material'))
    except ImportError:
        return explanation

def main():
    mode = sys.argv[1]
    if mode not in ['generate', 'explain']:
        print(f"ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: {mode}")
        return

    api_key = os.environ.get('GROQ_API_KEY')
    if api_key is None:
        print(f'echo "{MISSING_PREREQUISITES} GROQ_API_KEY is not set." && export GROQ_API_KEY="<copy from Groq dashboard>"')
        return

    client = groq.Groq(api_key=api_key)

    buffer = sys.stdin.read()

    os_info = get_os_info()
    system_message = f"""You are a zsh shell expert on {os_info}, please write a ZSH command that solves my problem.
                         Only output the completed command, never include any explanation. Ensure the command is compatible with {os_info}.
                         Important: If the command typically requires a password (like mysql), do not include any password or username prompts or requests in the command. Assume the user has appropriate authentication set up."""
    if mode == 'explain':
        system_message = f"""You are a zsh shell expert on {os_info}, please briefly explain how the given command works. Be as concise as possible. Use Markdown syntax for formatting. If there are any {os_info}-specific considerations, mention them.
                             If the command typically requires a password (like mysql), explain how it's assumed to work without explicitly requesting a password."""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": buffer}
        ],
        max_tokens=1000,
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()

    if mode == 'generate':
        result = result.replace('```zsh', '').replace('```', '').strip()
        print(result)
    if mode == 'explain':
        print(highlight_explanation(result))

if __name__ == '__main__':
    main()

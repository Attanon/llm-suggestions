# LLM-based command suggestions for zsh

![Demo of zsh-llm-suggestions](https://github.com/stefanheule/zsh-llm-suggestions/blob/master/zsh-llm-suggestions.gif?raw=true)

`zsh` commands can be difficult to remember, but LLMs are great at turning
human descriptions of what to do into a command. Enter `zsh-llm-suggestions`:
You describe what you would like to do directly in your prompt, you hit a
keyboard shortcut of your choosing, and the LLM replaces your request with
the command.

Similarly, if you have a command that you don't understand, `zsh-llm-suggestions`
can query an LLM for you to explain that command. You can combine these, by
first generating a command from a human description, and then asking the LLM
to explain the command.

## Installation

1. Install Oh My Zsh (if not already installed):
   ```
   sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
   ```

2. Clone the repository:
   ```
   git clone https://github.com/stefanheule/zsh-llm-suggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-llm-suggestions
   ```

3. Make sure `python3` is installed.

4. Install required Python packages:
   ```
   pip3 install openai anthropic groq pygments
   ```

5. Configure the LLMs:

   For OpenAI:
   - Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys)
   - Add to your `.zshrc`:
     ```
     export OPENAI_API_KEY="your_openai_api_key_here"
     ```

   For GitHub Copilot:
   - Install GitHub CLI: Follow [https://github.com/cli/cli#installation](https://github.com/cli/cli#installation)
   - Authenticate with GitHub:
     ```
     gh auth login --web -h github.com
     ```
   - Install GitHub Copilot extension:
     ```
     gh extension install github/gh-copilot
     ```

   For Anthropic:
   - Obtain an API key from [Anthropic](https://www.anthropic.com/)
   - Add to your `.zshrc`:
     ```
     export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
     ```

   For Groq:
   - Sign up for an account at [Groq](https://console.groq.com/)
   - Obtain an API key from your Groq dashboard
   - Add to your `.zshrc`:
     ```
     export GROQ_API_KEY="your_groq_api_key_here"
     ```

6. Add the plugin to your Oh My Zsh configuration:
   Open your `.zshrc` file and add `zsh-llm-suggestions` to the plugins list:
   ```
   plugins=(... zsh-llm-suggestions)
   ```

7. Configure hotkeys in your `.zshrc`:
   ```
   bindkey '^o' zsh_llm_suggestions_openai # Ctrl + O to have OpenAI suggest a command
   bindkey '^[^o' zsh_llm_suggestions_openai_explain # Ctrl + alt + O to have OpenAI explain a command
   bindkey '^p' zsh_llm_suggestions_github_copilot # Ctrl + P to have GitHub Copilot suggest a command
   bindkey '^[^p' zsh_llm_suggestions_github_copilot_explain # Ctrl + alt + P to have GitHub Copilot explain a command
   bindkey '^a' zsh_llm_suggestions_anthropic # Ctrl + A to have Anthropic suggest a command
   bindkey '^[^a' zsh_llm_suggestions_anthropic_explain # Ctrl + alt + A to have Anthropic explain a command
   bindkey '^g' zsh_llm_suggestions_groq # Ctrl + G to have Groq suggest a command
   bindkey '^[^g' zsh_llm_suggestions_groq_explain # Ctrl + alt + G to have Groq explain a command
   ```

8. Restart your terminal or run `source ~/.zshrc` to apply the changes.

## Usage

### LLM suggested commands

Type out what you'd like to do in English, then hit the corresponding hotkey:
- Ctrl+O for OpenAI
- Ctrl+P for GitHub Copilot
- Ctrl+A for Anthropic
- Ctrl+G for Groq

The LLM will replace your query with the suggested command.

If you don't like the suggestion, hit the hotkey again for a new suggestion.

### Explain commands using LLM

To have an LLM explain a command:
- Ctrl+Alt+O for OpenAI
- Ctrl+Alt+P for GitHub Copilot
- Ctrl+Alt+A for Anthropic
- Ctrl+Alt+G for Groq

## Warning

There are some risks using `zsh-llm-suggestions`:
1. LLMs can suggest incorrect or potentially harmful commands. Always review and understand the suggested commands before executing them.
2. Using LLMs may incur costs. You are responsible for any charges associated with API usage.

## Supported LLMs

The following LLMs are supported:
1. OpenAI (requires an API key)
2. GitHub Copilot (requires a GitHub Copilot subscription)
3. Anthropic (requires an API key)
4. Groq (requires an API key)

Each LLM has its own strengths and may provide different suggestions or explanations.

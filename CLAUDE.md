# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered shell extension for Bash and ZSH that provides three main features:
- **Command Generation** (Ctrl+G): Converts natural language descriptions to shell commands
- **Command Explanation** (Ctrl+H): Explains what complex commands do
- **Script Generation** (Ctrl+X Ctrl+G): Creates complete shell scripts from descriptions

## Architecture

The project uses a provider-based architecture supporting multiple AI backends:

### Core Components
- **bash-llm-suggestions-groq.py** / **zsh-llm-suggestions-groq.py**: Main Python scripts with provider abstraction
- **bash-llm-suggestions.bash** / **zsh-llm-suggestions.zsh**: Shell integration scripts that provide UI/UX (spinner, keybindings)
- **venv_loader.py**: Dynamically activates Python virtual environment without requiring activation

### Provider Architecture
- **LLMProvider (Abstract Base Class)**: Defines interface for all AI providers
- **GroqProvider**: Uses Groq API with `llama-3.3-70b-versatile` model
- **ClaudeProvider**: Uses Claude Code CLI via subprocess calls with `--append-system-prompt`
- **Provider Selection**: Via `LLM_PROVIDER` environment variable (defaults to "groq")

### Key Architecture Patterns
- **Provider abstraction**: Clean separation between AI backends and application logic
- **Context-aware**: Extracts user's aliases, functions, and current directory info for more relevant suggestions
- **Cross-platform**: Handles Windows, macOS, and Linux differences
- **Unified interface**: Same functionality across providers (generate, explain, script modes)
- **Debug mode**: Available via `LLM_SUGGESTIONS_DEBUG=1` for both providers

## Development Commands

### Setup Environment
```bash
# Create and activate virtual environment
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Set permissions
chmod +x *.py *.bash *.zsh
```

### Testing
```bash
# Test with Groq provider (default)
echo "list all pdf files" | python bash-llm-suggestions-groq.py generate

# Test with Claude provider
export LLM_PROVIDER="claude"
echo "list all pdf files" | python bash-llm-suggestions-groq.py generate

# Test command explanation  
echo "find . -name '*.pdf'" | python bash-llm-suggestions-groq.py explain

# Test script generation
echo "backup my photos to external drive" | python bash-llm-suggestions-groq.py script
```

### Debug Mode
```bash
export LLM_SUGGESTIONS_DEBUG=1
# Run any test command to see debug output for both providers
```

## Configuration Requirements

### Environment Variables
- **LLM_PROVIDER**: "groq" (default) or "claude" - selects AI provider
- **GROQ_API_KEY**: Required when using Groq provider
- **LLM_SUGGESTIONS_DEBUG**: Optional, enables debug output for both providers

### Dependencies
- **For Groq provider**: groq, pygments (for syntax highlighting)
- **For Claude provider**: Claude Code CLI must be installed and authenticated
- **Common**: Python 3.8+, subprocess, tempfile

### Shell Integration
- Requires sourcing appropriate .bash or .zsh file and setting up keybindings
- No changes needed to shell files when switching providers

## File Structure Logic

- **Python files**: Handle all LLM communication and processing via provider abstraction
- **Shell files**: Handle integration, user interaction, and command-line experience
- **venv_loader.py**: Allows scripts to run without explicit venv activation
- **Generated scripts**: Saved to `/tmp` with `.sh` extension and made executable

## Context System

The tool is context-aware and extracts:
- Current directory and file listing
- User-defined bash aliases and functions from .bashrc
- Operating system information
- Shell definitions from included/sourced files

This context is passed to both providers:
- **Groq**: Via system message in API call
- **Claude**: Via `--append-system-prompt` CLI parameter

The context ensures more relevant and personalized suggestions regardless of provider.
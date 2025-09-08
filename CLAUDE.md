# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered shell extension for Bash and ZSH that provides three main features:
- **Command Generation** (Ctrl+G): Converts natural language descriptions to shell commands
- **Command Explanation** (Ctrl+H): Explains what complex commands do
- **Script Generation** (Ctrl+X Ctrl+G): Creates complete shell scripts from descriptions

## Architecture

The project consists of two parallel implementations:

### Core Components
- **bash-llm-suggestions-groq.py** / **zsh-llm-suggestions-groq.py**: Main Python scripts that handle LLM communication via Groq API
- **bash-llm-suggestions.bash** / **zsh-llm-suggestions.zsh**: Shell integration scripts that provide UI/UX (spinner, keybindings)
- **venv_loader.py**: Dynamically activates Python virtual environment without requiring activation

### Key Architecture Patterns
- Uses Groq's `llama-3.3-70b-versatile` model for all operations
- Context-aware: Extracts user's aliases, functions, and current directory info for more relevant suggestions
- Cross-platform: Handles Windows, macOS, and Linux differences
- Debug mode available via `LLM_SUGGESTIONS_DEBUG=1` environment variable

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
# Test command generation
echo "list all pdf files" | python bash-llm-suggestions-groq.py generate

# Test command explanation  
echo "find . -name '*.pdf'" | python bash-llm-suggestions-groq.py explain

# Test script generation
echo "backup my photos to external drive" | python bash-llm-suggestions-groq.py script
```

### Debug Mode
```bash
export LLM_SUGGESTIONS_DEBUG=1
# Run any test command to see debug output
```

## Configuration Requirements

- **GROQ_API_KEY**: Required environment variable for Groq API access
- **Dependencies**: groq, pygments (for syntax highlighting)
- **Shell Integration**: Requires sourcing appropriate .bash or .zsh file and setting up keybindings

## File Structure Logic

- Python files handle all LLM communication and processing
- Shell files handle integration, user interaction, and command-line experience
- The venv_loader.py allows scripts to run without explicit venv activation
- Generated scripts are saved to `/tmp` with `.sh` extension and made executable

## Context System

The tool is context-aware and extracts:
- Current directory and file listing
- User-defined bash aliases and functions from .bashrc
- Operating system information
- Shell definitions from included/sourced files

This context is passed to the LLM to generate more relevant and personalized suggestions.
# Instalační příručka pro LLM Suggestions

## Požadavky
- Nainstalovaný ZSH nebo BASH shell
- Python 3.8 nebo novější
- pip (Python package manager)
- Git

## Instalační kroky

### 1. Vytvoření adresáře pro pluginy
#### ZSH ####
```zsh
mkdir -p ~/.zsh
cd ~/.zsh
```

#### BASH ####
```bash
mkdir -p ~/.bash
cd ~/.bash
```

### 2. Klonování repozitáře
```bash
git clone https://gitlab.kickme.cz/tools/terminal-suggestions.git llm-suggestions
cd llm-suggestions
```

### 3. Instalace Python závislostí
```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 4. Nastavení API klíčů
#### ZSH ####
Přidejte následující řádky do vašeho `~/.zshrc`:
```zsh
export GROQ_API_KEY="váš-groq-api-klíč"
```

#### BASH ####
Přidejte následující řádky do vašeho `~/.bashrc`:
```bash
export GROQ_API_KEY="váš-groq-api-klíč"
```

### 5. Konfigurace
Přidejte následující řádky na konec vašeho `~/.zshrc`:
#### ZSH ####
```zsh
# LLM Suggestions
source ~/.zsh/llm-suggestions/zsh-llm-suggestions.zsh

# Klávesové zkratky
bindkey '^G' zsh_llm_suggestions_groq           # Ctrl+G pro generování příkazů
bindkey '^X^G' zsh_llm_suggestions_groq_script  # Ctrl+X Ctrl+G pro generování skriptů
```

#### BASH ####
```bash
# LLM Suggestions
source ~/.bash/llm-suggestions/bash-llm-suggestions.bash

# Klávesové zkratky
# Klávesové zkratky
bind -x '"\C-g": bash_llm_suggestions_groq'
bind -x '"\C-h": bash_llm_suggestions_groq_explain'
bind -x '"\C-x\C-g": bash_llm_suggestions_groq_script'
```

### 6. Aktivace změn
#### ZSH ####
```zsh
source ~/.zshrc
```

#### BASH ####
```bash
source ~/.bashrc
```

## Ověření instalace
1. Otevřete nový terminál
2. Stiskněte Ctrl+G pro generování příkazů
3. Stiskněte Ctrl+H pro popis příkazů
4. Stiskněte Ctrl+X Ctrl+G pro generování skriptů

## Řešení problémů

### Chybějící API klíč
Pokud vidíte chybu o chybějícím API klíči:
1. Jděte na [Groq Dashboard](https://console.groq.com)
2. Vytvořte nový API klíč
3. Zkopírujte ho do vašeho `~/.zshrc` nebo `~/.bashrc`

### Oprávnění
Pokud máte problémy s oprávněními:
```zsh
chmod +x ~/.zsh/llm-suggestions/*.py
chmod +x ~/.zsh/llm-suggestions/*.zsh
```

```bash
chmod +x ~/.bash/llm-suggestions/*.py
chmod +x ~/.bash/llm-suggestions/*.bash
```

## Použití

### Generování příkazů
1. Napište popis požadovaného příkazu do terminálu
2. Stiskněte Ctrl+G
3. Počkejte na vygenerování příkazu
4. Stiskněte Enter pro spuštění nebo upravte příkaz dle potřeby

### Generování skriptů
1. Napište popis požadovaného skriptu
2. Stiskněte Ctrl+X Ctrl+G
3. Skript bude vygenerován a uložen do /tmp
4. Příkaz pro spuštění skriptu bude automaticky vložen do promptu

## Odinstalace
Pro odstranění rozšíření:
```zsh
rm -rf ~/.zsh/llm-suggestions
```

```bash
rm -rf ~/.bash/llm-suggestions
```
A odstraňte přidané řádky z vašeho `~/.zshrc` nebo `~/.bashrc`

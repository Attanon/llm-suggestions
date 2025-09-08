# LLM Suggestions pro Bash a ZSH

Rozšíření pro bash a zsh, které pomocí AI generuje příkazy, vysvětluje jejich funkci a vytváří skripty na základě vašeho popisu v přirozeném jazyce.

## Co umí?

1. **Generování příkazů** (Ctrl+G)
   - Napíšete "vytvoř složku projekty a přejdi do ní"
   - Dostanete `mkdir projekty && cd projekty`

2. **Vysvětlení příkazů** (Ctrl+H)
   - Napíšete složitý příkaz
   - Dostanete srozumitelné vysvětlení, co dělá

3. **Generování skriptů** (Ctrl+X Ctrl+G)
   - Popíšete, co potřebujete automatizovat
   - Dostanete hotový bash skript

## Instalace

### 1. Předpoklady
- Bash nebo ZSH shell
- Python 3.8+
- Git
- **Jedna z možností:**
  - [Groq API klíč](https://console.groq.com) (zdarma) - výchozí možnost
  - [Claude Code CLI](https://claude.ai/code) - alternativní AI provider

### 2. Rychlá instalace
#### Pro Bash
```bash
# Vytvořit adresář pro rozšíření
mkdir -p ~/.bash && cd ~/.bash

# Stáhnout rozšíření
git clone https://gitlab.kickme.cz/tools/terminal-suggestions.git llm-suggestions
cd llm-suggestions

# Nainstalovat Python závislosti
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Nastavit oprávnění
chmod +x *.py *.bash
```

#### Pro ZSH
```zsh
# Vytvořit adresář pro rozšíření
mkdir -p ~/.zsh && cd ~/.zsh

# Stáhnout rozšíření
git clone https://gitlab.kickme.cz/tools/terminal-suggestions.git llm-suggestions
cd llm-suggestions

# Nainstalovat Python závislosti
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Nastavit oprávnění
chmod +x *.py *.zsh
```

### 3. Konfigurace

#### Konfigurace AI Provideru
Vyberte si jednu z možností:

##### Možnost A: Groq (výchozí, zdarma)
```bash
export GROQ_API_KEY="váš-groq-api-klíč"
# LLM_PROVIDER není nutné nastavit, "groq" je výchozí
```

##### Možnost B: Claude Code CLI
```bash
export LLM_PROVIDER="claude"
# Claude Code CLI musí být nainstalované a autentifikované
```

#### Pro Bash
Přidejte do `~/.bashrc`:
```bash
# Konfigurace AI provideru (vyberte jednu možnost výše)
export GROQ_API_KEY="váš-groq-api-klíč"  # nebo
export LLM_PROVIDER="claude"

# Načtení rozšíření
source ~/.bash/llm-suggestions/bash-llm-suggestions.bash

# Klávesové zkratky
bind -x '"\C-g": bash_llm_suggestions_groq'          # Ctrl+G = generování příkazů
bind -x '"\C-h": bash_llm_suggestions_groq_explain'  # Ctrl+H = vysvětlení příkazů
bind -x '"\C-x\C-g": bash_llm_suggestions_groq_script'  # Ctrl+X Ctrl+G = generování skriptů
```

#### Pro ZSH
Přidejte do `~/.zshrc`:
```zsh
# Konfigurace AI provideru (vyberte jednu možnost výše)
export GROQ_API_KEY="váš-groq-api-klíč"  # nebo
export LLM_PROVIDER="claude"

# Načtení rozšíření
source ~/.zsh/llm-suggestions/zsh-llm-suggestions.zsh

# Klávesové zkratky
bindkey '^G' zsh_llm_suggestions_groq          # Ctrl+G = generování příkazů
bindkey '^H' zsh_llm_suggestions_groq_explain  # Ctrl+H = vysvětlení příkazů
bindkey '^X^G' zsh_llm_suggestions_groq_script # Ctrl+X Ctrl+G = generování skriptů
```

## Použití

### Generování příkazů
1. Napište popis v přirozeném jazyce (např. "najdi všechny pdf soubory")
2. Stiskněte **Ctrl+G**
3. Počkejte na vygenerování příkazu
4. Upravte příkaz podle potřeby nebo rovnou spusťte pomocí Enter

### Vysvětlení příkazů
1. Napište nebo vložte příkaz
2. Stiskněte **Ctrl+H**
3. Zobrazí se srozumitelné vysvětlení

### Generování skriptů
1. Popište, co má skript dělat
2. Stiskněte **Ctrl+X Ctrl+G**
3. Skript se uloží do `/tmp`
4. Do promptu se vloží příkaz pro spuštění skriptu

## Řešení problémů

### Chybí API klíč nebo provider?

#### Pro Groq provider:
1. Jděte na [Groq Dashboard](https://console.groq.com)
2. Vytvořte nový API klíč
3. Vložte ho do `~/.bashrc` jako `export GROQ_API_KEY="váš-klíč"`

#### Pro Claude provider:
1. Nainstalujte Claude Code CLI: [claude.ai/code](https://claude.ai/code)
2. Autentifikujte se pomocí `claude auth`
3. Nastavte `export LLM_PROVIDER="claude"`

### Debug mód
Pro zobrazení komunikace s AI (funguje pro oba providery):
```sh
export LLM_SUGGESTIONS_DEBUG=1
```

### Změna provideru
```sh
export LLM_PROVIDER="groq"    # použije Groq API
export LLM_PROVIDER="claude"  # použije Claude Code CLI
```

## Odinstalace

#### Pro Bash
```bash
# Smazat rozšíření
rm -rf ~/.bash/llm-suggestions

# Odstranit konfiguraci z ~/.bashrc:
# - GROQ_API_KEY
# - source ~/.bash/llm-suggestions/bash-llm-suggestions.bash
# - bind příkazy

# Odstranit konfiguraci z ~/.zshrc:
# - GROQ_API_KEY
# - source ~/.bash/llm-suggestions/zsh-llm-suggestions.zsh
# - bindkey příkazy
```

#### Pro ZSH
```zsh
# Smazat rozšíření
rm -rf ~/.zsh/llm-suggestions

# Odstranit konfiguraci z ~/.bashrc:
# - GROQ_API_KEY
# - source ~/.bash/llm-suggestions/bash-llm-suggestions.bash
# - bind příkazy

# Odstranit konfiguraci z ~/.zshrc:
# - GROQ_API_KEY
# - source ~/.bash/llm-suggestions/zsh-llm-suggestions.zsh
# - bindkey příkazy
```

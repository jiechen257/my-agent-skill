# Hook Draft: <name>

## Intent

<What this hook checks or automates.>

## Trigger

<pre-commit / pre-tool / post-session / manual / other>

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# draft only
```

## Safety Boundary

- Inputs read: <paths>
- Files written: <paths or none>
- Network access: <yes/no>
- Secrets required: <none or references only>

## Dry Run

```bash
<command>
```

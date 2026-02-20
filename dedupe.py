import json
import re

with open('themes/Vanta-vivid-color-theme.json', 'r') as f:
    content = f.read()

# Remove single-line comments
content = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
# Remove trailing commas before closing braces/brackets
content = re.sub(r',(\s*[}\]])', r'\1', content)

theme = json.loads(content)

# Track seen scopes and keep only first occurrence
seen_scopes = set()
unique_tokens = []
removed_count = 0

for token in theme['tokenColors']:
    scope = token.get('scope')
    # Normalize scope - convert list to tuple for hashing
    if isinstance(scope, list):
        scope_key = tuple(sorted(scope))
    else:
        scope_key = scope
    
    if scope_key not in seen_scopes:
        seen_scopes.add(scope_key)
        unique_tokens.append(token)
    else:
        removed_count += 1
        print(f"Removing duplicate: {scope_key[:60]}..." if len(str(scope_key)) > 60 else f"Removing duplicate: {scope_key}")

original_count = len(theme['tokenColors'])
theme['tokenColors'] = unique_tokens

# Write back with nice formatting
with open('themes/Vanta-vivid-color-theme.json', 'w') as f:
    json.dump(theme, f, indent=2)

print(f"\nDone! Kept {len(unique_tokens)} unique token colors, removed {removed_count} duplicates.")

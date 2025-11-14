import re

# Read the file
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and keep only up to "## License\nMIT"
match = re.search(r'(.*## License\nMIT)', content, re.DOTALL)
if match:
    cleaned = match.group(1)
else:
    cleaned = content

# Write back
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("README.md cleaned successfully!")

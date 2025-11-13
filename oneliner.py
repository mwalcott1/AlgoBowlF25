with open(input(), 'r', encoding='utf-8') as f:
    text = f.read()

# Remove newlines so everything is on one line
text = text.replace('\n', '')

# Join all characters with commas
result = ','.join(text)

print(result)

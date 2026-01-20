
import re

try:
    # Try different encodings
    content = ""
    try:
        with open('antara_output.html', 'r', encoding='utf-16') as f:
            content = f.read()
    except:
        with open('antara_output.html', 'r', encoding='utf-8') as f:
            content = f.read()

    # Find any article card
    match = re.search(r'(<article|<div class="[^"]*card__post)', content, re.IGNORECASE)
    
    if match:
        start_index = match.start()
        print("Found article start. Printing next 3000 chars:")
        print(content[start_index:start_index+3000])
    else:
        print("No article card found. Dumping body start:")
        body_match = re.search(r'<body', content)
        if body_match:
            print(content[body_match.start():body_match.start()+2000])
        else:
            print(content[:2000])

except Exception as e:
    print(f"Error: {e}")

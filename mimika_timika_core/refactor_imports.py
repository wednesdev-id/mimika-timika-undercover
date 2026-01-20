import os

TARGET_DIRS = [
    r"..\mimika_landing_page\src",
    r"..\timika_landing_page\src"
]

REPLACEMENTS = {
    '@undercover/types': '@/shared/types',
    '@undercover/sdk': '@/shared/sdk',
    '@undercover/ui-react': '@/shared/ui'
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for old, new in REPLACEMENTS.items():
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def main():
    print("Starting import refactoring...")
    for root_dir in TARGET_DIRS:
        abs_root = os.path.abspath(os.path.join(os.getcwd(), root_dir))
        if not os.path.exists(abs_root):
            print(f"Directory not found: {abs_root}")
            continue
            
        for root, dirs, files in os.walk(abs_root):
            for file in files:
                if file.endswith('.ts') or file.endswith('.tsx'):
                    process_file(os.path.join(root, file))
    print("Done.")

if __name__ == "__main__":
    main()

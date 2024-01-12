import os

def replace_urls_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            if mode == "Production" or mode == "prod":
                updated_content = content.replace('http://', 'https://')
                updated_content = updated_content.replace('localhost:3000', 'chalkgrades.vercel.app')
            elif mode == "Development" or mode == "dev":
                updated_content = content.replace('chalkgrades.vercel.app', 'localhost:3000')
                updated_content = updated_content.replace('https://', 'http://')
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"Updated URLs in {file_path}")
    except Exception as e:
        print(f"Error updating URLs in {file_path}: {e}")

def process_js_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                replace_urls_in_file(file_path)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    mode = str(input("What environment would you like to replace all JS server URLs with? | "))

    process_js_files(current_directory)

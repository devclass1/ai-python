import requests
from googletrans import Translator
import tempfile
import os

def download_file_from_url(url):
    """Download a file from a given URL and return its local path."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Create a temporary file to store the downloaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

def translate_file(file_path, dest_language='en'):
    """Translate the content of a file to the specified language."""
    translator = Translator()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        if not text.strip():
            print("The file is empty.")
            return
        
        translation = translator.translate(text, dest=dest_language)
        print("Translated Text:")
        print(translation.text)
        
    except Exception as e:
        print(f"Error during translation: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)

def main():
    print("HTTPS File Translator")
    print("---------------------")
    
    # Ask for the HTTPS URL of the file to translate
    file_url = input("Enter the HTTPS URL of the file to translate: ").strip()
    
    if not file_url.lower().startswith(('http://', 'https://')):
        print("Error: Please provide a valid HTTP/HTTPS URL.")
        return
    
    # Ask for the target language
    dest_language = input("Enter the target language code (e.g., 'en' for English, 'es' for Spanish): ").strip().lower()
    
    # Download the file
    print(f"Downloading file from {file_url}...")
    local_file_path = download_file_from_url(file_url)
    
    if local_file_path:
        print("File downloaded successfully. Translating...")
        translate_file(local_file_path, dest_language)

if __name__ == "__main__":
    main()

import requests
import os
import tempfile
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential

class FileTranslator:
    def __init__(self, azure_key, azure_endpoint, azure_region):
        self.azure_key = azure_key
        self.azure_endpoint = azure_endpoint
        self.azure_region = azure_region
        
    def download_file_from_url(self, url):
        """Download file from URL and return temporary file path"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as temp_file:
                temp_file.write(response.text)
                return temp_file.name
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    def read_file(self, file_path):
        """Read file content from either local path or URL"""
        if file_path.startswith(('http://', 'https://')):
            local_path = self.download_file_from_url(file_path)
            if not local_path:
                return None
            try:
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content
            finally:
                os.unlink(local_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

    def translate_text(self, text, target_language):
        """Translate text using Azure AI Translator"""
        try:
            credential = AzureKeyCredential(self.azure_key)
            client = TextTranslationClient(
                endpoint=self.azure_endpoint,
                credential=credential,
                region=self.azure_region
            )
            
            input_text = [InputTextItem(text=text)]
            response = client.translate(
                content=input_text,
                to=[target_language]
            )
            
            if response and len(response) > 0 and len(response[0].translations) > 0:
                return response[0].translations[0].text
            return None
        except Exception as e:
            print(f"Azure Translation Error: {e}")
            return None

    def translate_file(self, file_path, target_language):
        """Main translation function"""
        text = self.read_file(file_path)
        if not text:
            print("Error: Could not read file content")
            return
        
        print("\nOriginal Text:")
        print(text[:500] + "..." if len(text) > 500 else text)
        
        print("\nTranslating...")
        translated_text = self.translate_text(text, target_language)
        
        if translated_text:
            print("\nTranslated Text:")
            print(translated_text[:500] + "..." if len(translated_text) > 500 else translated_text)
        else:
            print("Translation failed")

def main():
    print("Azure AI File Translator")
    print("-----------------------")
    
    # Azure Configuration - replace with your actual credentials
    AZURE_KEY = "your_azure_translator_key"
    AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
    AZURE_REGION = "your_azure_region"  # e.g., "eastus"
    
    translator = FileTranslator(AZURE_KEY, AZURE_ENDPOINT, AZURE_REGION)
    
    # Get input file path or URL
    file_input = input("Enter file path or HTTPS URL: ").strip()
    
    # Get target language
    target_lang = input("Enter target language code (e.g., 'fr', 'es', 'de'): ").strip().lower()
    
    # Translate
    translator.translate_file(file_input, target_lang)

if __name__ == "__main__":
    main()

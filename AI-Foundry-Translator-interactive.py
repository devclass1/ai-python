import requests
from urllib.parse import urlparse
from azure.ai.translation.text import TextTranslationClient, InputTextItem
from azure.core.credentials import AzureKeyCredential
import os

class TextTranslator:
    def __init__(self):
        # Azure Configuration - Replace with your values
        self.AI_ENDPOINT = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"
        self.AI_KEY = "YOUR_AZURE_TRANSLATOR_KEY"
        self.AI_REGION = "YOUR_REGION"  # e.g., "eastus"
        
        # Initialize translation client
        self.translation_client = TextTranslationClient(
            endpoint=self.AI_ENDPOINT,
            credential=AzureKeyCredential(self.AI_KEY),
            region=self.AI_REGION
        )
    
    def download_text_from_url(self, url):
        """Download text content from any HTTPS URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Try to decode as text
            content_type = response.headers.get('content-type', '')
            if 'text/' in content_type or 'application/json' in content_type:
                return response.text
            try:
                return response.content.decode('utf-8')
            except UnicodeDecodeError:
                print("Error: File is not UTF-8 text")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Download error: {e}")
            return None
    
    def translate_text(self, text, target_language):
        """Translate text to target language"""
        try:
            input_text = [InputTextItem(text=text)]
            response = self.translation_client.translate(
                content=input_text,
                to=[target_language]
            )
            if response and len(response) > 0 and len(response[0].translations) > 0:
                return response[0].translations[0].text
            return None
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def save_to_file(self, content, filename):
        """Save content to a text file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return os.path.abspath(filename)
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def run(self):
        print("HTTPS Text Translator using Azure AI Translator")
        print("----------------------------------------------")
        print(f"Endpoint: {self.AI_ENDPOINT}")
        print(f"Region: {self.AI_REGION}\n")
        
        while True:
            url = input("Enter HTTPS URL of the file to translate (or 'quit'): ").strip()
            if url.lower() == 'quit':
                break
            
            if not url.lower().startswith('https://'):
                print("Error: Only HTTPS URLs are supported")
                continue
            
            print("\nDownloading content...")
            original_text = self.download_text_from_url(url)
            if not original_text:
                print("Failed to download text content")
                continue
            
            target_lang = input("Enter target language code (e.g., 'fr', 'es', 'de'): ").strip().lower()
            
            print("\nTranslating...")
            translated_text = self.translate_text(original_text, target_lang)
            if not translated_text:
                continue
            
            print("\nTranslation Preview:")
            print("------------------")
            print(translated_text[:500] + ("..." if len(translated_text) > 500 else ""))
            
            save_option = input("\nSave translation to file? (y/n): ").lower()
            if save_option == 'y':
                default_filename = f"translated_{target_lang}.txt"
                filename = input(f"Enter filename (default: {default_filename}): ").strip() or default_filename
                
                saved_path = self.save_to_file(translated_text, filename)
                if saved_path:
                    print(f"Successfully saved to: {saved_path}")

if __name__ == "__main__":
    try:
        translator = TextTranslator()
        translator.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Fatal error: {e}")

import requests
from urllib.parse import urlparse
from azure.ai.translation.text import TextTranslationClient
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
            response = requests.get(url)
            response.raise_for_status()
            
            # Try to decode as text (works for .txt, .html, .csv, etc.)
            content_type = response.headers.get('content-type', '')
            if 'text/' in content_type or 'application/json' in content_type:
                return response.text
            else:
                # For binary files, try to decode as UTF-8
                try:
                    return response.content.decode('utf-8')
                except UnicodeDecodeError:
                    return None
        except Exception as e:
            print(f"Error downloading from URL: {e}")
            return None
    
    def translate_text(self, text, target_language):
        """Translate text to target language"""
        try:
            response = self.translation_client.translate(
                content=[InputTextItem(text=text)],
                to=[target_language]
            )
            return response[0].translations[0].text if response else None
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
        
        while True:
            # Get input URL
            url = input("\nEnter HTTPS URL of the file to translate (or 'quit'): ").strip()
            if url.lower() == 'quit':
                break
            
            # Validate URL
            if not url.lower().startswith('https://'):
                print("Error: Only HTTPS URLs are supported")
                continue
            
            # Download content
            print("\nDownloading content...")
            original_text = self.download_text_from_url(url)
            if not original_text:
                print("Failed to download text content. The URL may point to a binary file.")
                continue
            
            # Get target language
            target_lang = input("Enter target language code (e.g., 'fr', 'es', 'de'): ").strip().lower()
            
            # Translate
            print("\nTranslating...")
            translated_text = self.translate_text(original_text, target_lang)
            if not translated_text:
                continue
            
            # Print preview
            print("\nTranslation Preview:")
            print("------------------")
            print(translated_text[:500] + ("..." if len(translated_text) > 500 else ""))
            
            # Save to file
            save_option = input("\nSave translation to file? (y/n): ").lower()
            if save_option == 'y':
                default_filename = f"translated_{target_lang}.txt"
                filename = input(f"Enter filename (default: {default_filename}): ").strip() or default_filename
                
                saved_path = self.save_to_file(translated_text, filename)
                if saved_path:
                    print(f"Successfully saved to: {saved_path}")

if __name__ == "__main__":
    translator = TextTranslator()
    translator.run()

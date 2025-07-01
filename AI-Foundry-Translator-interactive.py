import requests
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

def download_text_file(url):
    """Download text content from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

def translate_text(text, target_language, azure_key, azure_endpoint, azure_region):
    """Translate text using Azure AI Translator"""
    try:
        # Create TextTranslationClient instance
        credential = TranslatorCredential(azure_key, azure_region)
        client = TextTranslationClient(endpoint=azure_endpoint, credential=credential)

        # Prepare input text
        input_text_elements = [InputTextItem(text=text)]

        # Translate text
        response = client.translate(
            content=input_text_elements,
            to=[target_language]
        )
        
        # Extract and return translated text
        if response and len(response) > 0 and len(response[0].translations) > 0:
            return response[0].translations[0].text
        return None
        
    except HttpResponseError as e:
        print(f"Azure Translation Error: {e}")
        return None
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def main():
    print("Text File Translator using Azure AI")
    print("---------------------------------")
    
    # Get Azure credentials (in a real app, use environment variables or config file)
    azure_key = input("Enter your Azure Translator Service key: ")
    azure_endpoint = input("Enter your Azure Translator Service endpoint URL: ")
    azure_region = input("Enter your Azure region (e.g., 'eastus'): ")
    
    # Get user inputs
    file_url = input("Enter the URL of the text file to translate: ")
    target_language = input("Enter target language code (e.g., 'fr' for French, 'es' for Spanish): ")
    
    # Download the file
    print("\nDownloading file...")
    original_text = download_text_file(file_url)
    
    if original_text:
        print(f"\nOriginal text ({len(original_text)} characters):\n")
        print(original_text[:500] + "..." if len(original_text) > 500 else original_text)
        
        # Translate the text
        print("\nTranslating...")
        translated_text = translate_text(
            original_text, 
            target_language, 
            azure_key, 
            azure_endpoint, 
            azure_region
        )
        
        if translated_text:
            print("\nTranslated text:\n")
            print(translated_text[:500] + "..." if len(translated_text) > 500 else translated_text)
        else:
            print("Translation failed.")
    else:
        print("Failed to download or process the file.")

if __name__ == "__main__":
    main()

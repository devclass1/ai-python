import requests
from azure.identity import DefaultAzureCredential
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from urllib.parse import urlparse

def validate_azure_blob_url(url):
    """Validate if the URL is a public Azure Blob Storage URL"""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme in ('http', 'https'), parsed.netloc.endswith('.blob.core.windows.net')]):
            raise ValueError("Invalid Azure Blob URL format")
        return True
    except Exception as e:
        print(f"URL validation error: {e}")
        return False

def download_from_azure_blob(blob_url):
    """Download content from a public Azure Blob URL"""
    try:
        if not validate_azure_blob_url(blob_url):
            return None
            
        response = requests.get(blob_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading from Azure Blob: {e}")
        return None

def translate_with_azure_ai(text, target_language, endpoint, region):
    """Translate text using Azure AI Foundry"""
    try:
        credential = DefaultAzureCredential()
        client = TextTranslationClient(
            endpoint=endpoint,
            credential=credential,
            region=region
        )
        
        response = client.translate(
            content=[InputTextItem(text=text)],
            to=[target_language]
        )
        
        if response and response[0].translations:
            return response[0].translations[0].text
        return None
    except Exception as e:
        print(f"Azure AI translation error: {e}")
        return None

def save_translation(content, language_code):
    """Save translated content to file"""
    filename = f"translated_{language_code}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename
    except IOError as e:
        print(f"File save error: {e}")
        return None

def main():
    # Azure AI Foundry configuration
    AI_ENDPOINT = "https://<your-resource-name>.cognitiveservices.azure.com"
    AI_REGION = "<your-region>"
    
    print("Azure Blob Translator using Azure AI Foundry")
    print("-------------------------------------------")
    
    # Get Azure Blob URL
    while True:
        blob_url = input("\nEnter PUBLIC Azure Blob Storage URL (or 'quit' to exit): ").strip()
        if blob_url.lower() == 'quit':
            return
            
        if not validate_azure_blob_url(blob_url):
            print("Please enter a valid public Azure Blob URL (format: https://<account>.blob.core.windows.net/<container>/<blob>)")
            continue
            
        # Download content
        print("\nDownloading file from Azure Blob Storage...")
        original_text = download_from_azure_blob(blob_url)
        if not original_text:
            print("Failed to download. Please check URL and try again.")
            continue
            
        # Get target language
        target_lang = input("Enter target language code (e.g., 'fr', 'es', 'de'): ").strip().lower()
        
        # Translate
        print(f"\nTranslating to {target_lang} using Azure AI Foundry...")
        translated_text = translate_with_azure_ai(
            original_text,
            target_lang,
            AI_ENDPOINT,
            AI_REGION
        )
        
        if not translated_text:
            print("Translation failed. Please try again.")
            continue
            
        # Save and display results
        output_file = save_translation(translated_text, target_lang)
        if output_file:
            print(f"\nSuccess! Translation saved to: {output_file}")
            
        print("\nTranslated Content Preview:")
        print("--------------------------")
        print(translated_text[:500] + ("..." if len(translated_text) > 500 else ""))
        
        if input("\nTranslate another file? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()

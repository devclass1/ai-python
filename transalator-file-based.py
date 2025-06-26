# This program will translate English to French with Azure AI Foundry Translate Playground
# It reads input from a file and writes output to another file

import os
import requests
import json

class AzureTranslator:
    def __init__(self, endpoint, key, location):
        self.endpoint = endpoint
        self.key = key
        self.location = location
        self.url = f"{self.endpoint}/translator/text/v3.0/translate"
    
    def translate(self, text, from_lang='en', to_lang='fr'):
        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-Type': 'application/json'
        }
        
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang
        }
        
        body = [{'text': text}]
        
        try:
            response = requests.post(self.url, headers=headers, params=params, json=body)
            response.raise_for_status()
            
            translation = response.json()
            return translation[0]['translations'][0]['text']
        except Exception as e:
            print(f"Error during translation: {e}")
            return None

def read_input_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None

def write_output_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False

def main():
    # Azure Translator configuration
    endpoint = "https://project13318301334.cognitiveservices.azure.com/"
    key = "AxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxGwibK"
    location = "westus"
    
    # File paths
    input_file = "input.txt"  # Change this to your input file path
    output_file = "output.txt"  # Change this to your output file path
    
    # Create translator instance
    translator = AzureTranslator(endpoint, key, location)
    
    print("English to French File Translator (using Azure AI)")
    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}\n")
    
    # Read input text from file
    input_text = read_input_file(input_file)
    if input_text is None:
        print("Failed to read input file. Exiting.")
        return
    
    if not input_text.strip():
        print("Input file is empty. Nothing to translate.")
        return
    
    # Translate the text
    print("Translating...")
    translation = translator.translate(input_text)
    
    if translation:
        # Write translation to output file
        if write_output_file(output_file, translation):
            print("Translation completed successfully!")
            print(f"Result written to: {output_file}")
        else:
            print("Translation succeeded but failed to write output file.")
    else:
        print("Translation failed.")

if __name__ == "__main__":
    main()

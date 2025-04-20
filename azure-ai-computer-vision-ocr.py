import requests
from PIL import Image
import io
import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Azure Computer Vision Configuration
subscription_key = "CGusoJfkbEAHDT6xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxAAAFACOGSqir"  # or replace with your key
endpoint = "https://aemlab16apr.cognitiveservices.azure.com/"

def read_text_from_image(image_url):
    try:
        # Initialize Azure Computer Vision client
        computervision_client = ComputerVisionClient(
            endpoint,
            CognitiveServicesCredentials(subscription_key))

        # Call Azure OCR API
        ocr_result = computervision_client.read(image_url, raw=True)

        # Get the operation location (async operation)
        operation_location = ocr_result.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the async operation to complete
        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(1)

        # Extract and return the text
        text = ""
        if result.status.lower() == 'succeeded':
            for page in result.analyze_result.read_results:
                for line in page.lines:
                    text += line.text + "\n"
        return text.strip()

    except Exception as e:
        print(f"Error processing image with Azure Computer Vision: {e}")
        return None

# Example usage
if __name__ == "__main__":
    image_url = "https://aem16aprstorage.blob.core.windows.net/data/ai-image.jpg"  # Replace with your image URL

    # Set your Azure credentials (or use environment variables)
    os.environ["AZURE_COMPUTER_VISION_KEY"] = "CGusoJxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxYeBjFXJ3w3AAAFACOGSqir"
    os.environ["AZURE_COMPUTER_VISION_ENDPOINT"] = "https://aemlab16apr.cognitiveservices.azure.com/"

    extracted_text = read_text_from_image(image_url)
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Failed to extract text")

==================
    1  apt-get update -y
    2  mkdir application
    3  cd application/
    4  ls -l
    5  pip install --upgrade azure-cognitiveservices-vision-computervision
    6  apt install python3-pip
    7  pip install --upgrade azure-cognitiveservices-vision-computervision
    8  apt install python3-venv -y
    9  python3 -m venv myenv
   10  source myenv/bin/activate
   11  pip install --upgrade pip
   12  pip install --upgrade az
   13  pip install --upgrade azure-cognitiveservices-vision-computervision
   14  ls -lrt
   15  touch ai-vision-ocr.py
   16  vi ai-vision-ocr.py 
   17  python ai-vision-ocr.py
   18  pip install pillow
   19  python ai-vision-ocr.py
   20  vi ai-vision-ocr.py 
   21  python ai-vision-ocr.py
==============================

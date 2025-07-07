import os
import openai
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# Configure Azure AI Foundry
AZURE_ENDPOINT = "https://YOUR_RESOURCE_NAME.openai.azure.com/"  # Replace with your endpoint
AZURE_KEY = "your-azure-api-key"  # Replace with your key
DEPLOYMENT_NAME = "dall-e-3-deployment"  # Replace with your deployment name
API_VERSION = "2023-06-01-preview"  # API version

# Configure OpenAI to use Azure
openai.api_type = "azure"
openai.api_base = AZURE_ENDPOINT
openai.api_version = API_VERSION
openai.api_key = AZURE_KEY

# Ensure upload folder exists
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        size = request.form.get('size', '1024x1024')
        quality = request.form.get('quality', 'standard')
        style = request.form.get('style', 'vivid')
        
        try:
            # Generate image using Azure DALL-E-3
            response = openai.Image.create(
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1,
                deployment_id=DEPLOYMENT_NAME
            )
            
            image_url = response['data'][0]['url']
            
            # Download and save the image
            # Note: Azure might return a URL that requires authentication
            # You might need additional code to handle the download
            
            return render_template('index.html', 
                                 image_url=image_url,
                                 prompt=prompt)
            
        except Exception as e:
            error = str(e)
            return render_template('index.html', error=error)
    
    return render_template('index.html')

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

import os
from openai import AzureOpenAI
from flask import Flask, render_template, request, send_from_directory
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Azure OpenAI configuration
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Ensure the output directory exists
os.makedirs("outputs", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        
        try:
            # Generate image using Azure OpenAI
            result = client.images.generate(
                model=DEPLOYMENT_NAME,
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            
            # Get the image URL
            image_url = result.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save the image
            image_filename = f"generated_{hash(prompt)}.png"
            image_path = os.path.join("outputs", image_filename)
            with open(image_path, "wb") as f:
                f.write(image_response.content)
                
            return render_template("index.html", image_path=image_filename, prompt=prompt)
            
        except Exception as e:
            error = f"Error generating image: {str(e)}"
            return render_template("index.html", error=error)
    
    return render_template("index.html")

@app.route("/outputs/<filename>")
def serve_image(filename):
    return send_from_directory("outputs", filename)

if __name__ == "__main__":
    app.run(debug=True)

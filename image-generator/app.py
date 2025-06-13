import os
import requests
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Azure AI Foundry configuration
AZURE_AI_FOUNDRY_ENDPOINT = "YOUR_AZURE_AI_FOUNDRY_ENDPOINT"
AZURE_AI_FOUNDRY_KEY = "YOUR_AZURE_AI_FOUNDRY_KEY"
DEPLOYMENT_NAME = "YOUR_DEPLOYMENT_NAME"  # The name of your deployed model in Azure AI Foundry

# Ensure the output directory exists
os.makedirs("outputs", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        
        try:
            # Call Azure AI Foundry image generation API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AZURE_AI_FOUNDRY_KEY}"
            }
            
            payload = {
                "prompt": prompt,
                "n": 1,  # Number of images to generate
                "size": "1024x1024"  # Image size
            }
            
            response = requests.post(
                f"{AZURE_AI_FOUNDRY_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/images/generations?api-version=2023-06-01-preview",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            
            # Get the image URL from the response
            result = response.json()
            image_url = result["data"][0]["url"]
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save the image
            image_path = os.path.join("outputs", "generated_image.png")
            with open(image_path, "wb") as f:
                f.write(image_response.content)
                
            return render_template("index.html", image_path=image_path, prompt=prompt)
            
        except Exception as e:
            error = f"Error generating image: {str(e)}"
            return render_template("index.html", error=error)
    
    return render_template("index.html")

@app.route("/outputs/<filename>")
def serve_image(filename):
    return send_from_directory("outputs", filename)

if __name__ == "__main__":
    app.run(debug=True)

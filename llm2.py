#LLM Text Classification and Sentiment Analysis
from openai import AzureOpenAI
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Static Azure OpenAI Configuration
AZURE_CONFIG = {
    "api_key": "your-azure-openai-key-here",  # Replace with your actual key
    "api_version": "2023-12-01-preview",
    "azure_endpoint": "https://your-resource-name.openai.azure.com/",  # Replace with your endpoint
    "deployment_name": "gpt-35-turbo"  # Replace with your deployment name
}

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_CONFIG["api_key"],
    api_version=AZURE_CONFIG["api_version"],
    azure_endpoint=AZURE_CONFIG["azure_endpoint"]
)

# Initialize FastAPI app
app = FastAPI(
    title="Azure OpenAI Text Analysis API",
    description="API for text classification and sentiment analysis using Azure OpenAI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TextInput(BaseModel):
    text: str
    categories: list[str] = None

class BatchInput(BaseModel):
    texts: list[str]
    categories: list[str] = None

class AnalysisResult(BaseModel):
    text: str
    classification: str
    sentiment: dict

class AnalysisResponse(BaseModel):
    results: list[AnalysisResult]

# Default categories
DEFAULT_CATEGORIES = ["Feedback", "Complaint", "Inquiry", "Spam", "Other"]

def classify_text(text: str, categories: list[str] = DEFAULT_CATEGORIES) -> str:
    """Classify text using Azure OpenAI"""
    try:
        prompt = f"""
        Classify the following text into one of these categories: {', '.join(categories)}.
        Return ONLY the category name, nothing else.
        
        Text: "{text}"
        """
        
        response = client.chat.completions.create(
            model=AZURE_CONFIG["deployment_name"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=20
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(500, f"Classification error: {str(e)}")

def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment using Azure OpenAI"""
    try:
        prompt = f"""
        Analyze the sentiment of the following text. 
        Return a JSON object with:
        - sentiment: 'positive', 'negative', or 'neutral'
        - confidence: score (0-1)
        - key_phrases: list of influential phrases
        
        Text: "{text}"
        """
        
        response = client.chat.completions.create(
            model=AZURE_CONFIG["deployment_name"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(500, f"Sentiment error: {str(e)}")

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text(text_input: TextInput):
    """Analyze single text"""
    try:
        categories = text_input.categories or DEFAULT_CATEGORIES
        return {
            "text": text_input.text,
            "classification": classify_text(text_input.text, categories),
            "sentiment": analyze_sentiment(text_input.text)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/analyze/batch", response_model=AnalysisResponse)
async def analyze_batch(batch_input: BatchInput):
    """Analyze multiple texts"""
    try:
        categories = batch_input.categories or DEFAULT_CATEGORIES
        results = []
        for text in batch_input.texts:
            time.sleep(0.5)  # Rate limiting
            results.append({
                "text": text,
                "classification": classify_text(text, categories),
                "sentiment": analyze_sentiment(text)
            })
        return {"results": results}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/categories")
async def get_categories():
    """Get default categories"""
    return {"categories": DEFAULT_CATEGORIES}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": AZURE_CONFIG["deployment_name"],
        "api_version": AZURE_CONFIG["api_version"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

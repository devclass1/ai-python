#LLM Text Classification and Sentiment Analysis
import openai
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_text(text, categories):
    """
    Classify text into predefined categories using LLM
    
    Args:
        text (str): The text to classify
        categories (list): List of possible categories
    
    Returns:
        str: The classified category
    """
    prompt = f"""
    Classify the following text into one of these categories: {', '.join(categories)}.
    Return ONLY the category name, nothing else.
    
    Text: "{text}"
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in classification: {e}")
        return "Error"

def analyze_sentiment(text):
    """
    Analyze sentiment of text using LLM
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: Dictionary containing sentiment analysis results
    """
    prompt = f"""
    Analyze the sentiment of the following text. 
    Return a JSON object with these fields:
    - sentiment: one of 'positive', 'negative', or 'neutral'
    - confidence: your confidence score (0-1)
    - key_phrases: list of phrases that influenced your decision
    
    Text: "{text}"
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse response"}
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {"error": str(e)}

def batch_analyze(texts, categories):
    """
    Analyze multiple texts at once for efficiency
    
    Args:
        texts (list): List of texts to analyze
        categories (list): List of classification categories
    
    Returns:
        list: List of analysis results for each text
    """
    results = []
    for text in texts:
        # Add delay to avoid rate limiting
        time.sleep(0.5)
        
        analysis = {
            "text": text,
            "classification": classify_text(text, categories),
            "sentiment": analyze_sentiment(text)
        }
        results.append(analysis)
    return results

def display_results(analysis):
    """
    Display analysis results in a readable format
    
    Args:
        analysis (dict or list): Analysis results to display
    """
    if isinstance(analysis, list):
        for i, result in enumerate(analysis, 1):
            print(f"\nAnalysis #{i}:")
            print(f"Text: {result['text']}")
            print(f"Classification: {result['classification']}")
            print("Sentiment Analysis:")
            print(f"  - Sentiment: {result['sentiment'].get('sentiment', 'N/A')}")
            print(f"  - Confidence: {result['sentiment'].get('confidence', 'N/A')}")
            print(f"  - Key Phrases: {', '.join(result['sentiment'].get('key_phrases', []))}")
    else:
        print(f"\nText: {analysis['text']}")
        print(f"Classification: {analysis['classification']}")
        print("Sentiment Analysis:")
        print(f"  - Sentiment: {analysis['sentiment'].get('sentiment', 'N/A')}")
        print(f"  - Confidence: {analysis['sentiment'].get('confidence', 'N/A')}")
        print(f"  - Key Phrases: {', '.join(analysis['sentiment'].get('key_phrases', []))}")
    print()

def main():
    print("LLM Text Classification and Sentiment Analysis Lab")
    print("Enter 'quit' to exit or 'batch' to enter batch mode\n")
    
    # Example categories for classification
    categories = ["Feedback", "Complaint", "Inquiry", "Spam", "Other"]
    
    while True:
        user_input = input("Enter some text to analyze: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'batch':
            print("\nBatch Mode - Enter multiple texts (one per line). Enter 'done' when finished.")
            texts = []
            while True:
                batch_input = input("> ").strip()
                if batch_input.lower() == 'done':
                    break
                if batch_input:
                    texts.append(batch_input)
            
            if texts:
                print("\nProcessing batch...")
                results = batch_analyze(texts, categories)
                display_results(results)
            continue
            
        # Single text analysis
        analysis = {
            "text": user_input,
            "classification": classify_text(user_input, categories),
            "sentiment": analyze_sentiment(user_input)
        }
        display_results(analysis)

if __name__ == "__main__":
    main()

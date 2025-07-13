from openai import AzureOpenAI
import json
import time

# Azure OpenAI Configuration - REPLACE THESE WITH YOUR ACTUAL VALUES
AZURE_CONFIG = {
    "api_key": "your-azure-openai-key-here",
    "api_version": "2023-12-01-preview",
    "azure_endpoint": "https://your-resource-name.openai.azure.com/",
    "deployment_name": "gpt-35-turbo"
}

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_CONFIG["api_key"],
    api_version=AZURE_CONFIG["api_version"],
    azure_endpoint=AZURE_CONFIG["azure_endpoint"]
)

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
        print(f"⚠️ Classification error: {str(e)}")
        return "Error"

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
        print(f"⚠️ Sentiment analysis error: {str(e)}")
        return {"error": str(e)}

def display_result(text: str, category: str, sentiment: dict):
    """Display analysis results in a user-friendly format"""
    print("\n📝 Analysis Results:")
    print(f"Text: {text}")
    print(f"🔖 Classification: {category}")
    
    print("\n😊 Sentiment Analysis:")
    print(f"  - Mood: {sentiment.get('sentiment', 'N/A').title()}")
    print(f"  - Confidence: {sentiment.get('confidence', 'N/A')}")
    print(f"  - Key Phrases: {', '.join(sentiment.get('key_phrases', []))}")
    print("-" * 50)

def main():
    print("""
    🚀 Azure OpenAI Text Analysis Console
    ------------------------------------
    Commands:
    - Enter text to analyze
    - 'categories' - Show/modify categories
    - 'batch' - Enter batch mode
    - 'quit' - Exit the program
    """)
    
    current_categories = DEFAULT_CATEGORIES.copy()
    
    while True:
        user_input = input("\n📩 Enter text or command: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
            
        elif user_input.lower() == 'categories':
            print("\n📂 Current categories:")
            for i, cat in enumerate(current_categories, 1):
                print(f"{i}. {cat}")
                
            action = input("\n[A]dd, [R]emove, [C]lear, [K]eep? ").lower()
            
            if action == 'a':
                new_cat = input("Enter new category name: ").strip()
                if new_cat:
                    current_categories.append(new_cat)
                    print(f"✅ Added '{new_cat}'")
                    
            elif action == 'r':
                try:
                    remove_idx = int(input("Enter number to remove: ")) - 1
                    if 0 <= remove_idx < len(current_categories):
                        removed = current_categories.pop(remove_idx)
                        print(f"✅ Removed '{removed}'")
                except ValueError:
                    print("⚠️ Please enter a valid number")
                    
            elif action == 'c':
                current_categories.clear()
                print("✅ Cleared all categories")
                
            continue
            
        elif user_input.lower() == 'batch':
            print("\n📦 Batch Mode - Enter multiple texts (one per line). Enter 'done' when finished.")
            texts = []
            while True:
                batch_input = input("> ").strip()
                if batch_input.lower() == 'done':
                    break
                if batch_input:
                    texts.append(batch_input)
            
            if texts:
                print(f"\n🔍 Analyzing {len(texts)} texts...")
                for i, text in enumerate(texts, 1):
                    time.sleep(0.5)  # Rate limiting
                    category = classify_text(text, current_categories)
                    sentiment = analyze_sentiment(text)
                    
                    print(f"\n📄 Text {i}:")
                    display_result(text, category, sentiment)
            continue
            
        # Single text analysis
        category = classify_text(user_input, current_categories)
        sentiment = analyze_sentiment(user_input)
        display_result(user_input, category, sentiment)

if __name__ == "__main__":
    main()

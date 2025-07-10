import requests
import json
import os
from typing import Dict, Optional

class AzureAIFoundryAssistant:
    def __init__(self, endpoint: str, api_key: str):
        """
        Initialize the Azure AI Foundry assistant with endpoint and API key.
        
        Args:
            endpoint (str): The Azure AI Foundry endpoint URL
            api_key (str): The API key for authentication
        """
        self.endpoint = endpoint.rstrip('/')  # Remove trailing slash if present
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "api-key": self.api_key
        })
        
    def send_request(self, prompt: str, conversation_id: Optional[str] = None) -> Dict:
        """
        Send a request to the Azure AI Foundry endpoint.
        
        Args:
            prompt (str): The user's input prompt
            conversation_id (str, optional): Conversation ID for multi-turn conversations
            
        Returns:
            dict: The JSON response from the API
        """
        payload = {
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        try:
            response = self.session.post(
                f"{self.endpoint}/v1/completions",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Azure AI Foundry: {e}")
            return {"error": str(e)}
    
    def process_response(self, response: Dict) -> str:
        """
        Process the API response and extract the assistant's reply.
        
        Args:
            response (dict): The JSON response from the API
            
        Returns:
            str: The assistant's reply text
        """
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            return response.get("choices", [{}])[0].get("text", "No response text found")
        except (KeyError, IndexError) as e:
            return f"Error processing response: {str(e)}"
    
    def start_interactive_session(self):
        """
        Start an interactive session with the AI assistant.
        """
        print("Azure AI Foundry Assistant - Interactive Session")
        print("Type 'quit' or 'exit' to end the session.")
        print("-----------------------------------------------")
        
        conversation_id = None
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ('quit', 'exit'):
                print("Ending session. Goodbye!")
                break
                
            if not user_input:
                print("Please enter a message.")
                continue
                
            print("Assistant is thinking...")
            
            # Send request to Azure AI Foundry
            response = self.send_request(user_input, conversation_id)
            
            # Process the response
            assistant_reply = self.process_response(response)
            
            # Update conversation ID if provided in response
            conversation_id = response.get("conversation_id", conversation_id)
            
            print(f"Assistant: {assistant_reply}")
            print()  # Add blank line for readability


def main():
    # Configuration - replace with your actual endpoint and key
    ENDPOINT = "https://aemfoundry1007.cognitiveservices.azure.com/"
    API_KEY = "D4OysthTpxWVH4n3DZjuElGo7OqB9otIZj3C1XUs5FS65Vol8tYkJQQJ99BGACYeBjFXJ3w3AAAAACOGVdsI"
    
    # Initialize the assistant
    assistant = AzureAIFoundryAssistant(ENDPOINT, API_KEY)
    
    # Start interactive session
    assistant.start_interactive_session()


if __name__ == "__main__":
    main()

import requests
import json

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
        
    def send_request(self, prompt: str) -> dict:
        """
        Send a request to the Azure AI Foundry endpoint.
        
        Args:
            prompt (str): The user's input prompt
            
        Returns:
            dict: The JSON response from the API
        """
        # Azure AI Foundry typically uses this structure
        url = f"{self.endpoint}/api/v1/completion"
        
        payload = {
            "prompt": prompt,  # Note: Some services use "input" instead of "prompt"
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            print(f"Sending request to: {url}")  # Debugging
            print(f"Payload: {json.dumps(payload, indent=2)}")  # Debugging
            
            response = self.session.post(
                url,
                json=payload,
                timeout=30
            )
            
            print(f"Response status: {response.status_code}")  # Debugging
            print(f"Response headers: {response.headers}")  # Debugging
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Full error details: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            return {"error": str(e)}
    
    def process_response(self, response: dict) -> str:
        """
        Process the API response and extract the assistant's reply.
        """
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            # Try different response structures
            if "choices" in response:
                return response["choices"][0]["text"]
            elif "output" in response:
                return response["output"]
            elif "completion" in response:
                return response["completion"]
            else:
                return f"Unexpected response format: {json.dumps(response, indent=2)}"
        except (KeyError, IndexError, TypeError) as e:
            return f"Error processing response: {str(e)}\nFull response: {json.dumps(response, indent=2)}"
    
    def start_interactive_session(self):
        """Start an interactive session with the AI assistant."""
        print("Azure AI Foundry Assistant - Interactive Session")
        print("Type 'quit' or 'exit' to end the session.")
        print("-----------------------------------------------")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ('quit', 'exit'):
                print("Ending session. Goodbye!")
                break
                
            if not user_input:
                print("Please enter a message.")
                continue
                
            print("Assistant is thinking...")
            response = self.send_request(user_input)
            assistant_reply = self.process_response(response)
            print(f"Assistant: {assistant_reply}\n")


def main():
    # Configuration
    ENDPOINT = "https://aemfoundry1007.cognitiveservices.azure.com/"
    API_KEY = "D4OysthTpxWVH4n3DZjuElGo7OqB9otIZj3C1XUs5FS65Vol8tYkJQQJ99BGACYeBjFXJ3w3AAAAACOGVdsI"
    
    # Initialize the assistant
    assistant = AzureAIFoundryAssistant(ENDPOINT, API_KEY)
    
    # Start interactive session
    assistant.start_interactive_session()


if __name__ == "__main__":
    main()

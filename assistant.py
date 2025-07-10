import time
from openai import AzureOpenAI

class AzureAIAssistant:
    def __init__(self):
        # Initialize client with hardcoded values
        self.client = AzureOpenAI(
            azure_endpoint="https://aemfoundry1007.cognitiveservices.azure.com/",
            api_key="D4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxsI",
            api_version="2024-05-01-preview"
        )
        
        # Create assistant
        self.assistant = self.client.beta.assistants.create(
            model="gpt-4.1-mini",  # replace with your actual model deployment name
            instructions="You are a helpful AI assistant. Respond helpfully and concisely.",
            tools=[],
            tool_resources={},
            temperature=0.7,
            top_p=1
        )
        
        # Create thread for conversation
        self.thread = self.client.beta.threads.create()
    
    def process_message(self, user_input: str) -> str:
        """Send user input to assistant and return the response"""
        try:
            # Add user message to thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=user_input
            )
            
            # Start assistant run
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                # Get the latest assistant message
                for message in messages.data:
                    if message.role == 'assistant':
                        return message.content[0].text.value
                return "No response from assistant"
            elif run.status == 'requires_action':
                return "Assistant requires action (function calling not implemented)"
            else:
                return f"Assistant run ended with status: {run.status}"
                
        except Exception as e:
            return f"Error processing message: {str(e)}"
    
    def start_interactive_session(self):
        """Start the interactive chat session"""
        print("\nAzure AI Assistant - Interactive Session")
        print("Type 'quit' or 'exit' to end the session.")
        print("----------------------------------------\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ('quit', 'exit'):
                    print("\nEnding session. Goodbye!")
                    break
                    
                if not user_input:
                    print("Please enter a message.")
                    continue
                    
                print("Assistant is thinking...")
                response = self.process_message(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    try:
        print("Initializing Azure AI Assistant...")
        assistant = AzureAIAssistant()
        assistant.start_interactive_session()
    except Exception as e:
        print(f"Failed to initialize assistant: {str(e)}")

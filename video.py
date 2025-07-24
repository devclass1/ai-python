import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AzureAIVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv("AZURE_AI_FOUNDRY_API_KEY")
        self.endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def create_video(self, prompt):
        """Create a video from text prompt"""
        try:
            # Prepare the request payload
            payload = {
                "prompt": prompt,
                "parameters": {
                    "length": "medium",  # can be 'short', 'medium', 'long'
                    "style": "realistic",  # can be 'realistic', 'cartoon', 'anime', etc.
                    "resolution": "720p"  # can be '480p', '720p', '1080p'
                }
            }
            
            print("Sending request to Azure AI Foundry...")
            response = requests.post(
                f"{self.endpoint}/api/v1/video/generate",
                headers=self.headers,
                json=payload
            )
            
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            job_id = result.get("job_id")
            
            if not job_id:
                raise ValueError("No job ID returned from API")
                
            print(f"Video generation started. Job ID: {job_id}")
            print("Waiting for video to be generated...")
            
            # Poll for completion
            video_url = self._wait_for_completion(job_id)
            
            print(f"\nVideo generation complete!")
            print(f"Download URL: {video_url}")
            
            return video_url
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def _wait_for_completion(self, job_id, poll_interval=10, timeout=300):
        """Poll the API for job completion"""
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Video generation timed out")
                
            response = requests.get(
                f"{self.endpoint}/api/v1/video/status/{job_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                status_data = response.json()
                status = status_data.get("status")
                
                if status == "completed":
                    return status_data.get("video_url")
                elif status == "failed":
                    raise RuntimeError(f"Video generation failed: {status_data.get('error', 'Unknown error')}")
                # else continue waiting
                
            time.sleep(poll_interval)

def main():
    print("Azure AI Foundry Video Generator")
    print("--------------------------------")
    
    # Initialize the video generator
    video_gen = AzureAIVideoGenerator()
    
    while True:
        # Get user prompt
        prompt = input("\nEnter your video prompt (or 'quit' to exit): ").strip()
        
        if prompt.lower() in ['quit', 'exit']:
            print("Exiting...")
            break
            
        if not prompt:
            print("Please enter a valid prompt.")
            continue
            
        # Generate the video
        video_url = video_gen.create_video(prompt)
        
        if video_url:
            # Here you could add code to download the video
            print("\nWould you like to download the video? (y/n)")
            choice = input().lower()
            if choice == 'y':
                # Implement download logic here
                print("Download functionality would be implemented here.")
                
if __name__ == "__main__":
    main()

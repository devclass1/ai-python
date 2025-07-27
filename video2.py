import os
import requests
import json
import time

def generate_video_from_prompt():
    """
    This function takes a user prompt and generates a video using Azure OpenAI's video generation API.
    """
    # Get user input for the video prompt
    prompt = input("Enter your video prompt: ")
    n_seconds = input("Enter video duration in seconds (default: 5): ") or "5"
    height = input("Enter video height in pixels (default: 480): ") or "480"
    width = input("Enter video width in pixels (default: 854): ") or "854"
    
    # Set up API configuration (you can modify these or set as environment variables)
    endpoint = os.getenv("ENDPOINT_URL", "https://palas-mdlby2dt-eastus2.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "sora")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "<AZURE_OPENAI_API_KEY>")
    api_version = "preview"
    
    # Construct the API URL
    path = 'openai/v1/video/generations/jobs'
    params = f'?api-version={api_version}'
    constructed_url = endpoint + path + params

    headers = {
        'Api-Key': subscription_key,
        'Content-Type': 'application/json',
    }

    body = {
        "prompt": prompt,
        "n_variants": "1",
        "n_seconds": n_seconds,
        "height": height,
        "width": width,
        "model": deployment,
    }

    print("\n🚀 Starting video generation...")
    job_response = requests.post(constructed_url, headers=headers, json=body)
    
    if not job_response.ok:
        print("❌ Video generation failed.")
        print(json.dumps(job_response.json(), sort_keys=True, indent=4, separators=(',', ': ')))
        return
    
    job_response = job_response.json()
    job_id = job_response.get("id")
    status = job_response.get("status")
    status_url = f"{endpoint}openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"

    print(f"\n⏳ Polling job status for ID: {job_id}")
    while status not in ["succeeded", "failed"]:
        time.sleep(5)
        job_response = requests.get(status_url, headers=headers).json()
        status = job_response.get("status")
        print(f"Current status: {status}")

    if status == "succeeded":
        generations = job_response.get("generations", [])
        if generations:
            print("\n✅ Video generation succeeded!")
            generation_id = generations[0].get("id")
            video_url = f'{endpoint}openai/v1/video/generations/{generation_id}/content/video{params}'
            
            # Download the video
            video_response = requests.get(video_url, headers=headers)
            if video_response.ok:
                output_filename = input("\nEnter output filename (default: output.mp4): ") or "output.mp4"
                if not output_filename.endswith('.mp4'):
                    output_filename += '.mp4'
                
                with open(output_filename, "wb") as file:
                    file.write(video_response.content)
                print(f'\n🎥 Generated video saved as "{output_filename}"')
            else:
                print("❌ Failed to download the generated video.")
        else:
            print("⚠️ Status is succeeded, but no generations were returned.")
    elif status == "failed":
        print("\n❌ Video generation failed.")
        print(json.dumps(job_response, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    print("Azure OpenAI Video Generation Tool")
    print("---------------------------------")
    generate_video_from_prompt()

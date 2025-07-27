import os
import requests
import json
import time
import webbrowser

def generate_video_from_prompt():
    """
    This function takes a user prompt and generates a video using Azure OpenAI's video generation API,
    then provides a download link for the generated video.
    """
    print("Azure OpenAI Video Generation Tool")
    print("---------------------------------")
    print("This tool will generate a video from your prompt and provide a download link.\n")
    
    # Get user input
    prompt = input("Enter your video prompt (e.g., 'Football match'): ").strip()
    if not prompt:
        print("❌ Error: Prompt cannot be empty.")
        return
    
    try:
        n_seconds = int(input("Enter video duration in seconds (2-10, default 5): ") or 5)
        height = int(input("Enter video height in pixels (default 480): ") or 480)
        width = int(input("Enter video width in pixels (default 854): ") or 854)
    except ValueError:
        print("❌ Error: Please enter valid numbers for duration and dimensions.")
        return

    # API configuration
    endpoint = os.getenv("ENDPOINT_URL", "https://palas-mdlby2dt-eastus2.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "sora")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
    
    if not subscription_key or subscription_key == "<AZURE_OPENAI_API_KEY>":
        print("❌ Error: Missing Azure OpenAI API key. Please set the AZURE_OPENAI_API_KEY environment variable.")
        return

    # Construct API URL
    api_version = "preview"
    constructed_url = f"{endpoint}openai/v1/video/generations/jobs?api-version={api_version}"

    headers = {
        'Api-Key': subscription_key,
        'Content-Type': 'application/json',
    }

    body = {
        "prompt": prompt,
        "n_variants": 1,
        "n_seconds": n_seconds,
        "height": height,
        "width": width,
        "model": deployment,
    }

    print("\n🚀 Starting video generation...")
    try:
        response = requests.post(constructed_url, headers=headers, json=body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making API request: {str(e)}")
        return

    job_data = response.json()
    job_id = job_data.get("id")
    status = job_data.get("status")
    
    if not job_id:
        print("❌ Error: No job ID received from API")
        return

    status_url = f"{endpoint}openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"
    
    print(f"\n⏳ Video generation job created. Job ID: {job_id}")
    print("Polling for completion (this may take several minutes)...")

    while status not in ["succeeded", "failed"]:
        time.sleep(10)  # Check every 10 seconds
        try:
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            job_data = status_response.json()
            status = job_data.get("status")
            print(f"Current status: {status}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error checking status: {str(e)}")
            time.sleep(5)
            continue

    if status == "succeeded":
        generations = job_data.get("generations", [])
        if generations:
            generation_id = generations[0].get("id")
            download_url = f"{endpoint}openai/v1/video/generations/{generation_id}/content/video?api-version={api_version}"
            
            print("\n✅ Video generation succeeded!")
            print(f"\n🔗 Download your video here: {download_url}")
            print("\nThe download link will expire after some time. Download soon!")
            
            # Option to open in browser
            if input("Open download link in browser now? (y/n): ").lower() == 'y':
                webbrowser.open(download_url)
        else:
            print("⚠️ Video generated but no download URL was provided.")
    else:
        print("\n❌ Video generation failed.")
        print("Error details:")
        print(json.dumps(job_data, indent=2))

if __name__ == "__main__":
    generate_video_from_prompt()

from azure.ai.vision import VisionServiceOptions, VisionSource, ImageAnalysisOptions, ImageAnalyzer
from azure.ai.vision.models import VisualFeatures
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
from io import BytesIO
import os

def analyze_image(image_url):
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        
        # Display the image
        img = mpimg.imread(image_data, format='JPG')
        plt.imshow(img)
        plt.axis('off')  # Hide axes
        plt.show()

        # Set up Azure Vision Service
        vision_key = os.environ["AZURE_VISION_KEY"]
        vision_endpoint = os.environ["AZURE_VISION_ENDPOINT"]

        service_options = VisionServiceOptions(vision_endpoint, vision_key)
        vision_source = VisionSource(url=image_url)
        analysis_options = ImageAnalysisOptions()

        analysis_options.features = (
            VisualFeatures.TAGS |
            VisualFeatures.OBJECTS |
            VisualFeatures.CAPTION |
            VisualFeatures.DENSE_CAPTIONS |
            VisualFeatures.TEXT |
            VisualFeatures.PEOPLE
        )

        analyzer = ImageAnalyzer(service_options, vision_source, analysis_options)
        result = analyzer.analyze()

        if result.reason == 0:  # 0 means success
            print("\nImage Analysis Results:")
            print("----------------------")
            
            if result.caption is not None:
                print(f"Caption: '{result.caption.content}' (Confidence: {result.caption.confidence:.2f})")
            
            if result.dense_captions is not None:
                print("\nDense Captions:")
                for caption in result.dense_captions:
                    print(f"- '{caption.content}' (Confidence: {caption.confidence:.2f})")
            
            if result.tags is not None:
                print("\nTags:")
                for tag in result.tags:
                    print(f"- '{tag.name}' (Confidence: {tag.confidence:.2f})")
            
            if result.objects is not None:
                print("\nObjects:")
                for obj in result.objects:
                    print(f"- '{obj.name}' (Confidence: {obj.confidence:.2f})")
            
            if result.text is not None:
                print("\nText:")
                for line in result.text.lines:
                    print(f"- '{line.content}'")
            
            if result.people is not None:
                print("\nPeople:")
                for person in result.people:
                    print(f"- Person detected at position {person.bounding_box}")

        else:
            print(f"Analysis failed. Error: {result.error.message}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Azure Computer Vision OCR Demo")
    print("-----------------------------")
    image_url = input("Please enter the URL of the image you want to analyze: ")
    analyze_image(image_url)

from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(username, prompt, n, size):
    # FIXED: Folder naming convention
    OUTPUT_DIR = username + "_" + "generated_images"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    response = client.images.generate(
        model="dall-e-3", # Ensure you use a valid model name
        prompt=prompt,
        n=n,
        size=size,
        response_format="b64_json" # REQUIRED to get data for local saving
    )

    image_files = []

    for i, img in enumerate(response.data):
        image_base64 = img.b64_json
        image_bytes = base64.b64decode(image_base64)
        file_name = f"image_{i+1}.png"
        file_path = os.path.join(OUTPUT_DIR, file_name)
        
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # Return full relative path for the frontend to append to the URL
        relative_path = os.path.join(OUTPUT_DIR, file_name)
        image_files.append(relative_path)

    return image_files
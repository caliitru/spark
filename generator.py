from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generate_image(username, prompt, n, size):
    OUTPUT_DIR = username + ' ' + "generated_images"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=n,
        size=size
    )

    image_files = []

    for i, img in enumerate(response.data):
        image_base64 = img.b64_json
        image_bytes = base64.b64decode(image_base64)
        file_path = os.path.join(OUTPUT_DIR, f"image_{i+1}.png")
        file_name = f"image_{i+1}.png"
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        image_files.append(file_name)

    return image_files


def generate_captions(prompt:str, n):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional social media content writer. "
                    "Follow the user's instructions exactly."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7, 
    )
    value = response.choices[0].message.content.strip()
    captions = [c.strip() for c in value.split("\n\n") if c.strip()]

    return captions[:n]



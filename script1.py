import os
import fal_client
import requests
from moviepy.editor import ImageSequenceClip
from datetime import datetime

# Set your fal.ai API key as an environment variable
os.environ['FAL_KEY'] = ""

# A list of prompts to generate images for
prompts = [
    "Setting: A barren desert landscape with scattered gold nuggets on the ground. Vibe: Mysterious and untouched. Lighting: Bright sunlight creating reflections off the gold pieces. Background: Early humans in simple clothing, discovering the gold for the first time, filled with awe and curiosity.",
    "Setting: An ancient Egyptian market, bustling with merchants. Vibe: Lively and trading-focused. Lighting: Soft, warm lighting, with torches and sunlight illuminating golden artifacts. Background: Traders showcasing gold jewelry, goblets, and coins, symbolizing the rise of gold as a valued trade commodity in early civilizations.",
    "Setting: Inside a lavish Egyptian tomb adorned with gold artifacts. Vibe: Opulent and reverent. Lighting: Dim, with beams of light illuminating golden statues and treasures. Background: Pharaohs' statues surrounded by golden amulets and treasures, representing the religious and royal significance of gold.",
    "Setting: An ancient Roman workshop with tools, molds, and raw gold. Vibe: Industrious and skilled craftsmanship. Lighting: Natural light streaming in through a window, highlighting artisans crafting gold coins and jewelry. Background: Roman craftsmen shaping gold into coins, demonstrating the commercialization and standardization of gold currency.",
    "Setting: A bustling trade route in the Mali Empire during its golden age. Vibe: Dynamic and wealth-driven. Lighting: Bright sunlight illuminating a caravan of camels carrying gold and traders bartering for silk and spices. Background: Mansa Musa's entourage transporting gold, showcasing one of history's wealthiest rulers and the influence of African gold trade.",
    "Setting: A medieval European castle treasury. Vibe: Secure and guarded. Lighting: Torch-lit ambiance, with reflections glimmering off piles of gold coins and artifacts. Background: Kings and nobility counting and inspecting gold coins, symbolizing the accumulation of wealth and the power gold represented in Europe.",
    "Setting: A Spanish galleon ship loaded with treasures from the New World. Vibe: Adventurous and colonial. Lighting: Sunlit decks, with the gold gleaming under the open sky. Background: Spanish sailors securing chests of gold, illustrating the period of conquests, gold plundering, and the economic impact on Europe.",
    "Setting: A 19th-century American riverbank during the California Gold Rush. Vibe: Hopeful and bustling with activity. Lighting: Daylight with a dusty, earthy tone from the digging and sifting for gold in the river. Background: Miners of various backgrounds panning for gold, representing the feverish search for wealth and the rapid societal changes of the Gold Rush.",
    "Setting: The New York Stock Exchange floor in the early 20th century. Vibe: Fast-paced and modernizing. Lighting: Bright, artificial light illuminating traders in suits. Background: Brokers trading gold stocks and futures, indicating the shift from physical gold trade to financial markets and investments.",
    "Setting: A futuristic vault, securely storing bars of refined gold. Vibe: Advanced and impenetrable. Lighting: Cool, artificial lighting highlighting the pure gold bars stacked neatly. Background: A robotic security system guarding the vault, symbolizing the current state and future of gold as a secure, valuable asset in modern economies."
]


# Set the folder path where images will be saved
output_folder_path = ""

# Make sure the output folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Function to create and save images from prompts
def generate_and_save_images(prompts, folder_path):
    images = []

    # Loop over each prompt and make a request
    for prompt in prompts:
        try:
            # Make the API request to generate an image
            handler = fal_client.submit(
                "fal-ai/flux/schnell",
                arguments={
                    "prompt": prompt,
                    "image_size": "portrait_16_9",
                    "num_inference_steps": 4,
                    "num_images": 1,
                    "enable_safety_checker": True
                }
            )

            # Retrieve the generated image URL
            result = handler.get()

            # Check if 'images' is in the result
            if 'images' in result and len(result['images']) > 0:
                image_info = result['images'][0]
                image_url = image_info['url']

                # Download and save the image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    # Create a valid filename based on the prompt
                    image_filename = f"{prompt[:50].replace(' ', '_').replace(':', '')}.jpg"
                    image_path = os.path.join(folder_path, image_filename)
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_response.content)

                    images.append(image_path)
                    print(f"Image saved at: {image_path}")
                else:
                    print(f"Failed to download image for prompt: {prompt}")
            else:
                print(f"No image generated for prompt: {prompt}")

        except Exception as e:
            print(f"An error occurred for prompt '{prompt}': {e}")

    return images

# Function to create a video from images
def create_video(images, output_video, image_duration=5):
    clip = ImageSequenceClip(images, durations=[image_duration] * len(images))
    clip.write_videofile(output_video, fps=24)

# Main function to generate images and create video
def main():
    # Generate timestamped directory for this session
    dir_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_output_folder = os.path.join(output_folder_path, dir_name)
    os.makedirs(full_output_folder, exist_ok=True)
    print(dir_name)

    # Generate images
    generated_images = generate_and_save_images(prompts, full_output_folder)

    # Create video from generated images
    output_video_path = os.path.join(full_output_folder, "output_video1.mp4")
    create_video(generated_images, output_video_path)

    print(f"Video created: {output_video_path}")

if __name__ == "__main__":
    main()

import json
import os
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from tqdm import tqdm

# Load Stable Diffusion 2 model
model_id = "stabilityai/stable-diffusion-2"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, scheduler=scheduler, torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# Parameters
n_steps = 50


def generate_images_from_json(json_path, output_folder):
    with open(json_path, "r") as file:
        data = json.load(file)

    captions = data["captions"]

    # Sort image paths
    sorted_image_paths = sorted(captions.keys())

    os.makedirs(output_folder, exist_ok=True)

    for img_path in tqdm(sorted_image_paths, desc="Generating images"):
        prompt = captions[img_path]

        # Generate image
        image = pipe(prompt=prompt, num_inference_steps=n_steps).images[0]

        # Prepare output path
        image_filename = os.path.basename(img_path)
        output_path = os.path.join(output_folder, image_filename)

        # Save the generated image
        image.save(output_path)


if __name__ == "__main__":
    json_path = "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/desiboys_captions/llama3.2-vision/output.json"
    output_folder = "generated_output/sd2/desiboys_captions/llama3.2-vision"
    generate_images_from_json(json_path, output_folder)

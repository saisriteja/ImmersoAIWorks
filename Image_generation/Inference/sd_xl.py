import json
import os
import torch
from diffusers import DiffusionPipeline
from tqdm import tqdm
from PIL import Image

# Load Stable Diffusion XL base and refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to("cuda")

refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to("cuda")

# Parameters
n_steps = 40
high_noise_frac = 0.8


def generate_images_from_json(json_path, output_folder):
    with open(json_path, "r") as file:
        data = json.load(file)

    captions = data["captions"]

    # Sort image paths
    sorted_image_paths = sorted(captions.keys())

    os.makedirs(output_folder, exist_ok=True)

    for img_path in tqdm(sorted_image_paths, desc="Generating images"):
        prompt = captions[img_path]

        # Run base
        latent_image = base(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
        ).images

        # Run refiner
        final_image = refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=latent_image,
        ).images[0]

        # Prepare output path
        image_filename = os.path.basename(img_path)
        output_path = os.path.join(output_folder, image_filename)

        # Save the final image
        final_image.save(output_path)


if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description="Generate images from JSON prompts.")
    # parser.add_argument(
    #     "--json_path", type=str, required=True, help="Path to input JSON file."
    # )
    # parser.add_argument(
    #     "--output_folder",
    #     type=str,
    #     required=True,
    #     help="Folder to save generated images.",
    # )

    # args = parser.parse_args()

    # generate_images_from_json(args.json_path, args.output_folder)

    json_path = "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/desiboys_captions/llama3.2-vision/output.json"
    output_folder = "generated_output/sdxl/desiboys_captions/llama3.2-vision"
    generate_images_from_json(json_path, output_folder)

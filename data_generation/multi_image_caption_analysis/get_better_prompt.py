import json
from typing import Dict, List
from pydantic import BaseModel, ValidationError
from ollama import chat
import os
from tqdm import tqdm


class ImageComparison(BaseModel):
    """
    Pydantic model to structure the comparison results
    with common and different caption elements.
    """

    image: str
    common: Dict[str, List[str]]
    different: Dict[str, List[str]]


class CaptionComparator:
    """
    A flexible class to compare image captions across multiple models.
    """

    def __init__(self, model_name: str, json_paths: List[str]):
        """
        Initialize the comparator with model name and JSON file paths.

        :param model_name: Name of the LLM to use for comparison
        :param json_paths: List of paths to JSON files containing captions
        """
        self.model_name = model_name
        self.json_paths = json_paths
        self.captions_by_model = {}

        # Automatically extract model names from file paths
        self.model_names = [
            os.path.basename(os.path.dirname(path)) for path in json_paths
        ]

        # Load captions for each model
        self._load_captions()

    def _load_captions(self):
        """
        Load captions from JSON files and organize them by model.
        """
        for path, model_name in zip(self.json_paths, self.model_names):
            with open(path, "r") as f:
                data = json.load(f)
                self.captions_by_model[model_name] = data.get("captions", {})

    def _prepare_input_for_llm(self, image_path: str, captions: Dict[str, str]) -> str:
        """
        Prepare a structured prompt for LLM comparison.

        :param image_path: Path to the image
        :param captions: Dictionary of model names to their captions
        :return: Formatted prompt string
        """
        prompt = f"Compare the captions for the image: {image_path}\n"

        for model, caption in captions.items():
            prompt += f"Model ({model}): {caption}\n"

        prompt += """
        Return the common and different aspects in the following format:
        {
          "common": {
            "scene": ["<list of common elements>"],
            "details": ["<list of common elements>"]
          },
          "different": {
            "details": [
              "Model 1: <caption>",
              "Model 2: <caption>",
              ...
            ]
          }
        }
        """
        return prompt

    def analyze_image_captions(self) -> List[ImageComparison]:
        """
        Analyze captions for all common images across models.

        :return: List of ImageComparison results
        """
        # Find common image paths across all models
        common_images = list(
            set.intersection(
                *[set(captions.keys()) for captions in self.captions_by_model.values()]
            )
        )

        results = []
        # Use tqdm for progress tracking
        for image_path in tqdm(
            common_images, desc="Analyzing Image Captions", unit="image"
        ):
            # Collect captions for this image across all models
            image_captions = {
                model: self.captions_by_model[model].get(image_path, "")
                for model in self.model_names
            }

            # Prepare prompt for LLM
            prompt = self._prepare_input_for_llm(image_path, image_captions)

            try:
                # Get LLM response
                response = chat(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    format=ImageComparison.model_json_schema(),
                )

                # Parse and validate the response
                result = ImageComparison.model_validate_json(
                    response["message"]["content"]
                )
                result.image = image_path
                results.append(result)

            except (ValidationError, KeyError) as e:
                print(f"Error processing image {image_path}: {e}")

        return results


# Example usage
def main(json_paths: List[str], json_output_path: str, model_name: str):
    comparator = CaptionComparator(model_name=model_name, json_paths=json_paths)

    results = comparator.analyze_image_captions()

    # Print or process results
    for result in results:
        print(result.model_dump_json(indent=2))

    json_results = [result.dict() for result in results]
    with open(json_output_path, "w") as f:
        json.dump(json_results, f, indent=2)


if __name__ == "__main__":
    json_paths = [
        "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/generated_captions/blip/output.json",
        "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/generated_captions/llama3.2-vision/output.json",
        "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/generated_captions/llava/output.json",
        "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/generated_captions/llava-llama3/output.json",
    ]

    model_name = "llama3.2"
    json_output_path = "image_caption_comparision.json"
    main(json_paths, json_output_path, model_name)

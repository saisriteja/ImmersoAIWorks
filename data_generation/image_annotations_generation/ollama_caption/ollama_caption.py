from PIL import Image

import ollama


class ImageCaptioningModel:
    def __init__(self, model_name: str, device: str = "cuda"):
        """
        Initialize the image captioning model and processor.
        :param model_name: The name of the model to use (e.g., "Salesforce/blip-image-captioning-base").
        :param device: The device to run the model on ("cuda" or "cpu").
        """

        self.model_name = model_name

    def generate_caption(self, image_path: str):
        """_summary_

        Args:
            image_path (str): image path

        Returns:
            dict: caption data
        """
        if self.model_name == "llava:7b":

            res = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": "Describe this image:",
                        "images": [
                            "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/sample_images/312.jpg"
                        ],
                    }
                ],
            )

            data = {
                "image_path": image_path,
                "caption": res["message"]["content"],
            }

            return data

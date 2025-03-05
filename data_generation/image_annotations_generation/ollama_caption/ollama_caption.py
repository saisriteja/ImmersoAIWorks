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

    def generate_caption(self, image_path: str, content: str = "Describe this image:"):
        """Generate a caption for the given image.

        Args:
            image_path (str): Image path.
            content (str): The content/message to send to the model for image description.
                           Defaults to "Describe this image:".

        Returns:
            dict: Caption data with image path and caption text.
        """
        # Define the chat request structure with the dynamic content
        message = {
            "role": "user",
            "content": content,
            "images": [image_path],
        }

        # Perform the request to the ollama API
        res = ollama.chat(model=self.model_name, messages=[message])

        # Extract and return the caption along with the image path
        return {
            "image_path": image_path,
            "caption": res.get("message", {}).get("content", "No caption available"),
        }

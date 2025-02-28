from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor


class ImageCaptioningModel:
    def __init__(self, model_name: str, device: str = "cuda"):
        """
        Initialize the image captioning model and processor.
        :param model_name: The name of the model to use (e.g., "Salesforce/blip-image-captioning-base").
        :param device: The device to run the model on ("cuda" or "cpu").
        """
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
        self.device = device

    def generate_caption(self, image_path: str):
        """
        Generate captions for an image (both conditional and unconditional).
        :param image_path: The path to the image to be captioned.
        :return: A tuple of (conditional_caption, unconditional_caption).
        """
        # Open the image
        raw_image = Image.open(image_path).convert("RGB")

        # Conditional captioning
        text = "a photography of"
        inputs = self.processor(raw_image, text, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        caption_conditional = self.processor.decode(out[0], skip_special_tokens=True)

        # Unconditional captioning
        inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs)
        caption_unconditional = self.processor.decode(out[0], skip_special_tokens=True)

        data = {
            "image_path": image_path,
            "caption": caption_conditional,
            "unconditional_caption": caption_unconditional,
        }

        return data

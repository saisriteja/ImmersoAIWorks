import json
import os
import time

import toml
from logzero import logger


class CaptioningPipeline:
    def __init__(self, config_path: str):
        """
        Initialize the captioning pipeline, loading configuration and model(s).
        :param config_path: Path to the TOML configuration file.
        """
        self.config = toml.load(config_path)
        self.dataset_path = self.config["DatasetInfo"]["dataset_path"]
        self.output_path = self.config["MetaData"]["outputpath"]
        self.model_name = self.config["ModelInfo"]["modelname"]

        # generate the outputpath
        logger.info(f"Creating output directory at {self.output_path}")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # Initialize the model(s)
        if self.model_name == "Salesforce/blip-image-captioning-base":
            from blip_caption.blip_caption import ImageCaptioningModel

            self.model = ImageCaptioningModel(self.model_name)
        else:
            logger.error(f"Model {self.model_name} not supported.")
            return

    def get_all_images(self):
        """
        Get a list of all image file paths from the dataset folder.
        :return: List of image paths.
        """
        image_paths = []
        for filename in os.listdir(self.dataset_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                image_paths.append(os.path.join(self.dataset_path, filename))
        return image_paths

    def process_images(self):
        """
        Process all images, generating captions for each and collecting metadata.
        """
        start_time = time.time()
        captions = {}
        total_images = 0
        image_paths = self.get_all_images()

        for img_path in image_paths:
            total_images += 1
            caption_conditional = self.model.generate_caption(img_path)["caption"]
            captions[img_path] = (
                caption_conditional  # You can change this to unconditional if preferred.
            )

        time_taken = round(time.time() - start_time, 2)
        # convert to mins
        time_taken = round(time_taken / 60, 2)

        # Prepare metadata
        metadata = {
            "model_name": self.model_name,
            "time_taken": time_taken,
            "total_no_of_images": total_images,
        }

        self.write_to_json(captions, metadata)

    def write_to_json(self, captions, metadata):
        """
        Write the generated captions and metadata to a JSON file.
        :param captions: Dictionary of image paths and their corresponding captions.
        :param metadata: Metadata dictionary containing model name, time taken, etc.
        """
        output_data = {"metadata": metadata, "captions": captions}

        with open(self.output_path, "w") as json_file:
            json.dump(output_data, json_file, indent=4)

        print(
            f"Finished processing {metadata['total_no_of_images']} images. Output saved to {self.output_path}."
        )


# Main function to run the pipeline
def main():
    config_path = "config.toml"
    pipeline = CaptioningPipeline(config_path)
    pipeline.process_images()


if __name__ == "__main__":
    main()

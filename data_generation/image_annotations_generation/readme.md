Certainly! To place the "Steps to Add a New Model for Captioning" under a toggle bar, you can format it using Markdown in a way that is compatible with platforms that support such interactive elements. However, note that standard Markdown does not natively support toggle bars or collapsible sections. That functionality can be achieved using HTML elements, or in certain platforms like GitHub, you may use a collapsible section syntax.

Here's how you can structure it with a toggle bar using HTML within the Markdown:

````markdown
# Image Captioning Project

This project generates captions for images using pre-trained models. The configuration for the environment and model is specified in a `config.toml` file, and the script uses the specified model for captioning the images.

## Input

### Config File

Before running the project, make sure your `config.toml` file is properly set up. The `config.toml` file specifies:

- The name of the conda environment.
- The dataset directory containing all the images.
- The model to use for captioning.
- The output path for the generated captions.

Here’s an example of the `config.toml` file:

```toml
conda_env_name = 'generic'

[DatasetInfo]
dataset_path  = 'sample_images'

[ModelInfo]
modelname = "Salesforce/blip-image-captioning-base"

[MetaData]
outputpath = 'generated_captions/blip/output.json'
```
````

### Explanation:

- `conda_env_name`: The name of the conda environment that should be activated before running the script.
- `dataset_path`: The root directory for all the images you want to process.
- `modelname`: The model you want to use for captioning (e.g., `Salesforce/blip-image-captioning-base`).
- `outputpath`: The path where the generated captions will be saved (e.g., `'generated_captions/blip/output.json'`).

---

## Running the Project

To run the project, follow these steps:

1. **Make sure your conda environment is set up correctly.**
   Ensure that your conda environment contains all the necessary packages for running the script (e.g., PyTorch, transformers, etc.).

2. **Activate the Conda Environment**:
   The conda environment specified in the `config.toml` file will be automatically activated using the `run.sh` script.

3. **Run the `run.sh` Script**:
   This script will activate the environment and run the main Python script for captioning.

   Example:

   ```bash
   ./run.sh
   ```

---

## Output

The output will be a JSON file with the following structure:

```json
{
  "metadata": {
    "model_name": "Your Model Name",
    "time_taken": "Time Taken to Process (in seconds)",
    "total_no_of_images": "Total Number of Images Processed"
  },
  "captions": {
    "framepath1": "Caption for frame 1",
    "framepath2": "Caption for frame 2",
    "framepath3": "Caption for frame 3",
    ...
  }
}
```

### Explanation:

1. **metadata**:

   - **modelname**: The name of the model used for generating captions.
   - **timetaken**: The time taken to process the images and generate the captions.
   - **totalnoofimages**: The total number of images that were processed in the input folder.

2. **captions**:
   - The keys in this section represent the file paths of the images (e.g., `framepath1` refers to the first image's path).
   - The values are the corresponding captions generated for each image.

## Example

Input:

- Image Folder: `./images`
- Output JSON Path: `./output/annotations.json`

Sample output:

```json
{
  "metadata": {
    "model_name": "ImageCaptioningV2",
    "time_taken": "12.5",
    "total_no_of_images": 5
  },
  "captions": {
    "./images/image1.jpg": "A group of people at a park",
    "./images/image2.jpg": "A dog running on the beach",
    "./images/image3.jpg": "A man standing by a mountain",
    "./images/image4.jpg": "A close-up of a flower",
    "./images/image5.jpg": "A sunset over the ocean"
  }
}
```

---

## How to Use

1. **Prepare Your Environment**:

   - Ensure you have the necessary libraries installed (e.g., Python libraries for image processing and model inference).

2. **Run the Script**:

   - Pass the path to the image folder and the desired output path for the JSON file as arguments.
   - The script will process all the images in the provided folder and generate captions for each one.

3. **View the Output**:
   - The generated JSON file will contain metadata and captions for each image, which can be used for further analysis or storage.

## Requirements

- Python 3.x
- Required dependencies (e.g., image processing libraries, deep learning models for captioning)

---

<details>
<summary><h2><strong>Steps to Add a New Model for Captioning</strong></h2></summary>

To add a new model for image captioning, follow these steps:

### 1. Folder Structure

For naming convention, create a folder with the model name and append `_caption` to it. For example:

- `blip_caption/blip_caption.py`

### 2. Implement the Image Captioning Class

Inside the model folder (e.g., `blip_caption`), create a Python file (`blip_caption.py`) and define the `ImageCaptioningModel` class.

```python
class ImageCaptioningModel:
    def __init__(self, model_name: str, device: str = "cuda"):
        # Initialize all necessary variables (model loading, processor, etc.)
        pass

    def generate_caption(self, image_path: str):
        # Implement the inference logic to generate captions
        pass
```

- `__init__`: Initialize necessary variables, such as loading the model, setting the device (`cuda` or `cpu`), and any other configurations.
- `generate_caption`: Implement the inference logic that will process the input image and generate a caption.

### 3. Import the New Model in `main.py`

In your main script, you’ll need to import the new model class and initialize it based on the model name specified in the `config.toml` file.

Example snippet for `main.py`:

```python
# Initialize the model(s)
if self.model_name == "Salesforce/blip-image-captioning-base":
    from blip_caption.blip_caption import ImageCaptioningModel
    self.model = ImageCaptioningModel(self.model_name)
else:
    logger.error(f"Model {self.model_name} not supported.")
    return
```

This code checks the model name and imports the corresponding class for captioning. If the model is not supported, it logs an error.

### 4. Run the Inference

After adding the new model and modifying the code, you can run the inference by executing the `run.sh` script.

</details>

### Requirements for Models

1. Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
```

2. Kill running ollama process

```
sudo systemctl stop ollama
```

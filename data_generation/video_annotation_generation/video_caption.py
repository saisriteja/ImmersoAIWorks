import json
from ollama import chat, ChatResponse


class VideoSummaryGenerator:
    def __init__(self, json_file_path, final_prompt, model_name="llama3.2"):
        # Initialize with the input file path, final prompt, and model name
        self.json_file_path = json_file_path
        self.final_prompt = final_prompt
        self.model_name = model_name
        self.captions = {}
        self.sorted_captions = {}
        self.llm_prompt = ""

    def read_json(self):
        """Reads and parses the JSON file."""
        try:
            with open(self.json_file_path, "r") as file:
                data = json.load(file)
            self.captions = data.get("captions", {})
        except FileNotFoundError:
            print(f"Error: File not found at {self.json_file_path}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

    def sort_captions(self):
        """Sorts the captions by image names."""
        self.sorted_captions = {k: v for k, v in sorted(self.captions.items())}

    def generate_context(self):
        """Generates the context for each image."""
        prompt = ""
        for image_name, caption in self.sorted_captions.items():
            prompt += (
                f"Frame {image_name.split('/')[-1].split('.')[0]} context: {caption}\n"
            )
        return prompt

    def create_llm_prompt(self):
        """Creates the full prompt for the LLM."""
        init_prompt = """The task is to generate a concise 3-line summary of a video based on individual still frames. Each frame may include characters, settings, and visual cues that convey specific emotional tones, actions, or themes which should be considered in the summary. Your goal is to connect the key visual elements, including the character’s expressions, actions, attire, and the atmosphere of the environment, to create an engaging, cohesive summary that reflects the emotional or narrative progression of the video.

                    The following frames represent moments from a video, which conveys a contemplative, emotionally intense atmosphere. These images suggest themes of introspection, spirituality, or ritual, possibly in a historical or ceremonial setting. The descriptions below provide key context that should help you understand the setting, character emotions, and the visual tone of the video.
                    """
        context = self.generate_context()
        llm_prompt = init_prompt + context + self.final_prompt
        self.llm_prompt = llm_prompt

    def get_video_summary(self):
        """Interacts with the LLM to get the summary."""
        if not self.llm_prompt:
            self.create_llm_prompt()

        response: ChatResponse = chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": self.llm_prompt},
            ],
        )

        return response["message"]["content"]

    def get_sorted_captions(self):
        """Returns the sorted captions as a dictionary."""
        return self.sorted_captions


def main(json_file_path, final_prompt):
    video_summary_generator = VideoSummaryGenerator(json_file_path, final_prompt)

    # Read and process the JSON file
    video_summary_generator.read_json()
    video_summary_generator.sort_captions()

    # Get the sorted captions (as dictionary)
    sorted_captions = video_summary_generator.get_sorted_captions()
    # print("Sorted Captions:", sorted_captions)

    # Get the video summary
    summary = video_summary_generator.get_video_summary()
    print("Video Summary:", summary)


if __name__ == "__main__":

    # Example usage:
    json_file_path = "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation/generated_captions/llava/output.json"
    final_prompt = """Provide a concise 6-line summary of the above context. The summary should capture the overall emotional or narrative arc of the video, connecting the themes, character emotions, and atmosphere across the frames. Do not mention any specific frame number or describe individual frames, just the overall essence of the sequence."""
    main(json_file_path, final_prompt)

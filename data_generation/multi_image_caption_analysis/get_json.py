import os

json_files = []

path = "/media/hp/c587a0ea-5c63-499c-a609-e5e5362a9766/data/ImmersoAIWorks/data_generation/image_annotations_generation"


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            json_files.append(os.path.join(root, file))

print(json_files)

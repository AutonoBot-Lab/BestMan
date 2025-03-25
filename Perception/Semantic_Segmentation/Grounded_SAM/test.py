from PIL import Image
from Utils import Submodule

proxy_url = '127.0.0.1:7897'
detect_threshold = 0.3
detector_id = "IDEA-Research/grounding-dino-tiny"
segmenter_id = "facebook/sam-vit-base"
image = Image.open("./test_data/cat.jpg")
labels = ["a cat.", "a remote control."]
save_name = "./output/cute_cat.png"

grounded_sam = Submodule()
input_data = {
    "proxy_url": proxy_url,
    "detect_threshold":detect_threshold,
    "detector_id": detector_id,
    "segmenter_id": segmenter_id,
    "image": image,
    "labels": labels,
    "save_name": save_name
}
output = grounded_sam.call(input_data, "grounded_sam", "Perception/Semantic_Segmentation/Grounded_SAM/Grounded_SAM.py")
image_array, detection = output["image_array"], output["detection"]
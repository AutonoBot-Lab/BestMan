from PIL import Image
from Utils import Submodule

lang_sam = Submodule()
input_data = {
    "proxy_url": "127.0.0.1:7897",
    "input_img": Image.open(f"./test_image/test_rgb.jpg"),
    "query": "yellow cup",
    "box_filename": "./output/box.png",
    "mask_filename": "./output/mask.png"
}
results = lang_sam.call(
    input_data, "lang-segment-anything", "Perception/Semantic_Segmentation/Lang_SAM/Lang_SAM.py"
)
print(results)
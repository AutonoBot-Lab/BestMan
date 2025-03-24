import requests
from PIL import Image
from Utils import Submodule

proxy_url = '127.0.0.1:7897'
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
response = requests.get(url, stream=True)
image = Image.open(response.raw).convert("RGB")
text_labels = [["a photo of a cat", "a photo of a dog"]]
owl_vit = Submodule()
input_data = {
    "proxy_url": proxy_url,
    "image": image,
    "text_labels": text_labels
}
results = owl_vit.call(input_data, "owl_vit", "Perception/Object_Detector/OWL_ViT/OWL_ViT.py")
for res in results["results"]:
    print(f"Detected {res['label']} with confidence {res['score']} at location {res['box']}")
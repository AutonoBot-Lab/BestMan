import requests
from PIL import Image
from Utils import Submodule

proxy_url = '127.0.0.1:7897'
# single image with single text query
# images = [Image.open("./test_data/cat.jpg").convert("RGB")]
# text_queries = [["a photo of a cat", "a photo of a dog"]]

# multiple image with multiple text queries
images = [Image.open("./test_data/astronaut.png").convert("RGB"), Image.open("./test_data/coffee.png").convert("RGB")]
text_queries = text_queries = [["human face", "rocket", "nasa badge", "star-spangled banner"], ["coffee mug", "spoon", "plate"]]

owl_vit = Submodule()
input_data = {
    "proxy_url": proxy_url,
    "images": images,
    "text_queries": text_queries
}
output = owl_vit.call(input_data, "owl_vit", "Perception/Object_Detector/OWL_ViT/OWL_ViT.py")
results = output["results"]

# print results
for i in range(len(results)):
    print(f"\nimage {i}")
    text = text_queries[i]
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]

    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        print(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")
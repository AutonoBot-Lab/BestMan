from PIL import Image, ImageDraw, ImageFont
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection
import os
import requests
import matplotlib.pyplot as plt

class OWL_ViT:
    def __init__(self, model_name="google/owlvit-base-patch32", proxy_url=None):
        """
        Initialize the OWL_ViT class and load the model and processor.

        :param model_name: Model name, default is "google/owlvit-base-patch32"
        :param proxy_url: Proxy URL for downloading the pretrained model
        """
        if proxy_url:
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url

        self.processor = OwlViTProcessor.from_pretrained(model_name)
        self.model = OwlViTForObjectDetection.from_pretrained(model_name)

    def predict(self, image, text_labels, threshold=0.1):
        """
        Perform prediction on the input image and return a list of detection results.

        :param image: Input image (PIL.Image.Image object)
        :param text_labels: List of text labels (e.g., [["a photo of a cat", "a photo of a dog"]])
        :param threshold: Confidence threshold, default is 0.1
        :return: List of detection results, each element contains 'label', 'score', 'box'
        """
        # Process the input
        inputs = self.processor(text=text_labels, images=image, return_tensors="pt")

        # Run inference
        outputs = self.model(**inputs)

        # Target size
        target_sizes = torch.tensor([(image.height, image.width)])

        # Post-process the outputs
        results = self.processor.post_process_grounded_object_detection(
            outputs=outputs, target_sizes=target_sizes, threshold=threshold, text_labels=text_labels
        )
        result = results[0]

        # Format the output
        formatted_results = []
        for box, score, label in zip(result["boxes"], result["scores"], result["text_labels"]):
            box = [round(i, 2) for i in box.tolist()]
            formatted_results.append({
                "label": label,
                "score": round(score.item(), 3),
                "box": box
            })

        return formatted_results

    def visualize(self, image, results):
        """
        Visualize the detection results.

        :param image: Input image (PIL.Image.Image object)
        :param results: List of detection results, format [{'label': ..., 'score': ..., 'box': ...}]
        """
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()  # Default font

        for res in results:
            box = [int(i) for i in res["box"]]  # Convert to integer coordinates
            label = res["label"]
            score = res["score"]
            draw.rectangle(box, outline="red", width=2)  # Draw bounding box
            caption = f"{label} ({score:.2f})"  # Caption text
            draw.text((box[0], box[1]), caption, fill="red", font=font)  # Add text to the box

        # Display the image
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.axis("off")  # Turn off axes
        plt.show()


if __name__ == "__main__":
    
    proxy_url = '127.0.0.1:7897'
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    response = requests.get(url, stream=True)
    image = Image.open(response.raw).convert("RGB")
    text_labels = [["a photo of a cat", "a photo of a dog"]]

    # Initialize the OWL_ViT class
    owl_vit = OWL_ViT(proxy_url=proxy_url)

    # Perform prediction
    results = owl_vit.predict(image, text_labels)

    # Print detection results
    for res in results:
        print(f"Detected {res['label']} with confidence {res['score']} at location {res['box']}")
    
    # Visualize results
    owl_vit.visualize(image, results)

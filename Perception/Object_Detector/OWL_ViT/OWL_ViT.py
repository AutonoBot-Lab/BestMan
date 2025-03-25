import os
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from PIL import ImageDraw, ImageFont
from matplotlib import pyplot as plt
from Utils import serialize, deserialize

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

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = OwlViTProcessor.from_pretrained(model_name)
        self.model = OwlViTForObjectDetection.from_pretrained(model_name)

    def predict(self, images, text_queries, threshold=0.1):
        """
        Perform prediction on the input images and return a list of detection results.

        :param images: Input images
        :param text_queries: List of text queries (e.g., [["a photo of a cat", "a photo of a dog"]])
        :param threshold: Confidence threshold, default is 0.1
        :return: List of detection results, each element contains 'label', 'score', 'box'
        """
        # Process image and text inputs
        inputs = self.processor(text=text_queries, images=images, return_tensors="pt").to(self.device)

        # Print input names and shapes
        # for key, val in inputs.items():
        #     print(f"{key}: {val.shape}")
        
        # Set model in evaluation mode
        self.model.to(self.device)
        self.model.eval()

        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Print output names and shapes
        # for k, val in outputs.items():
        #     if k not in {"text_model_output", "vision_model_output"}:
        #         print(f"{k}: shape of {val.shape}")
        
        # print("\nText model outputs")
        # for k, val in outputs.text_model_output.items():
        #     print(f"{k}: shape of {val.shape}")

        # print("\nVision model outputs")
        # for k, val in outputs.vision_model_output.items():
        #     print(f"{k}: shape of {val.shape}") 

        # Target image sizes (height, width) to rescale box predictions [batch_size, 2]
        target_sizes = torch.Tensor([img.size[::-1] for img in images]).to(self.device)

        # Post-process the outputs
        results = self.processor.post_process_grounded_object_detection(
            outputs=outputs, target_sizes=target_sizes, threshold=threshold, text_labels=text_queries
        )
        
        return results
        
    def visualize(self, images, results):
        """
        Visualize the detection results.

        :param image: Input image (PIL.Image.Image object)
        :param results: List of detection results, format [{'label': ..., 'score': ..., 'box': ...}]
        """
        # Loop over predictions for each image in the batch
        for image, result in zip(images, results):
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()  # Default font
            
            for box, score, label in zip(result["boxes"], result["scores"], result["text_labels"]):
                box = [round(i, 2) for i in box.tolist()]
                draw.rectangle(box, outline="red", width=2)  # Draw bounding box
                score = round(score.item(), 3)
                caption = f"{label} ({score:.2f})"  # Caption text
                draw.text((box[0], box[1] - 10), caption, fill="white", font=font)  # Add text to the box
            
            plt.figure(figsize=(10, 10))
            plt.imshow(image)
            plt.axis("off")
            plt.show()


if __name__ == "__main__":

    # set work dir to OWL_ViT
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    input = deserialize("./data.pkl")
    proxy_url = input["proxy_url"]
    images = input["images"]
    text_queries = input["text_queries"]
    
    owl_vit = OWL_ViT(proxy_url=proxy_url)
    results = owl_vit.predict(images, text_queries)
    owl_vit.visualize(images, results)
    
    output = {
        "results": results
    }
    serialize(output, "./data.pkl")
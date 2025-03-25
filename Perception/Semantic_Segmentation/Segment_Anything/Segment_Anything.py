from PIL import Image, ImageDraw, ImageFont
import torch
from transformers import SamModel, SamProcessor
import os
import matplotlib.pyplot as plt
from Utils import serialize, deserialize
from utils import *

class Segment_Anything:
    def __init__(self, model_name="facebook/sam-vit-huge", proxy_url=None):
        """
        Initialize the Segment_Anything class and load the model and processor.

        :param model_name: Model name, default is "facebook/sam-vit-huge"
        :param proxy_url: Proxy URL for downloading the pretrained model
        """
        if proxy_url:
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SamModel.from_pretrained(model_name).to(self.device)
        self.processor = SamProcessor.from_pretrained(model_name)

    def predict(self, image, input_points=None, input_boxes=None):
        """
        Perform prediction on the input image and return a list of segmentation results.

        :param image: Input image (PIL.Image.Image object)
        :param input_points: List of input points (nb_images, nb_predictions, nb_points_per_mask, 2)
        :param threshold: Confidence threshold, default is 0.1
        :return: List of segmentation results, each element contains 'mask', 'score'
        """
        # Process the input
        if input_points is not None and input_boxes is None:
            inputs = self.processor(image, input_points=input_points, return_tensors="pt").to(self.device)
        elif input_points is None and input_boxes is not None:
            inputs = self.processor(image, input_boxes=input_boxes, return_tensors="pt").to(self.device)
        elif input_points is not None and input_boxes is not None:
            inputs = self.processor(image, input_points=input_points, input_boxes=input_boxes, return_tensors="pt").to(self.device)
        else:
            raise("Please provide either input_points or input_boxes")
                                                                   
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        masks = self.processor.image_processor.post_process_masks(
            outputs.pred_masks.cpu(), inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu()
        )[0][0]
        scores = outputs.iou_scores[0][0]
        return masks, scores

    def visualize(self, image, masks, scores):
        """Visualize the segmentation results on the input image."""
        show_masks_on_image(image, masks, scores)


if __name__=="__main__":
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    input = deserialize("./data.pkl")
    proxy_url = input["proxy_url"]
    image = input["image"]
    input_points = input["input_points"]
    input_boxes = input["input_boxes"]
    
    segment_anything = Segment_Anything(proxy_url=proxy_url)
    masks, scores = segment_anything.predict(image, input_points, input_boxes)
    segment_anything.visualize(image, masks, scores)
    
    output = {
        "masks": masks,   
        "scores": scores
    }
    serialize(output, "./data.pkl")
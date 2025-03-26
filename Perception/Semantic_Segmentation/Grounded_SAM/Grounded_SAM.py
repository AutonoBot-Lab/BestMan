import os
import torch
import numpy as np
from PIL import Image
from typing import Any, List, Dict, Optional, Union, Tuple
from transformers import AutoModelForMaskGeneration, AutoProcessor, pipeline
from Utils import serialize, deserialize
from utils import *

class Grounded_SAM:
    
    def __init__(
        self, 
        proxy_url: str = None,
        detect_threshold: float = 0.3,
        detector_id: Optional[str] = None, 
        segmenter_id: Optional[str] = None,
        polygon_refinement: bool = False
    ):
        
        if proxy_url:
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # init object detector
        self.detect_threshold = detect_threshold
        detector_id = detector_id if detector_id is not None else "IDEA-Research/grounding-dino-tiny"
        self.object_detector = pipeline(model=detector_id, task="zero-shot-object-detection", device=self.device)
        
        # init segmentator
        segmenter_id = segmenter_id if segmenter_id is not None else "facebook/sam-vit-base"
        self.segmentator = AutoModelForMaskGeneration.from_pretrained(segmenter_id).to(self.device)
        self.segment_processor = AutoProcessor.from_pretrained(segmenter_id)
        self.polygon_refinement = polygon_refinement
        
    def detect(
        self,
        image: Image.Image,
        labels: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Use Grounding DINO to detect a set of labels in an image in a zero-shot fashion.
        """

        labels = [label if label.endswith(".") else label+"." for label in labels]

        results = self.object_detector(image,  candidate_labels=labels, threshold=self.detect_threshold)
        results = [DetectionResult.from_dict(result) for result in results]

        return results

    def segment(
        self,
        image: Image.Image,
        detection_results: List[Dict[str, Any]]
    ) -> List[DetectionResult]:
        """
        Use Segment Anything (SAM) to generate masks given an image + a set of bounding boxes.
        """


        boxes = get_boxes(detection_results)
        inputs = self.segment_processor(images=image, input_boxes=boxes, return_tensors="pt").to(self.device)

        outputs = self.segmentator(**inputs)
        masks = self.segment_processor.post_process_masks(
            masks=outputs.pred_masks,
            original_sizes=inputs.original_sizes,
            reshaped_input_sizes=inputs.reshaped_input_sizes
        )[0]

        masks = refine_masks(masks, self.polygon_refinement)

        for detection_result, mask in zip(detection_results, masks):
            detection_result.mask = mask

        return detection_results

    def predict(
        self,
        image: Union[Image.Image, str],
        labels: List[str]
    ) -> Tuple[np.ndarray, List[DetectionResult]]:
        
        if isinstance(image, str):
            image = load_image(image)
        
        detections = self.detect(image, labels)
        detections = self.segment(image, detections)

        return np.array(image), detections
    
    def visualize(self, image_array, detections, save_name=None):
        """ Visualize the image with the detections """
        if save_name is None:
            plot_detections_plotly(image_array, detections)
        else:
            plot_detections(image_array, detections, save_name)
    

if __name__=="__main__":
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    input = deserialize("./data.pkl")
    proxy_url = input["proxy_url"]
    detect_threshold = input["detect_threshold"]
    detector_id = input["detector_id"]
    segmenter_id = input["segmenter_id"]
    image = input["image"]
    labels = input["labels"]
    save_name = input["save_name"]
    
    ground_sam = Grounded_SAM(proxy_url, detect_threshold, detector_id, segmenter_id)
    image_array, detection = ground_sam.predict(image, labels)
    ground_sam.visualize(image_array, detection, save_name)
    
    output = {
        "image_array": image_array,   
        "detection": detection
    }
    serialize(output, "./data.pkl")
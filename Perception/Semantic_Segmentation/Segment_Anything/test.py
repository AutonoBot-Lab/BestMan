from PIL import Image
from Utils import Submodule
from utils import *

proxy_url = '127.0.0.1:7897'
image = Image.open("./test_image/car.png").convert("RGB")

# single point for one mask
input_points = [[[450, 600]]]  # 2D location of a window in the image
show_points_on_image(image, input_points[0])
input_boxes = None

# multiple points for one mask
# input_points = [[[550, 600], [2100, 1000]]]
# show_points_on_image(image, input_points)
# input_boxes = None

# single box for one mask
# input_points = None
# input_boxes = [[[650, 900, 1000, 1250]]]
# show_boxes_on_image(image, input_boxes[0]) 

# single point and box for one mask
# input_boxes = [[[650, 900, 1000, 1250]]]
# input_points = [[[820, 1080]]]
# show_points_and_boxes_on_image(image, input_boxes[0], input_points[0])

segment_anything = Submodule()
input_data = {
    "proxy_url": proxy_url,
    "image": image,
    "input_points": input_points,
    "input_boxes": input_boxes
}
output = segment_anything.call(input_data, "segment_anything", "Perception/Semantic_Segmentation/Segment_Anything/Segment_Anything.py")

print(f"\nresults:")
masks, scores = output["masks"], output["scores"]

for i in range(len(masks)):
    mask, score = masks[i], scores[i]
    print(f"Segment mask {i+1} shape {mask.shape} with score {score}")
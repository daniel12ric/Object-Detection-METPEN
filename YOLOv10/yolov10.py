# -*- coding: utf-8 -*-
"""YOLOv10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dPJaWzFoBQF0wflrYo3VOYTCra27EsZL
"""

!nvidia-smi

import os
home = os.getcwd()
print(home)

!pip install -q supervision

!pip install -q git+https://github.com/THU-MIG/yolov10.git

!mkdir -p {home}/weights
!wget -P {home}/weights -q https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10n.pt
!wget -P {home}/weights -q https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10s.pt
!ls -lh {home}/weights

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import Image, clear_output


# %cd {home}

Image (filename='/content/orang6.JPG', height=600)

# Commented out IPython magic to ensure Python compatibility.
# %cd {home}
!yolo task=detect mode=predict conf=0.25 save=True model={home}/weights/yolov10s.pt source=/content/orang6.JPG

from ultralytics import YOLOv10

model = YOLOv10(f'{home}/weights/yolov10s.pt')
results=model(source=f'/content/orang6.JPG', conf=0.25)
# # Training
# model.train(...)
# # after training, one can push to the hub
# model.push_to_hub("your-hf-username/yolov10-finetuned")

# # Validation
# model.val(...)

print(results[0].boxes.xyxy)
print(results[0].boxes.conf)
print(results[0].boxes.cls)

import cv2
import supervision as sv
from ultralytics import YOLOv10

model = YOLOv10(f'{home}/weights/yolov10s.pt')
image = cv2.imread('/content/orang6.JPG')
results=model(image)[0]
detections = sv.Detections.from_ultralytics(results)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

sv.plot_image(annotated_image)

!pip install roboflow

# !mkdir {home}/datasets
# %cd {home}/datasets

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="YmbAf94dar4AnWymxESJ")
project = rf.workspace("metpen-o4ool").project("metpen-1")
version = project.version(1)
dataset = version.download("yolov8")

# Commented out IPython magic to ensure Python compatibility.
# %cd {home}

!yolo task=detect mode=train epochs=100 batch=32 plots=True \
model={home}/weights/yolov10s.pt \
data={dataset.location}/data.yaml
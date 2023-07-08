import xml.etree.ElementTree as ET
import glob
import os
import json
from tqdm import tqdm
import sys
from pascal_voc_writer import Writer


classes = ["MetalPart", "Pliers", "PlasticPart", "Bolt", "Washer", "Screwdriver", "Nut", "BoltWasher", "Nail", 
           "AdjustableClamp", "Hammer", "Cutter", "Pen", "FuelCap", "BoltNutSet", "Wire", "Wrench", "Battery",
           "LuggageTag", "MetalSheet", "Label", "Rock", "SodaCan", "ClampPart", "PaintChip", "AdjustableWrench",
           "LuggagePart", "Hose", "Screw", "Tape", "Wood", "Spring", "Spanner", "Cloth"]
# print([name for name in os.listdir(".") if os.path.isdir(name)])


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]



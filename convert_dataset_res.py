import cv2
import os
import xml.etree.ElementTree as ET
import glob

# Set the paths for the input and output directories
input_dir = "mixed_dataset_PNG1"
output_dir = "mixed_dataset_PNG1_1280"
input_resolution = (4056, 3040)  # Original resolution
output_resolution = (1280, 1280)  # Desired resolution

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
img_files = glob.glob(os.path.join(input_dir, f'*'))

print(img_files[0])
# Loop through each image file in the input directory
for filename in img_files:
    if filename.endswith(".jpg") or filename.endswith(".PNG"):
        
        # Open the image using Pillow
        image_path = filename# os.path.join(input_dir, filename)
        image = cv2.imread(image_path)

        # Resize the image to the desired resolution (1280x1280)
        resized_image = cv2.resize(image, output_resolution)

        # Save the resized image to the output directory
        fnm = filename.split("/")[-1]
        output_path = os.path.join(output_dir, fnm)
        cv2.imwrite(output_path, resized_image)

        print(f"Resized {filename} successfully!")

        # Open and resize the corresponding XML label file
        xml_path = os.path.splitext(filename)[0] + ".xml"
        xml_filename = xml_path.split("/")[-1]
        # xml_path = os.path.join(input_dir, xml_filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Calculate the resize ratio
        resize_ratio_x = output_resolution[0] / input_resolution[0]
        resize_ratio_y = output_resolution[1] / input_resolution[1]

        # Update the size values in the XML file
        size = root.find("size")
        size.find("width").text = str(output_resolution[0])
        size.find("height").text = str(output_resolution[1])

        # Update the bounding box coordinates
        for obj in root.findall("object"):
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            # Adjust the bounding box coordinates based on the resize ratio
            xmin = int(xmin * resize_ratio_x)
            ymin = int(ymin * resize_ratio_y)
            xmax = int(xmax * resize_ratio_x)
            ymax = int(ymax * resize_ratio_y)

            # Update the bounding box coordinates in the XML file
            bbox.find("xmin").text = str(xmin)
            bbox.find("ymin").text = str(ymin)
            bbox.find("xmax").text = str(xmax)
            bbox.find("ymax").text = str(ymax)

        # Save the updated XML label file to the output directory
        resized_xml_path = os.path.join(output_dir, xml_filename)
        tree.write(resized_xml_path)

        print(f"Updated {xml_filename} successfully!")

print("All images and labels resized!")

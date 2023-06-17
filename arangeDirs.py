import os
import glob
import shutil
from tqdm import tqdm
import sys

def get_subfolders(folder_path):
    folders = []
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)#.split(folder_path)[-1]
            folders.append(subfolder_path)
    return folders

# Specify the folder path for which you want to print subfolders
folder_path = sys.argv[1] #'Laballed_data_spanner'

folder_path_out = folder_path + "_flat"

isExist = os.path.exists(folder_path_out)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(folder_path_out)
   print(folder_path_out)



dir_names = get_subfolders(folder_path)

IMG_FRMT = "PNG"

files_img = []
for d in dir_names:
    files_img = files_img + glob.glob(os.path.join(d, f'*.{IMG_FRMT}'))

files_xml = []
for d in dir_names:
    files_xml = files_xml + glob.glob(os.path.join(d, '*.xml'))


print(files_img[-1])
print(files_xml[-1])
print(folder_path_out + "/" )
#folder_path_out = "1_flat"
#print(os.path.exists(folder_path_out))

print("Copying the images")
for file in tqdm(files_img):

    #dfile = file.replace('/', '_').replace(' ', '_')
    try:
        dest_path = folder_path_out + "/" + file.replace('/', '_').replace(' ', '_')

        shutil.copy(file, dest_path)
    except Exception as e:
        print(e)
        print("Can not copy this file: ",dest_path)
print("Copying the Labels")

for file in tqdm(files_xml):
    
    try:

        dfile = file.replace('/', '_').replace(' ', '_')

        shutil.copy(file, folder_path_out + "/" + dfile)
    except:
        print("Can not copy this file: ", dfile)
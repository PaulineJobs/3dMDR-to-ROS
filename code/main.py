import os
import json

# Declare the path of the original and target files
original_folder_path = "../Test_Files/Original_Files/"
converted_folder_path = "../Test_Files/Converted_Files/"

# Function to check if the file already exists
def is_file_exists (converted_folder_path,filename):
    # Check if the file exists using os.path.exists()
    if os.path.exists(converted_folder_path+filename):
        return True
    else:
        return False

# Function to split the filename into file and extension
def split_name_extension(filename):
    extracted = filename.split(".")
    file, extension = extracted[0],extracted[1]
    return file,extension

def get_resolution(filename, original_folder_path):
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        resolution = data["properties"]["resolution"]
        string_resolution = "[ "
        for i in resolution :
            string_resolution+=str(i)
            string_resolution+=", "
        string_resolution=string_resolution[:-2]
        string_resolution+=" ]"
        return string_resolution

def get_negate(filename, original_folder_path):
    return str(0)


def get_new_name(filename, original_folder_path):
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        new_name= data["properties"]["localmap_id"]
        return new_name

def get_thresh(filename, original_folder_path):
    with open(original_folder_path + filename, "r") as f:
        data = json.load(f)
        list_of_voxels = data["properties"]["list_of_voxels"]
        sorted_list_of_voxels = sorted(list_of_voxels)
        half_of_values = (sorted_list_of_voxels[0]+sorted_list_of_voxels[len(sorted_list_of_voxels)-1])/2
        thresh = half_of_values/sorted_list_of_voxels[len(sorted_list_of_voxels)-1]
        return str(thresh)



# Function to create an empty yaml file
def create_yaml_file (converted_folder_path,filename, origin = " ", negate=" ", occupied_tresh=" ", free_tresh=" "  ):
    file,extension = split_name_extension(filename)
    new_filename=get_new_name(filename, original_folder_path)
    resolution = get_resolution(filename, original_folder_path)
    negate = get_negate(filename, original_folder_path)
    occupied_tresh = get_thresh(filename, original_folder_path)
    free_tresh = get_thresh(filename,original_folder_path)
    # Check if the file already exists
    if not (is_file_exists(converted_folder_path,new_filename)):
        # Open the file and write the basic yaml structure
        f = open(converted_folder_path+new_filename, "w")
        f.write("image: "+new_filename+"\n")
        f.write("resolution: " + resolution +"\n")
        f.write("origin: " + origin+"\n")
        f.write("negate: " + negate +"\n")
        f.write("occupied_tresh: " + occupied_tresh +"\n")
        f.write("free_tresh: " + free_tresh +"\n")
        f.close()

# Function to convert all files in a folder
def convert_folder(original_folder_path,converted_folder_path) :
    for filename in os.listdir(original_folder_path):
        create_yaml_file(converted_folder_path, filename)

# Function to remove the converted files
def remove_converted_folder(folder_path):
    for filename in os.listdir(folder_path):
        os.remove(folder_path+filename)

# Remove the existing converted files
remove_converted_folder(converted_folder_path)
# Convert all files in the original folder
convert_folder(original_folder_path,converted_folder_path)





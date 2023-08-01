import os
import json

# Declare the path of the pathway to the folders
original_folder_path = "../Test_Files/MDR_files/"
converted_folder_path = "../Test_Files/ROS_files/"

# Function to check if the file exists and correspond to the pathway
def file_exists (converted_folder_path, filename):
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

def get_information_for_yaml_file_from_json_file(filename, original_folder_path):
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        resolution = get_resolution(data)
        negate = get_negate(data)
        treshold = get_thresh(data)
        yaml_filename = get_yaml_filename(data)
        origin = "[0,0,0]"
        return resolution, negate, treshold, yaml_filename, origin

def get_resolution(data):
        resolution = data["properties"]["resolution"]
        string_resolution = "[ "
        for i in resolution :
            string_resolution+=str(i)
            string_resolution+=", "
        string_resolution=string_resolution[:-2]
        string_resolution+=" ]"
        return string_resolution

def get_negate(data):
    return str(0)

def get_yaml_filename(data):
        yaml_filename = data["properties"]["localmap_id"]
        return yaml_filename

def get_thresh(data):
    list_of_voxels = data["properties"]["list_of_voxels"]
    sorted_list_of_voxels = sorted(list_of_voxels)
    half_of_values = (sorted_list_of_voxels[0]+sorted_list_of_voxels[len(sorted_list_of_voxels)-1])/2
    thresh = half_of_values/sorted_list_of_voxels[len(sorted_list_of_voxels)-1]
    return str(thresh)

def get_information_for_pgm_file_from_json_file(filename, original_folder_path) :
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        pgm_filename = split_name_extension(data["properties"]["localmap_id"])[0]+"pgm"
        list_of_points = data["properties"]["list_of_voxels"]
        width = data["properties"]["size"][0]
        height = data["properties"]["size"][1]
        depth = data["properties"]["size"][2]
    return list_of_points, width, height, depth, pgm_filename




# Function to create yaml file
def create_yaml_file (converted_folder_path,filename, origin = " ", negate=" ", occupied_tresh=" ", free_tresh=" "  ):
    resolution, negate, treshold, yaml_filename, origin = get_information_for_yaml_file_from_json_file(filename, original_folder_path)
    # Check if the file already exists
    if not (file_exists(converted_folder_path, yaml_filename)):
        # Open the file and write the basic yaml structure
        f = open(converted_folder_path + yaml_filename, "w")
        f.write("image: "+ yaml_filename +"\n")
        f.write("resolution: " + resolution +"\n")
        f.write("origin: " + origin+"\n")
        f.write("negate: " + negate +"\n")
        f.write("occupied_tresh: " + treshold +"\n")
        f.write("free_tresh: " + treshold +"\n")
        f.close()


def create_pgm_file (converted_folder_path,filename, origin = " ", negate=" ", occupied_tresh=" ", free_tresh=" "  ):
    list_of_points, width, height, depth, pgm_filename = get_information_for_pgm_file_from_json_file(filename, original_folder_path)
    if not (file_exists(converted_folder_path, pgm_filename)):
        with open(converted_folder_path + pgm_filename, "w") as f:
            f.write("P2\n")
            f.write(f"{width} {height}\n")
            f.write("255\n")
            for point in list_of_points:
               f.write(f"{point} ")
            f.close()

# Function to convert all files in a folder
def convert_folder(original_folder_path,converted_folder_path) :
    for filename in os.listdir(original_folder_path):
        create_yaml_file(converted_folder_path, filename)
        create_pgm_file(converted_folder_path, filename)

# Function to remove the converted files
def remove_converted_folder(folder_path):
    for filename in os.listdir(folder_path):
        os.remove(folder_path+filename)


# Remove the existing converted files
remove_converted_folder(converted_folder_path)
# Convert all files in the original folder
convert_folder(original_folder_path,converted_folder_path)





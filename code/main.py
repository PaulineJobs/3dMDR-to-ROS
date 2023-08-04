import os
import json

# Declare the path of the pathway to the folders
original_folder_path = "../Test_Files/MDR_files/"
converted_folder_path = "../Test_Files/ROS_files/"
# Default thresholds
free_thresh = "0.196"
occupied_thresh = "0.65"


# Check if the file exists and correspond to the pathway
def file_exists (converted_folder_path, filename):
    # Check if the file exists using os.path.exists()
    if os.path.exists(converted_folder_path+filename):
        return True
    else:
        return False

# Split the filename into file and extension
def split_name_extension(filename):
    extracted = filename.split(".")
    file, extension = extracted[0],extracted[1]
    return file,extension

# Read the json file and get information needed
def get_information_for_yaml_file_from_json_file(filename, original_folder_path):
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        resolution = get_resolution(data)
        negate = set_negate(data)
        yaml_filename = get_yaml_filename(data)
        origin = "[0,0,0]"
        return resolution, negate, yaml_filename, origin

# Get the resolution form json data in the correct format for the yaml file
def get_resolution(data):
        resolution = data["properties"]["resolution"]
        string_resolution = "[ "
        for i in resolution :
            string_resolution+=str(i)
            string_resolution+=", "
        string_resolution=string_resolution[:-2]
        string_resolution+=" ]"
        return string_resolution

#Set the negate
def set_negate(data):
    return str(0)

# Get the name of the future yaml file
def get_yaml_filename(data):
        yaml_filename = data["properties"]["localmap_id"]
        return yaml_filename

#Get information from the json file data needed for the pgm file
def get_information_for_pgm_file_from_json_file(filename, original_folder_path) :
    with open(original_folder_path+filename, "r") as f:
        data = json.load(f)
        pgm_filename = split_name_extension(data["properties"]["localmap_id"])[0]+".pgm"
        list_of_points = data["properties"]["list_of_voxels"]
        width = data["properties"]["size"][0]
        height = data["properties"]["size"][1]
        depth = data["properties"]["size"][2]
    return list_of_points, width, height, depth, pgm_filename




# Create yaml file
def create_yaml_file (converted_folder_path,filename ):
    resolution, negate, yaml_filename, origin = get_information_for_yaml_file_from_json_file(filename, original_folder_path)
    # Check if the file already exists
    if not (file_exists(converted_folder_path, yaml_filename)):
        # Open the file and write the basic yaml structure
        f = open(converted_folder_path + yaml_filename, "w")
        f.write("image: "+ yaml_filename +"\n")
        f.write("resolution: " + resolution +"\n")
        f.write("origin: " + origin+"\n")
        f.write("negate: " + negate +"\n")
        f.write("occupied_tresh: " + occupied_thresh +"\n")
        f.write("free_tresh: " + free_thresh +"\n")
        f.close()

#Create pgm file
def create_pgm_file (converted_folder_path,filename, origin = " ", negate=" ", occupied_tresh=" ", free_tresh=" "  ):
    list_of_points, width, height, depth, pgm_filename = get_information_for_pgm_file_from_json_file(filename, original_folder_path)
    if not (file_exists(converted_folder_path, pgm_filename)):
        with open(converted_folder_path + pgm_filename, "w") as f:
            f.write("P2\n")
            if depth == 1:
                f.write(f"{width} {height} \n")
            else :
                f.write(f"{width} {height} {depth}\n")

            f.write("255\n")
            for point in list_of_points:
               f.write(f"{point} ")
            f.close()

# Convert all files in a folder
def convert_folder(original_folder_path,converted_folder_path) :
    for filename in os.listdir(original_folder_path):
        create_yaml_file(converted_folder_path, filename)
        create_pgm_file(converted_folder_path, filename)

# Remove the converted files
def remove_converted_folder(folder_path):
    for filename in os.listdir(folder_path):
        os.remove(folder_path+filename)



if __name__ == '__main__':
    print("Hello ! ")
    print("Here you can convert 3D MDR files (.json) into ROS Gridmap files (yaml+pgm)")
    while True :
        user_input = input ("Please, press enter to convert files located in the folder Test_Files/MDR_files/")
        if user_input == '' :
            break
    print("Please wait....")
    # Remove the existing converted files
    remove_converted_folder(converted_folder_path)
    # Convert all files in the original folder
    convert_folder(original_folder_path,converted_folder_path)
    print("Conversion done")
    print("Converted files are located in Test_Files/ROS_files/")





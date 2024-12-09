# ------------------------------------------------------------------------------
# Author: Rui Xu
# Date: 2024-12-09
# Description:
# It is specifically designed for processing datasets such as SDSD, SMID, and others 
# that use `.npy` format to store images. This utility helps in converting large 
# collections of `.npy` files into more common image formats like `.png` for further 
# analysis or visualization.
#
# Usage:
# - Provide the path to the dataset containing `.npy` files in the `input_directory` 
#   variable.
# - The script will automatically process all `.npy` files in the given directory, 
#   convert them to `.png`, and delete the original `.npy` files after conversion.
#
# Notes:
# 1. The script assumes that `.npy` files contain 3-channel (RGB) image data. If the 
#    images are stored in a different format or have a different color channel ordering 
#    (e.g., BGR), the color channels may need to be manually adjusted.
# 2. This script can be applied to datasets such as SDSD, SMID, and others that store 
#    image data in `.npy` format.
# 3. Some npy conversion codes do not set the RGB-to-BGR conversion, so the converted 
#    image may have color issues.
#
# ------------------------------------------------------------------------------


import os
import numpy as np
from PIL import Image

def process_and_overwrite_npy(npy_file_path):

    try:
        # Load the .npy file
        data = np.load(npy_file_path)

        # Check the data type and dimensions
        print(f"Processing {npy_file_path} - Shape: {data.shape}, Data type: {data.dtype}")

        if data.ndim == 3 and data.shape[2] == 3:
            # Assuming the data is in RGB order, convert it to BGR order
            data = data[..., [2, 1, 0]]

            # Convert the numpy array to an Image object
            image = Image.fromarray(data.astype(np.uint8))

            # Save the image as a PNG file
            png_file_path = npy_file_path.replace('.npy', '.png')
            image.save(png_file_path)
            print(f"Saved {png_file_path}")

            # Delete the original .npy file
            os.remove(npy_file_path) 
            print(f"Deleted original .npy file: {npy_file_path}")

        else:
            print(f"{npy_file_path} does not contain a valid RGB image.")

    except Exception as e:
        print(f"Failed to process {npy_file_path}: {e}")


def process_directory(input_dir):
    """
    Traverse the given directory and process all .npy files.
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.npy'):
                npy_file_path = os.path.join(root, file)
                process_and_overwrite_npy(npy_file_path)


if __name__ == "__main__":

    input_directory = '/path_to_dataset/'

    process_directory(input_directory)

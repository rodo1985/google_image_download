import os
import cv2
from tqdm import tqdm
from simple_image_download import simple_image_download as simp
import pandas as pd

# Load the CSV file with proper delimiter
df = pd.read_csv('trail.csv', delimiter=';')

# Clean up column names
df.columns = df.columns.str.strip().str.replace('"', '')

# Extract the IDs and create the combined brand and model strings
ids = df['v_idreview'].tolist()
keywords = (df['v_descmarca'] + ' ' + df['v_descmodelo']).tolist()

# number of images to download
n_images = 100

# if folder exist, delete it
if os.path.exists('simple_images'):
    os.system('rm -r images')

# download images
for keyword in keywords:
    response = simp.simple_image_download
    response().download(keyword, n_images)


for keyword in keywords:

    # get all files in folder
    input_folder = os.path.join('simple_images', keyword)
    files = os.listdir(input_folder)
    
    print('Number of files before cleaning = ' + str(len(files)))

    # loop through files using tqdm
    for file in tqdm(files):
        # get image
        img = cv2.imread(os.path.join(input_folder, file))

        if img is None:
            
            # remove file
            os.remove(os.path.join(input_folder, file))

    # rename the folder adding the id at the beginning
    os.rename(input_folder, os.path.join('simple_images', str(ids[keywords.index(keyword)]) + '_' + keyword))

    print('Number of files after cleaning = ' + str(len(os.listdir(input_folder))))

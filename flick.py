import logging
from moviepy.editor import ImageClip, concatenate_videoclips
import os
from glob import glob
import json
import rawpy
import imageio
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_cr2_to_jpeg(cr2_path, output_path):
    with rawpy.imread(cr2_path) as raw:
        rgb = raw.postprocess()
    imageio.imsave(output_path, rgb)

def select_directory():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected

with open('config.json') as config_file:
    config = json.load(config_file)

if not config.get('folder_path'):
    logging.info("Folder path not specified in config, prompting user to select directory.")
    config['folder_path'] = select_directory()
    if not config['folder_path']:
        logging.error("No folder selected. Exiting.")
        exit()

folder_path = config['folder_path']
all_images = glob(os.path.join(folder_path, '*'))
logging.info(f"Found {len(all_images)} files in {folder_path}")

processed_images = []
for img_path in tqdm(all_images, desc="Converting Images"):
    if img_path.lower().endswith('.cr2'):
        output_path = img_path.rsplit('.', 1)[0] + '.jpg'
        convert_cr2_to_jpeg(img_path, output_path)
        processed_images.append(output_path)
    elif img_path.lower().endswith('.png'):
        processed_images.append(img_path)

selected_images = processed_images[:config.get('max_images', 10)]
logging.info(f"Selected {len(selected_images)} images for the video")

clips = []
for img_path in tqdm(selected_images, desc="Creating Clips"):
    clip = ImageClip(img_path)
    if config.get('output_resolution', 0) > 0:
        clip = clip.resize(height=config['output_resolution'])
    clips.append(clip.set_duration(config.get('image_duration', 1)))

video = concatenate_videoclips(clips, method="compose")
logging.info("Writing video file")
video.write_videofile(config.get('output_file', 'output_video.mp4'), fps=config.get('fps', 24))
logging.info(f"Video saved to {config.get('output_file', 'output_video.mp4')}")

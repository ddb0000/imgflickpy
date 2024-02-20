import argparse
import json
import logging
import os
from glob import glob
from multiprocessing import Pool
from pathlib import Path

import imageio
import rawpy
from moviepy.editor import ImageClip, concatenate_videoclips
from tqdm import tqdm
import re

def setup_logging(log_file='app.log'):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ])

def load_config(json_file):
    try:
        with open(json_file, 'r') as file:
            config = json.load(file)
            return config
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
    return {}

def convert_cr2_to_jpeg(cr2_path, output_path):
    try:
        with rawpy.imread(cr2_path) as raw:
            rgb = raw.postprocess()
        imageio.imsave(output_path, rgb)
    except Exception as e:
        logging.error(f"Failed to convert {cr2_path}: {e}")

def parse_arguments(config):
    parser = argparse.ArgumentParser(description='Convert images to a fast-paced video.')
    parser.add_argument('--folder-path', help='Path to the folder containing images.', default=config.get('folder_path'))
    parser.add_argument('--max-images', type=int, default=config.get('max_images', 10), help='Maximum number of images to include in the video.')
    parser.add_argument('--output-resolution', type=int, default=config.get('output_resolution', 1080), help='Resolution of the output video.')
    parser.add_argument('--image-duration', type=float, default=config.get('image_duration', 1), help='Duration of each image in the video.')
    parser.add_argument('--fps', type=int, default=config.get('fps', 24), help='Frames per second of the output video.')
    parser.add_argument('--output-file', default=config.get('output_file', 'output_video.mp4'), help='Name of the output video file.')
    parser.add_argument('--log-file', default='process.log', help='Log file path.')
    return parser.parse_args()

def get_image_paths(folder_path, extensions=('.cr2', '.jpg', '.jpeg', '.png')):
    folder = Path(folder_path)
    images = [(img, img.stat().st_mtime) for ext in extensions for img in folder.glob(f'*{ext}')]
    images.sort(key=lambda x: x[1])  # Sort by modification time
    return [str(img[0]) for img in images]


def process_image(img_path):
    try:
        file_extension = Path(img_path).suffix.lower()
        if file_extension == '.cr2':
            output_path = str(Path(img_path).with_suffix('.jpg'))
            convert_cr2_to_jpeg(img_path, output_path)
            return output_path
        elif file_extension in ('.jpg', '.jpeg', '.png'):
            return img_path
    except Exception as e:
        logging.error(f"Error processing {img_path}: {e}")
        return None

def validate_output(output_file):
    if Path(output_file).is_file():
        logging.info(f"Successfully created video: {output_file}")
    else:
        logging.error(f"Failed to create video: {output_file}")

def main():
    config = load_config('config.json')
    args = parse_arguments(config)
    setup_logging(args.log_file)

    all_images = get_image_paths(args.folder_path)
    if not all_images:
        logging.error("No images found. Exiting.")
        return

    with Pool() as p:
        processed_images = list(tqdm(p.imap(process_image, all_images), total=len(all_images), desc="Processing Images"))
    processed_images = [img for img in processed_images if img]

    if len(processed_images) > args.max_images:
        processed_images = processed_images[:args.max_images]

    clips = [ImageClip(img).set_duration(args.image_duration).resize(height=args.output_resolution) for img in tqdm(processed_images, desc="Creating Clips")]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(args.output_file, fps=args.fps)
    
    validate_output(args.output_file)

if __name__ == "__main__":
    main()

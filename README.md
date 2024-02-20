# imgflickpy

**imgflickpy**: quick hack to morph a static pile of images into video.

## magics:
- **CR2 to JPEG**: Handle RAW images like a pro.
- **Multiprocessing**: Because waiting is for the weak.
- **Customize everything**: Frame rate, resolution, etc. Through config files or command line, because GUIs are overrated.

## clone this beast:
```
git clone https://github.com/ddb0000/imgflickpy
```

### dependencies:
```
pip install -r requirements.txt
```

## configuration:
Tweak `config.json`:
```json
{
    "folder_path": "path/to/your/images",
    "max_images": 60,
    "output_resolution": 1080,
    "image_duration": 0.01,
    "fps": 24,
    "output_file": "your_video.mp4"
}
```
- `folder_path`: Where images chill.
- `max_images`: How many images to roll with.
- `output_resolution` & `fps`: Dial quality and pace.
- `output_file`: Name your masterpiece.

## running the show:
```
python flick.py --folder-path "path/to/images" --max-images 100 --output-file "epic_video.mp4"
```
Need help? `python flick.py -h` (But you've got this, right?)

## logs:
Check `process.log` to see what went down. Mix it up with `--log-file` to log elsewhere.

## contribute:
Got an idea? A fix? Dive in. Fork it, branch it, push it, PR it.

## license:
MIT License. Hack it, tweak it, share it, teach it.
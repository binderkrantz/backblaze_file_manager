from datetime import datetime
from pathlib import Path

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()

def get_file_creation_timestamp(file_path):
    '''
    Extracts the creation timestamp of a file.
    If the file is an image, the timestamp is extracted from the exif data.
    If the file is a video, the timestamp is extracted from the metadata.
    If the timestamp is not found, the earliest timestamp from the file stat is used.
    '''
    image_formats = ('png', 'jpg', 'jpeg', 'heic')
    video_formats = ('mov', 'mp4')
    file_created_at = None

    file_extention = Path(file_path).suffix[1:].lower()

    # extract exif data from image file
    if file_extention in image_formats:
        img = Image.open(file_path)
        exif_data = img.getexif()
        exif_ts = exif_data.get(306) or exif_data.get(36867) # 306: DateTime, 36867: DateTimeOriginal
        if exif_ts:
            file_created_at = datetime.strptime(exif_ts, '%Y:%m:%d %H:%M:%S')

    # extract metadata from video file
    elif file_extention in video_formats:
        parser = createParser(file_path)
        if metadata := extractMetadata(parser):
            file_created_at = metadata.get('creation_date')
    else:
        print(f'Unknown file format: {file_extention}')

    # read file stat data
    if file_created_at is None:
        file_info = Path(file_path).stat()
        stat_ts = min(file_info.st_birthtime, file_info.st_mtime) # the earliest timestamp is usually the accurate one
        file_created_at = datetime.fromtimestamp(stat_ts)

    assert isinstance(file_created_at, datetime), f'Invalid timestamp: {file_created_at}'
    
    return file_created_at
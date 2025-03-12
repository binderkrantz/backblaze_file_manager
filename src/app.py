from backblaze import BBlaze
from metadata import get_file_creation_timestamp

from pathlib import Path
from pprint import pprint



# 1. List files in directory. For each file:
    # 2. Extract datetime from file metadata (image exif, video metadata, file stat)
    # 3. Rename file by exif datetime
    # 4. Upload file to B2

def list_file_paths(dir_path, recursive=False):
    '''list all file paths in a directory'''
    dir_path = Path(dir_path)
    pattern = '**/*.*' if recursive else '*.*'
    return [str(p) for p in dir_path.glob(pattern)]

def dt_as_path(file_created_at):
    year = file_created_at.strftime('%Y')
    month = file_created_at.strftime('%m')
    full_str = file_created_at.strftime('%Y%m%dT%H%M%S')

    return '/'.join([year, month, full_str])

def increment_filename(file_path:str):
    '''Increment the suffix (after the last '-') of a file path'''
    path = Path(file_path)
    if '-' in path.stem:
        base, counter = path.stem.rsplit('-', 1)
        if counter:
            return str(path.with_stem(f"{base}-{int(counter) + 1}").as_posix())
    return str(path.with_stem(f"{path.stem}-1").as_posix())

########################################################################################################

def main():
    dir_path = r"C:/Users/chanb/OneDrive/Skrivebord/New folder/test"
    new_files = [Path(file_path) for file_path in list_file_paths(dir_path, recursive=True)]
    ########################################################
    # pprint(new_files)
    ########################################################
    online_files = BBlaze.list_files(bucket_name='wb-memories')
    pprint(online_files)
    to_upload = []

    for file_path in new_files:
        
        ts = get_file_creation_timestamp(str(file_path))
        new_file_name = dt_as_path(ts)
        new_file_size = file_path.stat().st_size
        full_new_file_name = new_file_name + file_path.suffix

        while (full_new_file_name, new_file_size) in online_files: ## TODO: workout the logic here. If name with same size already exists, file should be skipped as its likely a dupe.
            full_new_file_name = increment_filename(full_new_file_name)

        online_files.add((full_new_file_name, new_file_size))

        to_upload.append({
            "file_path": file_path,
            "new_name": full_new_file_name
        })
    pprint(to_upload)
    # for job in to_upload:
        # bb.upload_file(bucket_name='wb-memories', **job)

if __name__ == '__main__':
    main()
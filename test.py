import pathlib

def list_file_paths(dir_path, recursive=False):
    '''list all file paths in a directory'''
    dir_path = pathlib.Path(dir_path)
    pattern = '**/*' if recursive else '*'
    return [str(p) for p in dir_path.glob(pattern) if p.is_file()]

# Example usage:
x = list_file_paths(r"C:/Users/chanb/OneDrive/Skrivebord/New folder/", recursive=True)
print(x)
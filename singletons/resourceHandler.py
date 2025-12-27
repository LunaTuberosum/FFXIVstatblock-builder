import json
import pickle
import pygame
import os
import shutil


def load_dir(dir_path: str) -> list[str]:
    try:
        return os.listdir(dir_path)
    except:
        raise FileNotFoundError(f'Path "{dir_path}" dosen\'t exist or dosen\'t lead to a directory.')
    
def save_dir(dir_path: str, dir_name: str) -> None:
    try:
        os.makedirs(f'{dir_path}/{dir_name}')
    except:
        raise OSError(f'Something went wrong when making the dir {dir_name} at {dir_path}.')
    
def del_dir(dir_path: str) -> None:
    try:
        os.rmdir(dir_path)
    except:
        raise OSError(f'Something went wrong when deleting the dir {dir_path}.')
    
def rename_dir(dir_path: str, new_name: str) -> bool:
    try:
        os.rename(dir_path, new_name)
        return True
    except FileExistsError:
        return False
    except:
        raise OSError(f'Something went wrong when renaming the dir {dir_path}.')
    
def move_dir(dir_path: str, newPath: str) -> None:
    try:
        shutil.move(dir_path, newPath)
    except:
        raise OSError(f'Something went wrong when moving the dir {dir_path}.')

def load_image(image_path: str) -> pygame.Surface:
    try:
        return pygame.image.load(image_path).convert_alpha()
    except:
        raise FileNotFoundError(f'Path "{image_path}" dosen\'t exist.')
    
def load_font(font_path: str, font_size: int) -> pygame.font.Font:
    try:
        return pygame.font.Font(font_path, font_size)
    except:
        raise FileNotFoundError(f'Path "{font_path}" dosen\'t exist.')
    
def load_pickle(pickle_path: str) -> dict[str]:
    try:
        with open(pickle_path, 'rb') as _pickle_data:
            _output: dict[str] = pickle.load(_pickle_data)

        return _output
    
    except FileNotFoundError:
        return {}
    
    except:
        raise FileNotFoundError(f'Path "{pickle_path}" dosen\'t exist.')
    
def save_pickle(pickle_path: str, data: dict) -> None:
    try:
        with open(pickle_path, 'wb') as _pickle_data:
            pickle.dump(data, _pickle_data, protocol=pickle.HIGHEST_PROTOCOL)

    except:
        raise FileNotFoundError(f'An error occured when trying to pickle a file at "{pickle_path}"')
    
def load_json(json_path: str) -> dict[str]:
    try:
        with open(json_path, 'r') as _json_file:
            output: dict[str] = json.load(_json_file)

        return output
    except:
        raise FileNotFoundError(f'Path "{json_path}" dosen\'t exist.')

def save_json(json_path: str, data: dict) -> None:
    try:
        _jsonSave: str = json.dumps(data, indent=4)

        with open(json_path, 'w') as _json_file:
            _json_file.write(_jsonSave)
            
    except:
        raise FileNotFoundError(f'Path "{json_path}" dosen\'t exist.')
    
def del_json(json_path: str) -> None:
    try:
        os.remove(json_path)
    except:
        raise FileNotFoundError(f'Path "{json_path}" dosen\'t exist.')
    
def rename_json(json_path: str, new_name: str) -> bool:
    try:
        os.rename(json_path, new_name)
        return True
    except FileExistsError:
        return False
    except:
        raise FileNotFoundError(f'Path "{json_path}" dosen\'t exist.')

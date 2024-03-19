from pathlib import Path
from shutil import copyfile
from threading import Semaphore, Thread, RLock, current_thread
from unidecode import unidecode
import argparse
import logging
import re


class Pool:
    def __init__(self):
        self.active = []
        self.lock = RLock()
        
    def make_active(self, name):
        with self.lock:
            self.active.append(name)
    
    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)

def main():
    global folders
    folders = []
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    
    parser = argparse.ArgumentParser(description='Script for organizing messy folder')
    parser.add_argument('-s', '--source', required=True)     
    parser.add_argument('-o', '--output', default='result')
    args = vars(parser.parse_args()) 
    source = args.get("source")
    output = args.get("output")

    source_folder = Path(source)
    result_folder = Path(output)
    
    folders.append(source_folder)
    define_folders(source_folder)
    
    semaphore = Semaphore(5)
    pool = Pool()
    
    for folder in folders:
        th = Thread(target=organize_files, args=(folder, result_folder, semaphore, pool))
        th.start()
    print(f"Please check the result in - '{result_folder}' folder!")


def define_folders(path: Path):
    for element in path.iterdir():
        if not element.name in ('video', 'audio', 'images', 'documents'):
            if element.is_dir():
                the_dir = element.name
                new_name = normalize(the_dir)
                new_path = element.parent / new_name
                try:
                    element = element.rename(new_path)
                except Exception as ex:
                    logging.debug(f"exeption - {ex}")
                folders.append(element)
                define_folders(element)


def organize_files(path: Path, result_folder: Path, semaphore: Semaphore, pool: Pool):
    with semaphore:
        name = current_thread().name
        pool.make_active(name)
        for element in path.iterdir():
            if element.is_file():
                the_file = element.name
                new_name = normalize(the_file)
                new_path = element.with_name(new_name)
                element = element.rename(new_path)
                ext = element.suffix
                
                try:
                    if ext.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
                        destination_dir = result_folder / "images" / ext
                        destination_dir.mkdir(exist_ok=True, parents=True)
                        copyfile(element, destination_dir/element.name)
                              
                    elif ext.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
                        destination_dir = result_folder / "videos" / ext
                        destination_dir.mkdir(exist_ok=True, parents=True)
                        copyfile(element, destination_dir/element.name)

                    elif ext.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'):
                        destination_dir = result_folder / "documents" / ext
                        destination_dir.mkdir(exist_ok=True, parents=True)
                        copyfile(element, destination_dir/element.name)
                            
                    elif ext.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
                        destination_dir = result_folder / "audios" / ext
                        destination_dir.mkdir(exist_ok=True, parents=True)
                        copyfile(element, destination_dir/element.name)
                        
                except OSError as ex:
                    logging.error(ex)
        pool.make_inactive(name)
            
            
def normalize(path_argv: str) -> str:
    to_check_the_file = Path(path_argv)
    if to_check_the_file.suffix:
        extension_of_file = to_check_the_file.suffix
        path_argv = re.sub(extension_of_file, "", path_argv)
    new_name = unidecode(path_argv)
    new_name = ''.join(
        [item if item.isalnum() else '_' for item in new_name]) + (extension_of_file if to_check_the_file.suffix else "")
    return new_name

if __name__ == "__main__":
    main()
import os #operating system
import json #modules to deal with json file
import shutil  # support file (or collection of files) copying and removal
import subprocess
import sys # access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go","build"]
def get_all_game_dirs(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory:
                path = os.path.join(source,directory)
                game_paths.append(path)
        break
    return game_paths
def copy_and_overwrite(source,dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source,dest)
def make_json_meta_data_file(path,game_dirs):
    data = {
        "gameNames" : game_dirs,
        "numberofGames" : len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)
def main(source,target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd,source)
    target_path = os.path.join(cwd, target)
    paths = get_all_game_dirs(source_path)
    game_paths = get_name_from_paths(paths,"game")
    create_path(target_path)
    for scr, dest in zip(paths,game_paths):
        dest_path = os.path.join(target_path,dest)
        copy_and_overwrite(scr, dest_path)
        compile_game_code(dest_path)
    json_path = os.path.join(target_path,"metadata.json")

    make_json_meta_data_file(json_path,game_paths)
def get_name_from_paths(paths,to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip,"")
        new_names.append(new_dir_name)
    return new_names
def compile_game_code(path):
    code_file_name = None
    for root,dirs,files in os.walk(path):
        for file in files:
            if file.endswith(GAME_DIR_PATTERN):
                code_file_name = file
            break
        break
    if code_file_name == None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    result = subprocess.run(command, stdout= subprocess.PIPE, universal_newlines= True)
    print("compile result", result)
    os.chdir(cwd)
def create_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) != 3:
        raise Exception("you must pass a source and a target directory only")
    source, target = args[1:]
    main(source,target)


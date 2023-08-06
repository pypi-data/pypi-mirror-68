#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO modo verbose não está desligando
# TODO remove pytest dependency using unittest
# TODO include differente licenses
# TODO include template for tkinter project
# TODO include template for pyqt5 project

import argparse
import logging
import os
import sys
import subprocess
from newpyproj.support import content_dict

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

folders = ['docs', 'tests']
root_files = ['.gitignore', 'README', 'LICENSE', 'setup.py']
project_files = ['__init__.py', 'support.py']
test_files = ['test_advanced.py', 'test_basic.py']

def parse_args(args: list) -> dict:
    """Parse command line arguments

    Best use is to import with the sys module: sys.argv[1:]
    * first element is script name

    Arguments:
        args {list} -- Arguments from the command line

    Returns:
        dict -- returns a dict with the parsed arguments
    """
    
    parser = argparse.ArgumentParser(prog='newpyproj', description='Creates a new python project folder')
    parser.add_argument('project_name', help='Creates a command line interface project')
    parser.add_argument('-c', '--cli', action='store_true', help='Creates a command line interface project')
    parser.add_argument('-g', '--gui', action='store_true', help='Creates a graphical user interface project')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-p', '--pytest', action='store_true', help='Use pytest as unittest')
    parser.add_argument('-r', '--resources', action='store_true', help='Include resources folder')
    parser.add_argument('-s', '--shebang', action='store_false', help='Supress shebang line in files')
    parser.add_argument('-t', '--tests', action='store_false', help='Supress test folders and files')
    parser.add_argument('-d', '--docs', action='store_false', help='Supress doc folders and files')
    parser.add_argument('--template', action='store_false', help='Supress template content in files')
    
    logging.info('Parsing arguments...')
    processed_args = parser.parse_args(args)
    final_dict = vars(processed_args)

    return final_dict

def create_folders(project_name: str, args: dict = {}) -> bool:
    """Creates project folders from a predefined list

    Arguments:
        project_name {str} -- Name of the python project

    Keyword Arguments:
        args {dict} -- Dictionary of the arguments (default: {{}})

    Returns:
        bool -- Folder creation status, True if all folders created
    """
    
    creation_status = True

    logging.info('Intializing folder creation...')
    creation_folders = folders.copy()
    creation_folders.append(project_name)

    if 'docs' in args and \
        args['docs'] == False:
        creation_folders.remove('docs')
        logging.info('Docs folder supressed...')
    if 'tests' in args and \
        args['tests'] == False:
        creation_folders.remove('tests')
        logging.info('Tests folder supressed...')
    if 'resources' in args and \
        args['resources'] == True:
        creation_folders.append('resources')
        logging.info('Resources folder included...')

    # check if not already inside folder with project name
    if os.path.split(os.getcwd())[1] != project_name:
        logging.info('Creating root project folder...')
        os.mkdir(project_name)
        creation_status = os.path.isdir(project_name)
        os.chdir(project_name)
    else:
        logging.info('Using current folder as root project folder...')

    for folder in creation_folders:
        logging.info(f'Creating {folder} folder...')
        os.mkdir(folder)
        creation_status = os.path.isdir(folder) if creation_status else creation_status

    return creation_status

def create_files(project_name: str, args: dict = {}) -> bool:
    """Creates project files from a predefined list

    Arguments:
        project_name {str} -- Name of the python project

    Keyword Arguments:
        args {dict} -- Dictionary of the arguments (default: {{}})

    Returns:
        bool -- File creation status, True if all files created
    """
    creation_status = True

    def open_files(file_list: list) -> bool:
        file_creation_status = True
        for file_name in file_list:
            logging.info(f'Creating {file_name}...')
            open(file_name, 'w').close()
            file_creation_status = os.path.isfile(file_name) if file_creation_status else file_creation_status
        
        return file_creation_status
    
    logging.info('Intializing file creation...')
    project_files_creation = project_files.copy()
    project_files_creation.append(project_name + '.py')

    root_files_creation = root_files.copy()
    if 'cli' in args and \
        args['cli'] == True:
        root_files_creation.append('cli.py')
        project_files_creation.append('cli.py')
    if 'gui' in args and \
        args['gui'] == True:
        root_files_creation.append('gui.py')
        project_files_creation.append('gui.py')

    # check if in root and folders exist
    if os.path.split(os.getcwd())[1] == project_name and \
        os.path.isdir(project_name):
        logging.info('--Root directory--')
        root_creation_status = open_files(root_files_creation)
        logging.info('--Project directory--')
        os.chdir(project_name)
        project_creation_status = open_files(project_files_creation)
        os.chdir('..')
        if 'tests' in args and args['tests'] == False:
            test_creation_status = True
        else:
            logging.info('--Tests directory--')
            os.chdir('tests')
            test_creation_status = open_files(test_files)
            os.chdir('..')
    else:
        raise OSError('Project folder not found')
    
    creation_status = root_creation_status and project_creation_status and test_creation_status

    return creation_status

def create_template(project_name: str, args: dict = {}):
    logging.info('Initiating template creation...')

    def append_content(file_name: str, folder: str = '', template: bool = True, shebang: bool = False):
        if shebang:
            logging.info('Inserting shebang in file...')
            open(os.path.join(folder, file_name),'a').write(content_dict['shebang'])
        if template:
            index = file_name.replace('.py', '').replace('.','').replace('__', '').lower()
            index = index + '2' if folder != '' and (index == 'cli' or index == 'gui') else index
            index = 'projectfile' if index == folder else index
            logging.info(f'Appending template content to {file_name} file...')
            open(os.path.join(folder, file_name), 'a'). write(content_dict[index].replace('[[projectname]]', project_name))

    if 'cli' in args and \
        args['cli'] == True:
        append_content(file_name='cli.py', template=args['template'], shebang=args['shebang'])
        append_content(file_name='cli.py', folder=project_name, template=args['template'], shebang=args['shebang'])
    if 'gui' in args and \
        args['gui'] == True:
        append_content(file_name='gui.py', template=args['template'], shebang=args['shebang'])
        append_content(file_name='gui.py', folder=project_name, template=args['template'], shebang=args['shebang'])
    if 'tests' in args and \
        args['tests'] == True:
        for item in test_files:
            append_content(item, 'tests', args['template'])
    for item in root_files:
        append_content(file_name=item, template=args['template'])
    
    append_content(project_name + '.py', project_name, args['template'], args['shebang'])
    
    for item in project_files:
        append_content(item, project_name, args['template'])


def initiate_git(project_name: str):
    """Initializes git in project folder

    Arguments:
        project_name {str} -- Name of the python project
    """

    # check if in root and folders exist
    if not os.path.split(os.getcwd())[1] == project_name or \
        not os.path.isdir(project_name):
        raise OSError('Project folder not found')
    try:
        logging.info('Initializing GIT...')
        subprocess.call(['git', 'init'])
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', 'First Commit'])
    except OSError:
        raise OSError('GIT not available')
    

def main():
    args = parse_args(sys.argv[1:])
    if args['verbose'] == True:
        logging.getLogger().setLevel(logging.INFO)
    logging.info('\n\nCreating project folder structure and files for your new python project')
    status1 = create_folders(args['project_name'], args)
    status2 = create_files(args['project_name'], args)
    create_template(args['project_name'], args)
    logging.info(f"\n\nFolders: {'ok' if status1 else 'error'} \nFiles: {'ok' if status2 else 'error'} \n")


if __name__ == '__main__':
    main()
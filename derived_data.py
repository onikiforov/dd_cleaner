#!/usr/bin/python
from tabulate import tabulate
import subprocess
import time
import argparse


dd_dir_name = 'DerivedData'
default_dir = '~'


def execute_shell(command, working_directory=None, stdout=None, stderr=None):
    p = subprocess.Popen([command], cwd=working_directory, shell=True, stdout=stdout, stderr=stderr)
    if stderr:
        stdout, stderr = p.communicate()
        return stdout, stderr
    elif stdout:
        output = p.stdout.read()
        return output
    else:
        p.wait()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        action="store_true",
        dest="force_flag",
        default=False,
        help='Flag to delete DerivedData without confirmation, default is False'
    )
    parser.add_argument(
        '-d',
        action="store",
        dest="check_directory",
        default=default_dir,
        help='Top level directory to search for DerivedData, default is "~"'
    )

    args = parser.parse_args()

    return args.check_directory, args.force_flag


def get_list_of_derived_data_locations(check_dir_name):
    print('Searching for DerivedData directories...')
    shell_result = execute_shell(
        'find {} -type d -name {} | xargs du -sh | gsort -hr'.format(check_dir_name, dd_dir_name),
        stdout=subprocess.PIPE
    )

    return shell_result.splitlines()


def clear_directory(dir_path):
    print('Deleting content of {}'.format(dir_path))
    execute_shell('rm -rf {}/*'.format(dir_path))


def prompt_to_delete():
    response = raw_input('Do you want to delete content of any DerivedData directory?\nEnter y or n\n')
    return response.lower() in ('yes', 'y')


def list_delete_options_dict(sorted_list):
    print('\nSearch is completed.\nPlease select directories(s) to clear:\n')
    print(tabulate([(item['index'], item['size'], item['path']) for item in sorted_list],
                   headers=['Index', 'Size', 'Path']))

    response = raw_input('\nEnter coma-separated numbers to clear specific directories, 0 to clear all directories, '
                         'or negative numbers to exclude specific directories from clearing targets\n')

    indexes = response.split(',')

    indexes = [int(x.strip(' ')) for x in indexes]

    if len(indexes) == 1 and indexes[0] == 0:
        sorted_list = [d['path'] for d in sorted_list]

    elif 0 in indexes or all(i < 0 for i in indexes):
        indexes_to_save = [abs(x) for x in indexes]
        if 0 in indexes:
            indexes_to_save.remove(0)
        modified_list = list(sorted_list)
        [modified_list.remove(item) for item in sorted_list if item['index'] in indexes_to_save]
        sorted_list = [d['path'] for d in modified_list]

    else:
        modified_list = list(sorted_list)
        [modified_list.remove(item) for item in sorted_list if item['index'] not in indexes]
        if modified_list == sorted_list:
            print('\nSeriously? Did you really think that typing all that numbers would be easier than entering \'0\'?')
        sorted_list = [d['path'] for d in modified_list]

    if not sorted_list:
        print('Nothing to delete!')
    else:
        return sorted_list


def confirm_action(list_of_dirs):
    print('I am going to delete content of next directories:\n')
    for dir_path in list_of_dirs:
        print(dir_path)
    response = raw_input('\nAre you sure?\nEnter y or n\n')

    return response.lower() in ('yes', 'y')


def form_dd_locations_dict(list_of_derived_data_locations):
    dd_list = []
    for dd_data in list_of_derived_data_locations:
        size, path = dd_data.split('\t')
        dd_list.append({'size': size, 'path': path})
    n = 1
    for item in dd_list:
        item['index'] = n
        n += 1

    return dd_list


def main():
    start_time = time.time()

    check_directory, force_flag = parse_args()
    list_of_derived_data_locations = get_list_of_derived_data_locations(check_directory)
    dd_loc_list = form_dd_locations_dict(list_of_derived_data_locations)

    formed_dict = None

    while not formed_dict:
        try:
            formed_dict = list_delete_options_dict(dd_loc_list)
        except IndexError:
            print('Make sure you didn\'t input number outside the scope!\n')
            continue
        except ValueError:
            print('Make sure you input numbers!\n')
            continue
        break

    print('\n')

    if formed_dict:
        if (not force_flag and confirm_action(formed_dict)) or force_flag:
            for dd_data in formed_dict:
                clear_directory(dd_data)
        else:
            print('\nNothing was cleared!')

    print("\n--- Execution time: {} seconds ---".format(time.time() - start_time))


if __name__ == '__main__':
    main()

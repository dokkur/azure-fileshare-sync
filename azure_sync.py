import os
import json
import sys
from azure.storage import CloudStorageAccount
from azure.storage.file import FileService
from azure.storage.file.models import Directory as AzureDirectory

file_service = FileService(os.environ['AZURE_STORAGE_ACCOUNT'], os.environ['AZURE_STORAGE_ACCESS_KEY'])

def process_dir(local_base_path, fileshare, directory, initial_dst):
    print("PROCESSING DIR ", directory)

    generator = file_service.list_directories_and_files(fileshare, directory)
    for file_or_dir in generator:
        azure_path = os.path.join(directory, file_or_dir.name)
        local_path = azure_path

        if initial_dst:
            local_path = azure_path.split(initial_dst)[1][1:]

        local_full_path = os.path.realpath(os.path.join(local_base_path, local_path))

        # if dir
        if type(file_or_dir) == AzureDirectory:
            subdir_generator = file_service.list_directories_and_files(fileshare, azure_path)

            process_dir(local_base_path, fileshare, azure_path, initial_dst)

            if not (os.path.exists(local_full_path)):
                print("DELETING... ", azure_path)
                file_service.delete_directory(fileshare, azure_path, fail_not_exist=True)

        # if file
        else:
            print("CHECKING LOCAL FILE ", local_full_path)
            if not (os.path.exists(local_full_path)):
                file_service.delete_file(fileshare, directory, file_or_dir.name)


def go(src, fileshare, dst):
    print("Creating volume {}".format(fileshare))
    res = file_service.create_share(fileshare)

    for path, subdirs, files in os.walk(src):
        for file_name in files:
            file_path = os.path.realpath(os.path.join(path, file_name))
            azure_dir = path[len(src) + 1:]
            azure_dir = os.path.join(dst, azure_dir) if azure_dir else dst
            print("{} -> to {} as {}".format(file_path, azure_dir, file_name))

            if len(azure_dir):
                dirs = azure_dir.split(os.sep)
                path = ''
                for d in dirs:
                    path = os.path.join(path, d)
                    print("trying to create {}".format(path))
                    file_service.create_directory(fileshare, path)

            res = file_service.create_file_from_path(fileshare, azure_dir, file_name, file_path)

    # removing old files
    process_dir(src, fileshare, dst, dst)


if __name__ == '__main__':
    src = sys.argv[1]
    remote = sys.argv[2]

    try:
        remote_parts = remote.split(os.sep)
        fileshare = remote_parts[0]
        dst = os.sep.join(remote_parts[1:])
    except IndexError:
        fileshare = remote
        dst = ''

    go(src, fileshare, dst)


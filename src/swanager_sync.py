import os
import sys
import json
import azure_sync

if __name__ == '__main__':
    config_file = sys.argv[1]
    remote = sys.argv[2]

    try:
        remote_parts = remote.split(os.sep)
        fileshare = remote_parts[0]
        base_dst = os.sep.join(remote_parts[1:])
    except IndexError:
        fileshare = remote
        base_dst = ''

    with open(config_file) as json_data:
        config = json.load(json_data)

    project_dir = os.path.dirname(os.path.realpath(config_file))

    for volume in config['volumes']:
        volume_src = volume['src']
        volume_dest = volume['dest'][1:]
        src = os.path.join(project_dir, volume_src)
        dst = os.path.join(base_dst, volume_dest)

        azure_sync.go(src, fileshare, dst)


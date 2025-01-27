import time

import fire
from monitors import SystemCallMonitor, FileMonitor


class Commands:

    def start(self, path_to_file_to_run=None, path_to_check_files_modification="/etc/"):
        if not path_to_file_to_run:
            print("Choose a file to run and check!")
            return

        file_monitor = FileMonitor(path_to_check_files_modification)
        system_call_monitor = SystemCallMonitor(path_to_file_to_run)

        file_monitor.start()
        system_call_monitor.start()
        time.sleep(40)


if __name__ == '__main__':
    fire.Fire(Commands)

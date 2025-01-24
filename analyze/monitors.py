import subprocess
import time
from abc import ABC, abstractmethod
from threading import Thread
import re
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Monitor(ABC, Thread):
    @abstractmethod
    def run(self):
        pass


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logger.info(f"File modified: {event.src_path}")

    def on_created(self, event):
        logger.info(f"File created: {event.src_path}")

    def on_deleted(self, event):
        logger.info(f"File deleted: {event.src_path}")


class FileMonitor(Monitor):
    def __init__(self, path_to_monitor):
        super().__init__()
        self._path = path_to_monitor
        self._event_handler = FileHandler()
        self._observer = Observer()
        self._observer.schedule(self._event_handler, path_to_monitor, recursive=True)

    def run(self):
        logger.info(f"Start monitoring {self._path}")
        self._observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.on_close()

    def on_close(self):
        logger.info(f"Stop monitoring {self._path}")
        self._observer.stop()
        self._observer.join()


class SystemCallMonitor(Monitor):

    SUSPICIOUS_PATTERNS = {
        "file_access": [r"/etc/passwd", r"/etc/shadow"],
        "network": [r"socket", r"connect"],
        "process": [r"execve", r"fork", r"clone"],
        "file_modification": [r"unlink", r"chmod", r"chown", r"write"]
    }

    def __init__(self, file_to_check):
        super().__init__()
        self._file_to_check = file_to_check

    def check_line_for_patterns(self, line):
        for category, patterns in self.SUSPICIOUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line):
                    logger.warning(f"[ALERT] Suspicious activity detected ({category}): {line.strip()}")
                    return True
        return False

    def run(self):
        process = None
        try:
            # Запуск strace с анализом системных вызовов
            process = subprocess.Popen(
                ["strace", "-f", "-e", "trace=all", self._file_to_check],
                stderr=subprocess.PIPE,
                text=True
            )

            logger.info(f"Monitoring {self._file_to_check} with strace...\n")

            # Чтение вывода strace в реальном времени
            while True:
                line = process.stderr.readline()
                if not line:  # Если данные закончились
                    break
                self.check_line_for_patterns(line)

            logger.info(f"Stop monitoring {self._file_to_check} with strace...\n")
        except KeyboardInterrupt:
            logger.info("\nMonitoring interrupted by user.")
        except Exception as e:
            logger.error(f"Error occurred: {e}", exc_info=e)
        finally:
            if process:
                process.terminate()

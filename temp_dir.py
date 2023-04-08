import os
import shutil
import tempfile


class TempDir(object):
    def __enter__(self, path='c:/temp/', delete_on_exit=False):
        self.name = tempfile.mkdtemp(prefix=path)
        self.delete_on_exit = delete_on_exit
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        if self.delete_on_exit or not os.environ.get('DEBUG'):
            shutil.rmtree(self.name)
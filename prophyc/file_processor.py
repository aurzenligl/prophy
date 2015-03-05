import os
from contextlib import contextmanager

class CyclicIncludeError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s included again during parsing" % path)

class FileNotFoundError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s not found" % path)

def _get_first_existing_path(leaf, dirs):
    for dir in dirs:
        path = os.path.join(dir, leaf)
        if os.path.exists(path):
            return path

@contextmanager
def push_dir(dirs, dir):
    try:
        dirs.insert(0, dir)
        yield dirs
    finally:
        dirs.pop(0)

@contextmanager
def swap_dir(dirs, dir):
    try:
        tmp = dirs[0]
        dirs[0] = dir
        yield dirs
    finally:
        dirs[0] = tmp

class FileProcessor(object):

    def __init__(self, process_content, include_dirs):
        self.process_content = process_content
        '''Function object accepting arguments (content, path, process_file)'''
        self.include_dirs = [_ for _ in include_dirs]
        self.files = {}
        '''Absolute paths are keys, values are results of process_content calls'''

    def __call__(self, path):
        return self.process_main(path)

    def process_main(self, path):
        '''Process main file.

        Can be called multiple times during file processor lifetime.
        '''
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with push_dir(self.include_dirs, os.path.dirname(path)):
            return self._process_file(path)

    def process_leaf(self, leaf):
        '''Process include file.

        It's meant to be called multiple times recurrentially by content processor.
        '''
        path = _get_first_existing_path(leaf, self.include_dirs)
        if not path:
            raise FileNotFoundError(leaf)
        with swap_dir(self.include_dirs, os.path.dirname(path)):
            return self._process_file(path)

    def _process_file(self, path):
        abspath = os.path.abspath(path)
        if abspath in self.files:
            if self.files[abspath] is None:
                raise CyclicIncludeError(path)
            return self.files[abspath]
        self.files[abspath] = None

        result = self.process_content(open(path).read(), path, lambda leaf: self.process_leaf(leaf))
        self.files[abspath] = result
        return result

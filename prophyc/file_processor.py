import os

class CyclicIncludeError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s included again during parsing" % path)

class FileNotFoundError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s not found" % path)

def get_first_existing_path(leaf, dirs):
    for dir in dirs:
        path = os.path.join(dir, leaf)
        if os.path.exists(path):
            return path

class FileProcessor(object):

    def __init__(self, process_content, include_dirs):
        self.process_content = process_content
        '''Function object accepting arguments (content, path, process_file)'''
        self.include_dirs = include_dirs
        self.files = {}
        '''Absolute paths are keys, values are results of process_content calls'''

    def __call__(self, path):
        return self.process_main(path)

    def process_main(self, path):
        '''Process main file.

        It's meant to be called once during file processor lifetime.
        '''
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        return self._process_file(path)

    def process_leaf(self, leaf):
        '''Process include file.

        It's meant to be called multiple times by content processor.
        '''
        path = get_first_existing_path(leaf, self.include_dirs)
        if not path:
            raise FileNotFoundError(leaf)
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

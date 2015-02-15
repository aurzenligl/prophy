import os

class CyclicIncludeError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s included again during parsing" % path)

class FileNotFoundError(Exception):
    def __init__(self, path):
        Exception.__init__(self, "file %s not found" % path)

class FileProcessor(object):

    def __init__(self, content_processor, include_dirs):
        self.content_processor = content_processor
        self.include_dirs = include_dirs
        # keys are file paths, values are None during processing
        # and assigned with content_processor return values after
        self.files = {}

    def __call__(self, path):
        '''Processes file and its possible includes.

        Call this function only once during processor lifetime.
        Further calls can only be made by enclosed content processor.
        '''

        if path in self.files:
            if self.files[path] is None:
                raise CyclicIncludeError(path)
            return self.files[path]

        if self.files:
            fullpath = self.get_full_path(path)
            if not fullpath:
                raise FileNotFoundError(path)
            path = fullpath
        else:
            if not os.path.exists(path):
                raise FileNotFoundError(path)

        self.files[path] = None # detects cyclic includes
        result = self.content_processor(open(path).read(), path, self)
        self.files[path] = result
        return result

    def get_full_path(self, path):
        for dir in self.include_dirs:
            fullpath = os.path.join(dir, path)
            if os.path.exists(fullpath):
                return fullpath

import os

class CyclicIncludeError(Exception):
    def __init__(self, filename):
        Exception.__init__(self, "file %s included again during parsing" % filename)

class FileNotFoundError(Exception):
    def __init__(self, filename):
        Exception.__init__(self, "file %s not found" % filename)

class FileProcessor(object):

    def __init__(self, content_processor, include_dirs):
        self.content_processor = content_processor
        self.include_dirs = include_dirs
        # keys are filenames, values are None during processing
        # and assigned with content_processor return values after
        self.files = {}

    def __call__(self, filename):
        '''Processes file and its possible includes.

        Call this function only once during processor lifetime.
        Further calls can only be made by enclosed content processor.
        '''

        if filename in self.files:
            if self.files[filename] is None:
                raise CyclicIncludeError(filename)
            return self.files[filename]
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        self.files[filename] = None # detects cyclic includes
        self.files[filename] = self.content_processor(open(filename).read(), filename, self)
        return self.files[filename]

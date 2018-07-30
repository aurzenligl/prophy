import os


class GeneratorBase(object):
    """
        The common task for a generator is to create files (in certain language)
        in an output_dir (passed to constructor) out of given model nodes.
    """

    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def localize(self, basename):
        return os.path.join(self.output_dir, basename)

    def serialize(self, nodes, basename):
        raise NotImplementedError("Abstract method not intended to call")

    @classmethod
    def write_file(cls, file_path, string):
        with open(file_path, "w") as f:
            f.write(string)

import os
import re

from prophyc.file_processor import FileProcessor

class InclContProc(object):
    def __call__(self, content, filename, file_processor):
        out = ''
        for line in content.splitlines():
            match = re.match('#include <([a-zA-Z0-9_./]*)>', line)
            if match:
                filename = match.groups()[0]
                out += file_processor(filename)
            else:
                out += line + '\n'
        return out

def test_file_processor_single_curdir(tmpdir_cwd):
    open('input.txt', 'w').write('the input\n')
    proc = FileProcessor(InclContProc(), [])
    assert proc('input.txt') == 'the input\n'

def test_file_processor_single_nestdir(tmpdir_cwd):
    os.mkdir('x')
    open('x/input.txt', 'w').write('nest input\n')
    proc = FileProcessor(InclContProc(), [])
    assert proc('x/input.txt') == 'nest input\n'

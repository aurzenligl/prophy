import os
import tempfile
import pytest

from prophyc.file_processor import FileProcessor

class JoinContentProcessor(object):
    def __call__(self, content, filename, file_processor):
        return ':'.join((filename, content))

def test_file_processor_single_curdir(tmpdir_cwd):
    open('input.txt', 'w').write('the input')
    proc = FileProcessor(JoinContentProcessor(), [])
    assert proc('input.txt') == 'input.txt:the input'

def test_file_processor_single_nestdir(tmpdir_cwd):
    os.mkdir('x')
    open('x/input.txt', 'w').write('nest input')
    proc = FileProcessor(JoinContentProcessor(), [])
    assert proc('x/input.txt') == 'x/input.txt:nest input'

import os
import re
import pytest
from prophyc.file_processor import FileProcessor, CyclicIncludeError, FileNotFoundError

def fake_process_content(content, path, process_file):
    out = ''
    for line in content.splitlines():
        match = re.match('#include <([a-zA-Z0-9_./]*)>', line)
        if match:
            include_path = match.groups()[0]
            out += process_file(include_path)
        else:
            out += line + '\n'
    return out

def test_file_processor_single_curdir(tmpdir_cwd):
    open('input.txt', 'w').write('the input\n')
    assert FileProcessor(fake_process_content, [])('input.txt') == 'the input\n'

def test_file_processor_single_nestdir(tmpdir_cwd):
    os.mkdir('x')
    open('x/input.txt', 'w').write('nest input\n')

    assert FileProcessor(fake_process_content, [])('x/input.txt') == 'nest input\n'

def test_file_processor_include_dirs(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    open('x/x.txt', 'w').write('one input')
    open('y/y.txt', 'w').write('other input')
    open('input.txt', 'w').write('''\
#include <x.txt>
#include <y.txt>
''')
    assert FileProcessor(fake_process_content, ['x', 'y'])('input.txt') == '''\
one input
other input
'''

def test_file_processor_main_file_not_found(tmpdir_cwd):
    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(fake_process_content, [])('nonexistent.txt')
    assert e.value.message == 'file nonexistent.txt not found'

def test_file_processor_include_file_not_found(tmpdir_cwd):
    open('main.txt', 'w').write('#include <incl.txt>')
    open('incl.txt', 'w').write('xxxx')
    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(fake_process_content, [])('main.txt')
    assert e.value.message == 'file incl.txt not found'

def test_file_processor_include_dir_precedence(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    os.mkdir('z')
    open('main.txt', 'w').write('#include <incl.txt>')
    def process():
        return FileProcessor(fake_process_content, ['z', 'y', 'x'])('main.txt')

    open('x/incl.txt', 'w').write('first')
    assert process() == 'first\n'

    open('y/incl.txt', 'w').write('second')
    assert process() == 'second\n'

    open('z/incl.txt', 'w').write('third')
    assert process() == 'third\n'

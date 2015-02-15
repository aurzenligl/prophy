import os
import re

from prophyc.file_processor import FileProcessor

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

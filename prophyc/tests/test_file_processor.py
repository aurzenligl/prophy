import os
import re
import pytest
from prophyc.file_processor import FileProcessor, CyclicIncludeError, FileNotFoundError

class FakeContentProcessor(object):

    def __init__(self):
        self.calls = 0

    def __call__(self, content, path, process_file):
        self.calls += 1
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
    assert FileProcessor(FakeContentProcessor(), [])('input.txt') == 'the input\n'

def test_file_processor_single_nestdir(tmpdir_cwd):
    os.mkdir('x')
    open('x/input.txt', 'w').write('nest input\n')

    assert FileProcessor(FakeContentProcessor(), [])('x/input.txt') == 'nest input\n'

def test_file_processor_include_dirs(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    open('x/x.txt', 'w').write('one input')
    open('y/y.txt', 'w').write('other input')
    open('input.txt', 'w').write('''\
#include <x.txt>
#include <y.txt>
''')
    assert FileProcessor(FakeContentProcessor(), ['x', 'y'])('input.txt') == '''\
one input
other input
'''

def test_file_processor_main_file_not_found(tmpdir_cwd):
    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(FakeContentProcessor(), [])('nonexistent.txt')
    assert e.value.message == 'file nonexistent.txt not found'

def test_file_processor_include_file_not_found(tmpdir_cwd):
    os.mkdir('x')
    open('main.txt', 'w').write('#include <incl.txt>')
    open('x/incl.txt', 'w').write('xxxx')
    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert e.value.message == 'file incl.txt not found'

def test_file_processor_main_self_include(tmpdir_cwd):
    open('main.txt', 'w').write('#include <main.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert e.value.message == 'file main.txt included again during parsing'

def test_file_processor_leaf_self_include(tmpdir_cwd):
    open('main.txt', 'w').write('#include <incl.txt>')
    open('incl.txt', 'w').write('#include <incl.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert e.value.message == 'file incl.txt included again during parsing'

def test_file_processor_cyclic_include(tmpdir_cwd):
    open('main.txt', 'w').write('#include <incl1.txt>')
    open('incl1.txt', 'w').write('#include <incl2.txt>')
    open('incl2.txt', 'w').write('#include <incl1.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert e.value.message == 'file incl1.txt included again during parsing'

def test_file_processor_include_dir_precedence(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    os.mkdir('z')
    open('main.txt', 'w').write('#include <incl.txt>')
    process = lambda: FileProcessor(FakeContentProcessor(), ['z', 'y', 'x'])('main.txt')

    open('x/incl.txt', 'w').write('first')
    assert process() == 'first\n'

    open('y/incl.txt', 'w').write('second')
    assert process() == 'second\n'

    open('z/incl.txt', 'w').write('third')
    assert process() == 'third\n'

def test_file_processor_nested_includes(tmpdir_cwd):
    open('main.txt', 'w').write('#include <incl1.txt>')
    open('incl1.txt', 'w').write('#include <incl2.txt>')
    open('incl2.txt', 'w').write('#include <incl3.txt>')
    open('incl3.txt', 'w').write('some text')

    assert FileProcessor(FakeContentProcessor(), ['.'])('main.txt') == 'some text\n'

def test_file_processor_include_already_parsed(tmpdir_cwd):
    open('main.txt', 'w').write('''\
#include <incl.txt>
#include <./incl.txt>
#include <././incl.txt>
''')
    open('incl.txt', 'w').write('text')

    fake = FakeContentProcessor()
    assert FileProcessor(fake, ['.'])('main.txt') == 'text\ntext\ntext\n'
    assert fake.calls == 2

def test_file_processor_multisegment_paths(tmpdir_cwd):
    os.makedirs('proj/include/x/y')
    open('proj/main.txt', 'w').write('''\
#include <a.txt>
#include <x/b.txt>
#include <x/y/c.txt>
''')
    open('proj/include/a.txt', 'w').write('one')
    open('proj/include/x/b.txt', 'w').write('two')
    open('proj/include/x/y/c.txt', 'w').write('three')
    assert FileProcessor(FakeContentProcessor(), ['proj/include'])('proj/main.txt') == 'one\ntwo\nthree\n'

def test_file_processor_main_directory_is_an_implicit_include_directory(tmpdir_cwd):
    os.mkdir('x')
    open('main.txt', 'w').write('#include <incl1.txt>')
    open('incl1.txt', 'w').write('some text')
    open('x/incl1.txt', 'w').write('wrong text')

    assert FileProcessor(FakeContentProcessor(), ['x'])('main.txt') == 'some text\n'

def test_file_processor_main_directory_implicit_include_directory_taken_over_by_successive_calls(tmpdir_cwd):
    os.mkdir('x')
    open('main1.txt', 'w').write('#include <incl1.txt>')
    open('incl1.txt', 'w').write('some text')
    open('x/main2.txt', 'w').write('#include <incl2.txt>')
    open('incl2.txt', 'w').write('some text') # this is intended not to be found

    processor = FileProcessor(FakeContentProcessor(), [])
    processor('main1.txt')

    with pytest.raises(FileNotFoundError) as e:
        processor('x/main2.txt')
    assert e.value.message == 'file incl2.txt not found'

def test_file_processor_leaf_directory_takes_over_as_an_implicit_include_directory(tmpdir_cwd):
    os.makedirs('x/y/z')
    open('main.txt', 'w').write('#include <x/incl1.txt>')
    open('x/incl1.txt', 'w').write('#include <y/incl2.txt>')
    open('x/y/incl2.txt', 'w').write('#include <z/incl3.txt>')
    open('x/y/z/incl3.txt', 'w').write('some text')

    assert FileProcessor(FakeContentProcessor(), [])('main.txt') == 'some text\n'

def test_file_processor_leaf_directory_takes_over_as_an_implicit_include_directory_error(tmpdir_cwd):
    os.mkdir('x')
    open('main.txt', 'w').write('#include <x/incl1.txt>')
    open('x/incl1.txt', 'w').write('#include <incl2.txt>')
    open('incl2.txt', 'w').write('some text')

    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert e.value.message == 'file incl2.txt not found'

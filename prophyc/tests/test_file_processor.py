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
    tmpdir_cwd.join('input.txt').write('the input\n')
    assert FileProcessor(FakeContentProcessor(), [])('input.txt') == 'the input\n'

def test_file_processor_single_nestdir(tmpdir_cwd):
    os.mkdir('x')
    tmpdir_cwd.join('x/input.txt').write('nest input\n')

    assert FileProcessor(FakeContentProcessor(), [])('x/input.txt') == 'nest input\n'

def test_file_processor_include_dirs(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    tmpdir_cwd.join('x/x.txt').write('one input')
    tmpdir_cwd.join('y/y.txt').write('other input')
    tmpdir_cwd.join('input.txt').write('''\
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
    assert str(e.value) == 'file nonexistent.txt not found'

def test_file_processor_include_file_not_found(tmpdir_cwd):
    os.mkdir('x')
    tmpdir_cwd.join('main.txt').write('#include <incl.txt>')
    tmpdir_cwd.join('x/incl.txt').write('xxxx')
    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert str(e.value) == 'file incl.txt not found'

def test_file_processor_main_self_include(tmpdir_cwd):
    tmpdir_cwd.join('main.txt').write('#include <main.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert str(e.value) == 'file main.txt included again during parsing'

def test_file_processor_leaf_self_include(tmpdir_cwd):
    tmpdir_cwd.join('main.txt').write('#include <incl.txt>')
    tmpdir_cwd.join('incl.txt').write('#include <incl.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert str(e.value) == 'file incl.txt included again during parsing'

def test_file_processor_cyclic_include(tmpdir_cwd):
    tmpdir_cwd.join('main.txt').write('#include <incl1.txt>')
    tmpdir_cwd.join('incl1.txt').write('#include <incl2.txt>')
    tmpdir_cwd.join('incl2.txt').write('#include <incl1.txt>')
    with pytest.raises(CyclicIncludeError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert str(e.value) == 'file incl1.txt included again during parsing'

def test_file_processor_include_dir_precedence(tmpdir_cwd):
    os.mkdir('x')
    os.mkdir('y')
    os.mkdir('z')
    tmpdir_cwd.join('main.txt').write('#include <incl.txt>')

    def process():
        return FileProcessor(FakeContentProcessor(), ['z', 'y', 'x'])('main.txt')

    tmpdir_cwd.join('x/incl.txt').write('first')
    assert process() == 'first\n'

    tmpdir_cwd.join('y/incl.txt').write('second')
    assert process() == 'second\n'

    tmpdir_cwd.join('z/incl.txt').write('third')
    assert process() == 'third\n'

def test_file_processor_nested_includes(tmpdir_cwd):
    tmpdir_cwd.join('main.txt').write('#include <incl1.txt>')
    tmpdir_cwd.join('incl1.txt').write('#include <incl2.txt>')
    tmpdir_cwd.join('incl2.txt').write('#include <incl3.txt>')
    tmpdir_cwd.join('incl3.txt').write('some text')

    assert FileProcessor(FakeContentProcessor(), ['.'])('main.txt') == 'some text\n'

def test_file_processor_include_already_parsed(tmpdir_cwd):
    tmpdir_cwd.join('main.txt').write('''\
#include <incl.txt>
#include <./incl.txt>
#include <././incl.txt>
''')
    tmpdir_cwd.join('incl.txt').write('text')

    fake = FakeContentProcessor()
    assert FileProcessor(fake, ['.'])('main.txt') == 'text\ntext\ntext\n'
    assert fake.calls == 2

def test_file_processor_multisegment_paths(tmpdir_cwd):
    os.makedirs('proj/include/x/y')
    tmpdir_cwd.join('proj/main.txt').write('''\
#include <a.txt>
#include <x/b.txt>
#include <x/y/c.txt>
''')
    tmpdir_cwd.join('proj/include/a.txt').write('one')
    tmpdir_cwd.join('proj/include/x/b.txt').write('two')
    tmpdir_cwd.join('proj/include/x/y/c.txt').write('three')
    assert FileProcessor(FakeContentProcessor(), ['proj/include'])('proj/main.txt') == 'one\ntwo\nthree\n'

def test_file_processor_main_directory_is_an_implicit_include_directory(tmpdir_cwd):
    os.mkdir('x')
    tmpdir_cwd.join('main.txt').write('#include <incl1.txt>')
    tmpdir_cwd.join('incl1.txt').write('some text')
    tmpdir_cwd.join('x/incl1.txt').write('wrong text')

    assert FileProcessor(FakeContentProcessor(), ['x'])('main.txt') == 'some text\n'

def test_file_processor_main_directory_implicit_include_directory_taken_over_by_successive_calls(tmpdir_cwd):
    os.mkdir('x')
    tmpdir_cwd.join('main1.txt').write('#include <incl1.txt>')
    tmpdir_cwd.join('incl1.txt').write('some text')
    tmpdir_cwd.join('x/main2.txt').write('#include <incl2.txt>')
    tmpdir_cwd.join('incl2.txt').write('some text')  # this is intended not to be found

    processor = FileProcessor(FakeContentProcessor(), [])
    processor('main1.txt')

    with pytest.raises(FileNotFoundError) as e:
        processor('x/main2.txt')
    assert str(e.value) == 'file incl2.txt not found'

def test_file_processor_leaf_directory_takes_over_as_an_implicit_include_directory(tmpdir_cwd):
    os.makedirs('x/y/z')
    tmpdir_cwd.join('main.txt').write('#include <x/incl1.txt>')
    tmpdir_cwd.join('x/incl1.txt').write('#include <y/incl2.txt>')
    tmpdir_cwd.join('x/y/incl2.txt').write('#include <z/incl3.txt>')
    tmpdir_cwd.join('x/y/z/incl3.txt').write('some text')

    assert FileProcessor(FakeContentProcessor(), [])('main.txt') == 'some text\n'

def test_file_processor_leaf_directory_takes_over_as_an_implicit_include_directory_error(tmpdir_cwd):
    os.mkdir('x')
    tmpdir_cwd.join('main.txt').write('#include <x/incl1.txt>')
    tmpdir_cwd.join('x/incl1.txt').write('#include <incl2.txt>')
    tmpdir_cwd.join('incl2.txt').write('some text')

    with pytest.raises(FileNotFoundError) as e:
        FileProcessor(FakeContentProcessor(), [])('main.txt')
    assert str(e.value) == 'file incl2.txt not found'

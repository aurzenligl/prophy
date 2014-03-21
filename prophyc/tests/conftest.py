import pytest
import string
import random
import sys
import os

sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

random.seed(1984)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

@pytest.fixture
def setup_file_to_read(request):
    f_name = "example_file_" + request.function.func_name + ".txt"
    f = open(f_name, "w")
    f.write(id_generator(24))
    return f_name

@pytest.yield_fixture
def tmpdir_cwd(tmpdir):
    orig_dir = os.getcwd()
    os.chdir(str(tmpdir))
    sys.path.insert(0, str(tmpdir))
    yield tmpdir
    sys.path.pop(0)
    os.chdir(orig_dir)

import pytest
import string
import random

random.seed(1984)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

@pytest.fixture
def setup_file_to_read(request):
    f_name = "example_file_" + request.function.func_name + ".txt"
    f = open(f_name, "w")
    f.write(id_generator(24))
    return f_name
from prophyc import model

def make_member(name, type_, array = None, optional = False):
    return model.StructMember(name, type_, model.Array(*array) if array else None, optional)

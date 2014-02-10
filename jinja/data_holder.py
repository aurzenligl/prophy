
class DataHolder(object):
    msg_dict={}
    typedef_dict={}
    constant_dict={}
    enum_dict={}
    struct_dict={}
    include_dict={}

    def sort_list(self,dic):
        out_list = []
        for key, val in dic.iteritems():
            if "_" not in val:
                out_list.insert(0,key)
            else:
                if val in out_list:
                    index = out_list.index(val)
                    out_list.insert(index + 1, key)
                else:
                    out_list.append(key)
        return out_list
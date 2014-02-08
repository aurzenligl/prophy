
class DataHolder(object):

    def set_msg_dict(self,msg_dict):
        self.msg_dict = msg_dict

    def set_typedef_dict(self,typedef_dict):
        self.typedef_dict = typedef_dict

    def set_constant_dict(self,constant_dict):
        self.constant_dict = constant_dict

    def set_enum_dict(self,enum_dict):
        self.enum_dict = enum_dict

    def set_struct_dict(self,struct_dict):
        self.struct_dict = struct_dict

    def set_include_list(self,include_list):
        self.include_list = include_list

    def get_msg_dict(self):
        return self.msg_dict

    def get_typedef_dict(self):
        return self.typedef_dict

    def get_constant_dict(self):
        return self.constant_dict

    def get_enum_dict(self):
        return self.enum_dict

    def get_struct_dict(self):
        return self.struct_dict

    def get_include_list(self):
        return self.include_list

import protophy


class LMGTT_ResetReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('spare',protophy.u32)]


class LMGTT_ResetResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Status',protophy.u32),
                    ('SubUnit',protophy.u32),
                    ('Cause',protophy.u32)]


class LMGTT_UserActivateReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('NumOfValidElements',protophy.u32),
                    ('UeId',protophy.u32),
                    ('NumOfSrbs',protophy.u32),
                    ('Srb_SrbId',protophy.u32),
                    ('NumOfDrbs',protophy.u32),
                    ('Drb_DrbId',protophy.u32)]


class LMGTT_UserActivateResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Status',protophy.u32),
                    ('SubUnit',protophy.u32),
                    ('Cause',protophy.u32)]


class LMGTT_UserDeactivateReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('NumOfValidElements',protophy.u32),
                    ('UeId',protophy.u32),
                    ('NumOfSrbs',protophy.u32),
                    ('Srb_SrbId',protophy.u32),
                    ('NumOfDrbs',protophy.u32),
                    ('Drb_DrbId',protophy.u32)]


class LMGTT_UserDeactivateResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Status',protophy.u32),
                    ('Subunit',protophy.u32),
                    ('Cause',protophy.u32)]


class LMGTT_UserSetupReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('NumOfValidElements',protophy.u32),
                    ('TargetForSrbs',protophy.u32),
                    ('CellIdForSrbs',protophy.u32),
                    ('CrntiForSrbs',protophy.u32)]


class LMGTT_UserSetupResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Subunit',protophy.u32),
                    ('Cause',protophy.u32)]
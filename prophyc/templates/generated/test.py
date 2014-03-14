import prophy 



TPoolId = prophy.u32
TNumberOfItems = prophy.u32
TAaSysComNid = prophy.u16

class EL2DeployableNode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EL2DeployableNode_Basic1',0), ('EL2DeployableNode_Basic2',1), ('EL2DeployableNode_Basic3',2), ('EL2DeployableNode_Basic4',3), ('EL2DeployableNode_Extended1',10), ('EL2DeployableNode_Extended2',11), ('EL2DeployableNode_Extended3',12), ('EL2DeployableNode_Extended4',13), ('EL2DeployableNode_Extended5',14), ('EL2DeployableNode_Extended6',15), ('EL2DeployableNode_Extended7',16), ('EL2DeployableNode_Extended8',17), ('EL2DeployableNode_ArmL2Master',20), ('EL2DeployableNode_ArmL2Slave',21), ('EL2DeployableNode_DcmLrcPsMaster',22), ('EL2DeployableNode_DcmLrcPsSlave',23)]

class SL2DeploymentInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('l2NodeType',EL2DeployableNode), ('nodeAddr',TAaSysComNid)]
class SL2PoolInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('poolId',TPoolId), ('numOfDeploymentInfo',TNumberOfItems), ('deploymentInfo',prophy.array(SL2DeploymentInfo,bound='numOfDeploymentInfo'))]

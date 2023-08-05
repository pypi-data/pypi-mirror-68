from localstack.utils.aws import aws_models
PHnYt=super
PHnYo=None
PHnYJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  PHnYt(LambdaLayer,self).__init__(arn)
  self.cwd=PHnYo
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,PHnYJ,env=PHnYo):
  PHnYt(RDSDatabase,self).__init__(PHnYJ,env=env)
 def name(self):
  return self.PHnYJ.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

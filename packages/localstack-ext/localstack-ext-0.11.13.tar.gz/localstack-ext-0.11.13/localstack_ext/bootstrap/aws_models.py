from localstack.utils.aws import aws_models
qdSzY=super
qdSzL=None
qdSzU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qdSzY(LambdaLayer,self).__init__(arn)
  self.cwd=qdSzL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,qdSzU,env=qdSzL):
  qdSzY(RDSDatabase,self).__init__(qdSzU,env=env)
 def name(self):
  return self.qdSzU.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

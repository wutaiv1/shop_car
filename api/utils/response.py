
# 继承该类后，具有一些属性，对这些属性进行替换，对象的方式，更加的简单
class BaseResponse(object):

    def __init__(self):
        self.code = 1000
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__

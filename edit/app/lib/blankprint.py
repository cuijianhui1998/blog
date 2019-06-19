'''
本文件是对蓝图一个拓展,随着项目越来越大,我感觉虽然有蓝图的帮助我们对对象分类,
但是仍然感觉文件的耦合度太高,所以自定义了一个类似于蓝图的节点,取名为blankprint(源于慕课课程)
'''



class BlankPrint():
    def __init__(self,name):
        self.name = name
        self.mound = []

    def route(self,rule,**options):
        def decorator(function):
            self.mound.append((function,rule,options))
            return function
        return decorator

    def register(self,blueprint,url_prefix=None):
        if url_prefix is None:
            url_prefix = '/'+self.name
        for function,rule,options in self.mound:
            endpoint = options.pop('endpoint',function.__name__)
            blueprint.add_url_rule(url_prefix+rule,endpoint,function,**options)
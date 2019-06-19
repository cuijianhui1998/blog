from enum import Enum,unique

@unique
class BlogTypeEnum(Enum):
    pythonBase = 1001
    pythonProcess = 1002
    pythonNew = 1003
    flask = 1011
    Django = 1012
    tornado = 1013
    html5 = 1021
    css = 1022
    javascript = 1023
    allIsFile = 1031
    install = 1032

'''
在使用markdown前,我们需要了解一些他的扩展
markdown.extensions.extra 额外添加的扩展
markdown.extensions.abbr 缩略语
markdown.extensions.attr_list 属性列表
markdown.extensions.def_list  定义列表
markdown.extensions.fenced_code 受控代码块
markdown.extensions.footnotes 脚注
markdown.extensions.tables 表格
markdown.extensions.admonition 警告
markdown.extensions.codehilite 代码块
markdown.extensions.legacy_attr :Legacy Attributes
markdown.extensions.legacy_em   :Legacy Emphasis
markdown.extensions.meta    元数据
markdown.extensions.nl2br   新的中断线
markdown.extensions.sane_lists  Sane Lists
markdown.extensions.smarty  SmartyPants
markdown.extensions.toc :Table of Contents
markdown.extensions.wikilinks   :WikiLinks  wiki连接
'''
from markdown import Markdown,markdown
from markdown.preprocessors import Preprocessor #前置处理器
from markdown.postprocessors import Postprocessor   #后置处理器

from markdown.extensions import Extension   #扩展的基类


#如果我们需要重新设置转义的字符
class MyMarkdown(Markdown):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #设置不被转义的字符
        self.ESCAPED_CHARS = ['\\', '*','`', '_', '{', '}', '[', ']',
                              '(', ')', '>', '#', '+', '-', '.', '!']




#下面是抄袭了别人的作为示例,以供我自己添加拓展


#前置处理器
class CodePreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        flag_in = False
        block = []
        for line in lines:
            if line[:3] == '!!!':
                flag_in = True
                block.append('<pre class="brush: %s;">' % line[3:].strip())
            elif flag_in:
                if line.strip() and line[0] == '!':
                    block.append(line[1:])
                else:
                    flag_in = False
                    block.append('</pre>')
                    block.append(line)
                    new_lines.extend(block)
                    block = []
            else:
                new_lines.append(line)
        if not new_lines and block:
            new_lines = block
        return new_lines
##后置处理器
class CodePostprocessor(Postprocessor):
    def run(self, text):
        t_list = []
        for line in text.split('\n'):
            if line[:5] == '<p>!<':
                line = line.lstrip('<p>').replace('</p>', '')[1:]
            t_list.append(line)
        return '\n'.join(t_list)

class CodeExtension(Extension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        ##注册扩展，用于markdown.reset时扩展同时reset
        md.registerExtension(self)

        ##设置Preprocessor
        # print md.preprocessors.keys()
        md.preprocessors.register(CodePreprocessor(md), 'code_pre', 20)
        # md.postprocessors.register(MyButtonPreprocessor(md),'mybutton',26)

        ##设置Postprocessor
        # print md.postprocessors.keys()
        md.postprocessors.register(CodePostprocessor(md), 'code_post', 8)

#最后的使用
#示例
text= '''
!!!python!!!
!def foo():
###title
<p>!<sjadghhjdas</p>
'''
myext = CodeExtension()
md = markdown(text, extensions=[myext,])
print(md)
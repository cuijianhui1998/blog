import csv,codecs

from flask import redirect,url_for,request
from werkzeug.utils import secure_filename
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView,AdminIndexView,expose
from flask_admin._compat import csv_encode
from flask import Response, stream_with_context
from flask_login import current_user


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            if current_user.username=='admin' :
                return self.render(self._template)
            return redirect(url_for('web.index'))
        return redirect(url_for('web.login'))





class ArticleView(ModelView):
    '''
    重写了flask_admin中的一些设置
    '''
    can_create = True
    can_edit = False
    can_export = True
    can_delete = True
    create_template = 'control/publish.html'
    #修改编辑该模型的模板
    # edit_template = 'control/update.html'
    #显示的字段
    column_list = ['id','title','poster','author','select','is_recommend','create_time']
    #可排序的字段
    column_sortable_list = ['create_time','id']
    #默认排序的字段
    column_default_sort  = 'create_time'
    #每一页的数量
    page_size = 15

    def _export_csv(self, return_url):
        """
            Export a CSV of records as a stream.
            这是我抄袭了别人的
        """
        count, data = self._export_data()

        # https://docs.djangoproject.com/en/1.8/howto/outputting-csv/
        class Echo(object):
            """
            An object that implements just the write method of the file-like
            interface.
            """

            def write(self, value):
                """
                Write the value by returning it, instead of storing
                in a buffer.
                """
                return value

        #
        writer = csv.writer(Echo())

        def generate():
            # Append the column titles at the beginning
            titles = [csv_encode(c[1]) for c in self._export_columns]
            titles[0] = codecs.BOM_UTF8.decode("utf8") + codecs.BOM_UTF8.decode() + titles[0]
            yield writer.writerow(titles)

            for row in data:
                vals = [csv_encode(self.get_export_value(row, c[0]))
                        for c in self._export_columns]
                yield writer.writerow(vals)

        filename = self.get_export_name(export_type='csv')

        disposition = 'attachment;filename=%s' % (secure_filename(filename),)

        return Response(
            stream_with_context(generate()),
            headers={'Content-Disposition': disposition},
            mimetype='text/csv'
        )





# class AdminCreateBlogView(BaseView):
#     '''
#     这是一个用于后台创建博客的视图函数,路径是 '/admin/admincreateblogview'
#     也就是admin加上类名的全小写;
#     expose中路由的路径必须是'/',不可改变,,最后通过render返回HTML页面
#     '''
    #由于我在ArticleView中添加了create_templates,所有这里重复了
    # @expose('/')
    # def index(self):
    #     return self.render('control/publish.html')


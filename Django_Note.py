# -*- coding: utf-8 -*-
__author__ = 'xzq'

'''
1. Django项目框架:
                DjangoWeb
                    |---- DjangoWeb
                       |--- settings.py   # 配置文件
                       |--- urls.py      # url管理系统
                       |--- wsgi.py      # wsgi服务器接口
                    |---- templates      # 模板
                    |---- app            # 具体app
                       |--- migrations      # 迁移
                       |--- static          # 静态文件(js,css,img)
                       |--- admin.py        # 数据库管理
                       |--- apps.py         #
                       |--- models.py       # 连接数据库, 操作数据
                       |--- test.py
                       |--- views.py        # 视图函数
                       |--- urls.py         # 属于该app的url分系统
2. 基本命令:
          1>. python manage.py startapp  app_name    # 创建app
              # 创建新的app后, settings中注册
                INSTALLED_APPS = [
                    'blog.apps.BlogConfig',
                ]
          2>. python manage.py runserver  ip:port   # 运行项目
          3>. python manage.py makemigrations       # 生成数据库表单文件
          4>. python manage.py migrate              # 创建数据库表单
'''  # Django项目框架

'''
3. 基本MVC流程:
             1>. urls.py 中路由选择, 分配视图函数   (C)
             
             2>. views.py 中具体实现逻辑           (V)
                 1>>. 返回render渲染的模板
                     return render(req, 'test.html', {'模板变量':'python变量'})
                 2>>. 直接返回HTTPResponse
                     return HTTPResponse('data')
                 3>>. 取GET数据
                      req.method                # 前端提交方式
                      req.GET.get('key')
                 4>>. 取POST数据
                      req.POST.get('key')   
                      #  将settings.py中的先关闭
                      # 'django.middleware.csrf.CsrfViewMiddleware',              # django 对post的表单做安全检测，先暂时关闭     
                 5>>. 一个Request一定要对应一个Response, 请求一定要回应    
             3>. templates 操作html模板           (T)
                1>>. html中的静态文件在static中
                2>>. 静态文件的路径在settings.py中配置
                ##整个templates的渲染过程在wsgi服务器(后端)中进行，而js,css等静态文件的渲染在前端中进行
                
             4>. models.py 中操作数据库            (M)    
                           
'''  # 基本MVC流程

'''
4. 静态文件路径配置:
           1>. 静态文件配置
           /******** settings.py *****************/
           STATIC_URL = '/static/'              # 别名, 前端默认静态文件的虚拟路径
 
           STATICFILES_DIRS = (
              os.path.join(BASE_DIR, 'blog/static'),          # 配置静态文件的真实路径
           )
           
           2>. 在html文件中的调用方式
              1>>. 写死的
                   <script src="/static/jquery-3.1.1.js"></script>    # 只能调用jquery-3.1.1.js
              
              2>>. 通过模板动态调用
                   {% load staticfiles %}     # html头文件中导入
                   <script src="{% static 'jquery-3.1.1.js' %}"></script>

'''  # 静态文件路径配置

'''  
5. url系统:  urls.py
           1>. 导入 from django.conf.urls import url
           2>. 基本格式:
                     urlpatterns = [
                        url(正则表达式, views视图函数，参数，别名),
                     ]
           url分类:
               3>. 无命名分组:
                   url(r'^article/(\d{4})/(\d{2})',views.article),       # 无命名分组，注意article视图函数要传参
               
               4>. 有命名分组:
                   url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})',views.article),  # 有命名分组, 视图函数一定要按前端命名要求传参
               
               5>. 别名: 不将前端url写死
                   1>>. 供前端表单使用，不会将前端url写死
                        url(r'^register/', views.register, name='reg')   # 别名
                   2>>. 通过模板动态调用
                        <form action="{% url 'reg' %}" method="post">
                   3>>. 模板中传参
                         {% url 'reg' param1 param2 %}                 # 此时是无名分组传参，要命名在url系统中命名
                   
           urls分流:  
               1>. DjangoWeb项目urls.py中为主系统
                   urlpatterns = [
                        path('admin/', admin.site.urls),
                        path('blog/', include('blog.urls'))   # 通过include('blog.urls') 导入
                   ]
               2. 具体app中(如blog)urls.py 为分系统
                   urlpatterns = [
                    url(r'userInfo/',views.userInfo),
                    url(r'^article/(\d{4})/(\d{2})',views.article),       # 无命名分组
                    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})',views.article),  # 有命名分组
                    url(r'^register/', views.register, name='reg')   # 别名
                   ]
               
               # 浏览器访问时:
                  # http://127.0.0.1:8080/blog/register/
'''  # url系统

'''
6. 视图函数: views.py
          1>. HTTPRequest 和 HTTPResponse 对象:  django.http
              * 一个Request一定要回应一个Response
              1>>. HTTPRequest属性方法:
                    属性:   .path    # 全局路径, 不包括域名
                           .method  # 前端提交页面的方法, 全部大写 GET POST
                           .GET     # 包含所有HTTP GET参数的类字典对象 keys和values都是字符串
                           .POST    # 包含所有HTTP POST参数的类字典对象 keys和values都是字符串
                           .COOKIES # 包含所有cookies的包含所有cookies的标准Python字典对象；keys和values都是字符串
                           .FILES   # 包含所有上传文件的类字典对象, 每一个value同时也是一个标准的python字典对象
                                      value = {
                                         filename:      上传文件名，用字符串表示
                                         content_type:   上传文件的Content Type, 字符串
                                         content:       上传文件的原始内容
                                      }
                           .user
                           .session
                    
                    方法:  .get_full_path()   # 全路径+url提交值 
              
              2>>. HTTPResponse:  
                   ** 每个view请求处理方法必须返回一个HttpResponse对象               
                      return  HTTPResponse('str')
                      1>>. 页面渲染:
                          return  render('模板.html', context_dir)
                          # return  render_to_response('模板.html', context_dir, context_instance=RequestContext(req))
                      2>>. 页面跳转:
                          return redirect('url')      # 如果要传参通过url/?message=%s 传参给另一个视图函数
                          
                          ret = redirect('url')       # 也可以通过cookie
                          ret.set_cookie(键，值)       
                      render和redirect的区别:   render 没有页面跳转, 虽然显示了别的页面，但还是当前url
                      
'''  # views.py 视图函数 HTTPRequst 和 HTTPResponse

'''
7. 模板:  Template + Context
       1. 基本流程:
           from django.template import Template, Context
           from django.template.load import get_template
           1>. 具体过程
               # t = Template('<h1>My name is {{name}}</h1>')
               t = get_template('name.html')
               c = Context({'name':'xzq})
               html = t.render(c)
               return HTTPResponse(html)
           2>. 简写:
              return render(req, 'name.html', {'name':'xzq'})
       
       2. Template支持的变量类型:
          1>. Template中的变量定义: {{ variable }}
          2>. 支持的类型: 基本变量类型(num, str, boolean)
                         类对象或对象类型(list, dict, obj)
          3>. 深度变量查找:  .attr 或 .func (不能传参)
          
       3. Template过滤器:
          1>. Template中定义过滤器:  {{obj|filter[:param]}}
          2>. filter类型:   add: num                # 给变量加上相应的值
                           cut: 'str'              # 移除变量中的指定字符
                           date: 'Y-m-d-H-M-S'     # 指定日期格式 %Y年 %m月 %d日 %X时间(%H时 %M分 %S秒) %a星期
                           default: 0              # 变量为False, 指定默认值
                           default_if_none: 0      # 变量为None, 指定默认值
                           safe                    # 申明变量为安全, 可以翻译成html   
          
       4. Template控制语句:
          1>. 语法:  {% tag %}
          2>. if语句: 
                      {% if condition1 %}
                         # pass
                      {% elif condition2 %}
                         # pass
                      {% else %}
                      {% endif %}
                      # 支持 and or not
          3>. for语句: 
                     {% for item in list,dict %}
                        # pass
                     {% endfor %}
                     * 不支持break 和 continue
                     * 用 forloop提供循环信息:       forloop.counter     # 循环计数 1 开始
                                                   forloop.counter0    # 循环计数 0 开始
                                                   forloop.first       # 第一次循环为true
       
       5. 其他:
          1>. url语句:
                     {% url 'reg' %}          # 引用路由配置 
                     
          2>. 表单验证:
                     {% csrf_token %}        # 会在wsgi服务器中渲染成input标签, 其值为提交的钥匙. 表单在提交时服务器会先验证该钥匙，正确则让提交。
                                             # 防止跨站攻击验证
          3>. 变量重命名:
                     {% with local_name = input_name %}
                       {{ local_name }}
                     {% endwith %}
          
          4>. 禁止wsgi服务器渲染:
                     {% verbatim %}
                        {{ hello }}
                     {% endverbatim %}
          
          5>. 加载标签库:  {% load %}
'''  # template 模板基础，基本语句，过滤器，tag

'''
*1. 自定义filter和tag:
               1>. 自定义filter:
                                  1>>. app中创建templatetags模块
                                  2>>. 创建任意myTag.py文件
                                  3>>. from django import template
                                       register = template.Library()   #register的名字是固定的,不可改变
                                       
                                       @register.filter                # 自定义过滤器, 只能传参一个
                                       def filter_multi(t1, t2):
                                            return t1 * t2 
                                  /************template***************/
                                  {% load myTag %}                       #  加载自定义标签库
                                  <h1> {{ test|filter_multi:3 }}</h1>    #  调用自定义标签
                      
               2>. 自定义tag:   1> - 3> 一样
                                  from django.utils.safestring import mark_safe   # 导入安全声明函数
                                  
                                  @register.simple_tag                            # 自定义标签, 不限制参数， 但不能用在控制语句里面
                                  def simple_tag_multi(v1,v2):
                                        return  v1 * v2  
                                  
                                  @register.simple_tag
                                  def my_input(id,arg):
                                        result = "<input type='text' id='%s' class='%s' />" %(id,arg,)
                                        return mark_safe(result)                  # 相当于filter中的 safe 声明 
                                        
                                   /************template***************/
                                  {% load myTag %}                       #  加载自定义标签库
                                  {% my_input %}
                                  {% simple_tag_multi %}

*2. 模板继承:
           /**********父类模板中********/
           <h1>{% block content %}Hello{% endblock %}</h1>      # 子类只能改内容
           {% block content %}<h1>>Hello</h1>{% endblock %}     # 子类还可以改布局
           # block 不能重名
           
           1. {% extends 'base.html' %}  # 导入父类模板
           
           2. {% block title %}My Title {% endblock %}   # 重写父类block部分
           
           3. {% block content %}
                  {{ block.super }}                      # 调用父类block部分
              {% endblock %}
              
*3. 模板包含:
           {% include %} 允许在模版中包含其他模版的内容
           {% include 'include/nav.html'%}       # 这里'nav.html'是写好的模板块文件              
'''  # 模板，自定义filter和tag, 模板继承

'''
8. 数据库: models.py
         1>. django 默认支持 sqlite, mysql, oracle, postgresql
         2>. django 默认使用 sqlite, 其数据库orm引擎为 django.db.backends.sqlite3
         3>. django 连接mysql:
                 1>>. 更改settings.py 的 DATABASES:
                          DATABASES = {
                            'default': {
                                'ENGINE': 'django.db.backends.mysql',       # mysql的数据库orm引擎
                                'NAME': 'django_orm',                       # 要连接的数据库名称
                                'USER': 'root',                             # 数据库用户名
                                'PASSWORD': '123456',                       # 数据库密码
                                'HOST': '',                                 # 数据库主机，留空默认为localhost
                                'PORT': '3306',                             # 数据库端口
                             }
                          }
                 2>>  更改django的数据库驱动文件(python-mysql-connection): 
                        MySQLdb(django默认使用, python2) --->  pymysql(python3)
                     /***********DjangoWeb.__init__.py********************/
                     import pymysql
                     pymysql.install_as_MySQLdb()
                     
                 ** Python36错误处理:
                    django.db.backends.mysql.base.py
                    1. 注释:
                        if version < (1, 3, 13):
                        raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
                    
                    django.db.backend.mysql.operations.py    
                    2. 更改: 146-147
                        # query = query.decode(errors='replace')
                        query = query.encode(errors='replace')
'''  # models 数据库, 连接mysql

'''
Admin: 数据库管理
      1. 注册model到admin:  1) admin.site.register(Book)
                           2) @admin.register(Book)
      
      2. admin定制: 1) class myAdmin(admin.ModelAdmin)
                   2) @admin.register(Book,myAdmin)
                                           
'''  # Admin

'''
Model组件: 
         (字段)作用: 1. 后端建表
                    2. 限制并验证admin输入的数据类型 
         使用:   在models.py中创建表 
                每一张表是一个类class, 表的每一项数据是这个类的对象obj
                class Table(model.Models):
                     field = model.Field     
                
                1. Field类型: 1) 后端数据库有的字段 2) Admin额外提供验证的字段
                  
                   字段名                参数                         数据库中存储类型
                   /*************** 后端数据库有的字段 **************************/
                   AutoField(Field)     primary_key                 # INT PRIMARY KEY AUTO_INCREMENT
                   IntegerField(Field)     /                        # INT
                   BooleanField(Field)     /                        # TINYINT(1)
                   CharField(Field)      maxlength                  # VARCHAR(max_length)
                   FloatField(Field)       /                        # DOUBLE
                   DecimalField(Field)  max_digits(总位数)           # DECIMAL 
                                        decimal_places(小数位长度)                 
                   TextField(Field)        /                        # LONGTEXT
                   DateField(Field)        /                        # DATE // YYYY-MM-DD
                   DateTimeField(DateField) /                       # DATETIME // YYYY-MM-DD HH:MM:SS 
                   TimeField(DateField)     /                       # TIME     // HH:MM:SS   
                   
                   /**************** Admin额外提供验证的字段 **********************/  
                   EmailField(CharField)   /                        # VARCHAR
                   URLField(CharField)     /                        # VARCHAR
                   IPAddressField(Field)   /                        # CHAR(15)
                   FileField(Field)       upload_to='地址'           # VARCHAR 
                   ImageField(FileField)  upload_to='地址'           # VARCHAR
                                          width_field=None, height_width=None
                   
                                       
'''  # Model组件: 字段

'''
Model字段参数的作用:
                  1. 限制约束数据
                     null = False                         # NOT NULL
                     default = None                       # DEFAULT = None
                     primary_key = True                   # PRIMARY KEY
                     unique = True                        # UNIQUE
                     db_index = True                      # INDEX
                  
                  2. 用于admin显示
                     verbose_name                         # admin中显示的字段名
                     help_text                            # admin中显示的帮助信息
                     choices = [(0,'上海'),(1,'北京'),]    # admin中的选择框
                     blank                                # admin中是否可为空
                     editable                             # admin中是否可编辑
             
                  3. 错误信息反馈
                     error_messages = {
                            '字段参数':'错误反馈',
                            'invalid': '格式错误',    # 正则校验错误
                     } 
                  4. 自定义验证
                     validators = []
元信息:
      class UserInfo(models.Model):
           nid = models.AutoField(primary_key=True)
           user = models.CharField(max_length=20)
           class Meta:
                 db_table = 'table_name'                # 数据库中的自定义表名字
                 index_together = [('nid','user')]      # 建立联合索引
                 unique_together = [('nid','user')]     # 建立联合唯一索引
                 verbose_name = 'table_name'            # admin中显示的表名字             
'''  # Model组件: 字段参数, 元信息

'''
一对多: 多的那方为子表, 设置外键                    
       fk = models.ForeignKey(                  # django默认创建为 fk_id
            to='主表名',                         # 可不加to 
            to_field='主表字段名',                # 默认为主表的主键
            on_delete='级联方式',                # models.CASCADE       // 父表删除，子表对应删除
                                                # models.SET_NULL      // 父表删除，子表对应置空，前提是允许置空（默认不允许置空）
                                                # models.SET_DEFAULT   // 父表删除，子表对应置为默认值，前提是有默认值(default)
                                                # models.PROTECT       // 子表有数据，父表不允许删除，否则报错  
            related_name='反向操作的manager'     # 用于代替反向操作的manager, obj.child_set
            db_constraint = True                # 是否创建约束
            )

一对一: 一对多 + 唯一索引
       oto = models.OneToOneField(
             to = '主表名',                    # 可不加to
             to_field = '主表字段名',           # 默认为主表的主键
             on_delete = '级联方式',
            )
            
多对多: 两个一对多
       1. 自动创建: 可用manager修改数据
               mtm = models.ManyToManyField(
                     to = '主表名',
                     related_name= '反向操作的manager',
                     db_constraint = True,                 # 是否对第三张表创建约束
                     db_table = None,                      # 第三张表名 
                    )       
       2. 手动创建: 手动修改数据
               1>. 自定义第三表
                   class Table_name(models.Model):
                      u = models.ForeignKey(Table_1)
                      t = models.ForeignKey(Table_2)
               2>. mtm = models.ManyToManyField(
                       to = '主表名',
                       related_name = '反向操作的manager',
                       through = '自定义的第三张表',       # 用于指定关系表 
                       through_fields= ['u','t']         # 用于指定关系表中那些字段做多对多关系表
                    ) 
自关联: 
    1. 多对多:      
           class User:
               d = models.ManyToManyField('self',related_name='b')       # 用户互粉
    2. 一对多:
               d = models.ForeignKey(User,related_name='b')  # 评论楼                 
               
'''  # Model组件: 一对多, 一对一， 多对多

'''           
1. 创建表:         python manage.py makemigrations     # 创建model迁移文件
                  python manage.py migrate            # 迁移model至数据库生成具体表  

2. 修改表, 重新跑一遍
3. 删除表:
         1>. 先到数据库把表删掉：drop table 
         2>. 注释django中对应的model
         3>. 执行以下命令:
                 python manage.py makemigrations
                 python manage.py migrate --fake
         4>. 写入新的model:
         5>. 重新迁移   


4. 配置日志文件:
   /************* settings.py ****************/
   LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'propagate': True,
                'level':'DEBUG',
            },
        }
    }     
         
'''  # Model组件: 创建表, 修改表, 删除表, 配置日志文件

'''
ORM单表操作:  在views.py里面
             from models import *
             
             t = Table()               # 表单对象model是一个表记录, model只有attrs和save()
             manager = Table.objects   # 表单的一个类属性是一个Manager对象, 用于管理表记录对象model
             
             1. 增加记录
                1>. 方式一: 创建表记录对象, 并添加
                         t = Table(**info)
                         t.save                    # 此时才会提交到数据库
                2>. 方式二: 通过Manager对象添加
                         Table.objects.create(**info) # 直接提交到数据库
                         
             2. 查询表记录: 通过manager操作
                QuerySet是model的集合对象: 1) 可迭代
                                         2) 可切片
                                         3) 不会马上执行, 运行时执行, 并将数据存入QuerySet内置的cache
                                         4）再次执行时从cache中拿数据
                                     * 只需要判断数据有无, 用.exist()方法
                                     * 当读取数据特别大时, 用.iterator()方法, 但数据不会存入cache
                                     * 对于常用的数据, 存入cache; 不常用的用iterator()    
                
                .all()                   # SELECT * FROM Table, 查询全部, 返回QuerySet
                .filter(**kwargs)        # SELECT * FROM Table Where condition, 条件查找, 返回QuerySet
                .get(**kwargs)           #                                    , 只能查找一个, 有多个或没有则报错, 返回model, 没有数据处理的方法
                 
                condition:   
                        * 原始django_orm只有与','  没有或非 ---> 引入Q查询
                        * from django.db.models import Q
                        * Q(condition) 封装过的条件可以有 & | ~
                        * Q查询可以与原始查询一起使用, 但一定要放在最前面 
                        
                        >a          # field__gt = a
                        <a          # field__lt = a
                        >=a         # Q(field__gt=a) | Q(field=a)
                        <=a         # Q(field__lt=a) | Q(field=a)
                        between a and b       # field__range=[a,b]
                        in (a,b,c)            # field__in=[a,b,c]
                        like= '%a%'           # field__contains=a, 区分大小写； field_icontains=a, 不区分大小写
                        正则                   # field__regex = r'',  区分大小写； field_iregex= r'',  不区分大小写
                        
                        其他双下划线方法:  __startswith, __istartswith, __endswith, __iendswith
                
                /***************** 查询后的数据处理 *************************************/                              
                .values(*field)             # SELECT field,field2,..  返回一个ValueQuerySet集合, 且每项是一个{field:value,}字典
                .values_list(*field)        #                                                    每项是一个(value1,value2,)元组
                // 去重
                    .distinct()                 # SELECT DISTINCT..       
                // 排序
                    .order_by(*field)           # .. ORDER BY field1,..   升序
                    .order_by(-*field)          #                         降序
                    .order_by(*field).reverse() #                         反转
                // 聚合
                    from django.db.models import Avg, Min, Max, Sum, Count
                    .aggregate(Avg('field'))  
                // 分组聚合
                    .values(*field).annotate([my_name]=Avg('field2'))    # SELECT field1, field2, Avg(field) FROM Table GROUP BY field2
                
                其他处理方式: .count()           # 计数 
                            .first(), .last()  # 取第一个或取最后一个
                            .exist()           # 若查找存在数据则返回True, 判断数据是否存在可用, 不需要读取全部数据, 不会放入cache
                            .defer('field')    # 排除某列数据
                            .only('field')     # 仅取某列数据
                            .using('defualt1') # 连接不同的数据库
                当需要对整个field操作时 
                    from django.db.models import F
                    manager.update(num=F('num')+1)  # 包装field, 使其可以被调用
                
                
             
             3. 删除记录
                manager.查.delete()      # 要注意get方法查到的是单条记录, 但都有delete方法
                
             4. 更新记录
                方式一: 通过QuerySet.update()
                      manager.filter().update(field=value)  # 要注意get查到的是单条记录, 没有update方法
                方式二: 通过model重写
                      obj = manager.filter()[0]
                      obj.field = new_value
                      obj.save()                            # 会将全部数据重新写入, 不推荐   
                      
             * 自定义SQL语句
                1. 完全自定义
                   from django.db import connection, connections
                   cursor = connection.cursor()   # cursor = connections('default1').cursor()
                2. 对当前manager自定义
                   manager.raw('sql',param=None,translations=None,using=None)
                       'sql'               # SQL语句
                       param               # 为该SQL语句传入的参数,避免写死,如raw('select id as nid from userinfo where nid>%s', params=[12,])
                       translations        # 列名转换, 如 name_map = {'first': 'first_name', 'last': 'last_name'}
                                                        raw('SELECT * FROM some_other_table', translations=name_map) 
                       using='default'     # 使用哪个数据库 
                3. 利用extra函数对当前manager自定义
                   extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None) 
                   如 extra(select={'new_id': "select id from tb where id > %s"}, select_params=(1,), order_by=['-nid'])                                      
'''  # ORM, 单表操作

'''
ORM多表操作:
          连表: manager.select_related('fk1',..)    # 一次连表获得所有数据
               manager.prefetch_related('fk1',..)  # 子查询, 两次查询一次缓存
          1. 一对多
                1>. 添加记录
                    方式一: 直接指定外键id
                           book_info={
                                'title':'php',
                                'price':100.00,
                                'publish_date':'2017-7-9',
                                'publisher_id':3                  # 此时外键为'publish_id'
                            }
                           Book.objects.create(**book_info)
                    
                    方式二: 先获取要绑定的主表记录对象，再绑定
                          pub_obj = Publisher.objects.get(id=1)
                          book_info = {
                                'title':'php',
                                'price':100.00,
                                'publish_date':'2017-7-9',
                                'publisher':pub_obj               # 此时外键为'publiser', 按建表时的来，因为相当于是先指定对象，django再转为外键号
                          }
                          
                2>. 查找记录:
                    方式一: 通过对象(正向)或QuerySet(反向)查找
                           正向查找(子表->主表):  child_obj.foreignkey     # 获得主表对应的对象，通过其属性访问主表信息，相当于子表左连接主表
                           反向查找(主表->子表):  pub_obj.child_set        # 获得子表对应的manager, 可通过后续的查找方法filter,get,all获得子表信息
                                                                         #  这里child是子表的表名  
                                                
                    方式二: 双下划线连接表
                           正向查找(子表->主表):  Book.objects.filter(publisher__name=value)         # 通过 外键 双下划线连接主表有关的查询条件
                                                Book.objects.filter().values('publisher__name')    # 通过 外键 双下划线查询主表的信息
                           反向查询(主表->子表):  Publisher.objects.filter(book___name=value)       # 通过 子表表名 双下划线连接子表有关的查询条件
                                                Publisher.objects.filter().values(book_title)     # 通过 子表表明 双下划线查询子表的信息
                
                3>. 删除记录:
                    删除子表记录:
                           manager.查.delete()       # 同单表操作
                    删除主表记录:
                           manager.查.delete()       # 按on_delete操作子表信息                
                
                4>. 更新记录:
                    manager.查.update()              # 更新子表, 主表同单表操作
          
          2. 多对多:
                1>. 增加记录:
                     通过方式一创建关系: 只能通过其对象的外键属性add方法添加，一次可以添加多个关系
                          book_obj.authors.add(author1,author2)
                          book_obj.authors.add(*QuerySet)
                     
                     通过方式二创建关系: 手动对关系表添加,一次只能添加一个关系
                          book_author_info = {
                                'author': author_obj,
                                'book': book_obj
                          }
                          Book_Author.objects.create(**book_author_info)
                          或者
                          book_author_info = {
                               'author_id': author_id
                               'book_id':book_id
                          }
                     ** 反向操作: 通过author_obj.book_set   # 获得子表的manager, 然后进一步操作
                                
                4>. 查找记录: 同一对多双下划线查找
                
                5>. 删除记录:
                      正向删除:  book_obj.author.clear()     # 清除全部
                                book_obj.author.remove()    # 清除指定author_id
                      反向删除:  author_obj.book_set.clear()
                                                  .remove()
                                                  
                6>. 修改记录:  .set([])   # 指定book_id                                                             
'''  # ORM, 多表操作

'''
Cookie: 是服务器返回给客户端Cookie，是一组键值对，其键和值都是字符串
        同一个客户端再次访问服务器时，会携带该Cookie
        
        应用: 1. 服务器可以通过Cookie验证客户端
             2. 页面跳转时传递信息
             
        局限: 1. Cookie保存在客户端
             2. Cookie只能存4096字节
             
        使用: 1. 设置Cookie: 
                    response = redirect('/url') 或者  HTTPResponse()
                    response.set_cookie('key','value',max_age=, expire=)  # 1>. key, value都是str
                                                                            2>. 一次只能设置一组键值对
                                                                            3>. max_age为有效的秒数
                                                                            4>. expire为到期的datetime时间
             2. 客户端再次访问，服务器获取其携带的Cookie:
                    request.Cookie      # 一组组键值对
             
             3. 删除Cookie:
                   response.delete_cookie('key')      # 相当于是在服务端删除后，在传给客户端覆盖
             3. jquery可以通过.cookie()操作Cookie                                                                       

Session: 仅在返回给客户端的Cookie上存储sessionid（字符串），所有信息以键值对的形式存入服务器数据库，在django中是 django_session表
         使用:  1. 设置session:     request.session[key] = value         # value可以是任意数据类型
               
               2. 获取session:     request.session[key]                 # request.session是一个对象封装的键值对
               
               3. 删除session:     del request.session[key]             # 删除一个键值对
                                   request.session.flush()             # 删除该session
                                   
               4. 设置有效时间:     request.session.set_expiry(value)    # value可为整数或者datetime
               
               * 设置session的流程: 1>. 生成随机字符串
                                   2>. 将其写入Cookie中
                                   3>. 将其保存的服务器数据库中
                                   4>. 在服务器设置其相应字段
               * 客户端再次访问时，服务器通过其Cookie中唯一的sessionid 找到客户端对应的数据
'''  # Cookie & Session

'''
请求生命周期: 1.客户端发送HTTP请求
            *. 中间件
            2. 服务器的url管理系统根据其url匹配
            3. 匹配成功则执行ViewFunction:  1. FBV:  url --> 函数
                                          2. CBV:  url --> 类 --> 获取请求的方法post/get --> 执行相应的函数
                                             /****** views.py *******/
                                             from django.views import View
                                             class CBV(View):
                                                def dispatch(self,req,*args,**kwargs):
                                                    # other code
                                                    result = super(CBV,self).dispatch(req,*args,**kwargs)
                                                    return result
                                                def get(self,req): pass
                                                def post(self,req):pass
                                             
                                             /******* urls.py ******/
                                             url(r'^test$',view.CBV.as_view())
                                          
                                          * 执行过程: url --> CBV --> dispatch分配函数(反射) --> get --> dispatch 返回值
                                                                                          |__> post------^
            4. 业务处理: 1>. 操作数据库: 原始sql 
                                      orm
                        2>. 响应内容:  
                                     response = HTTPResponse('响应体')
                                     response['key'] = 'value'              # 响应头
                                     response.set_cookie('key','value')     # 响应体
                                     return response                        


搭建工作环境的流程:
                 1. 创建project
                 2. 创建app                           # python manage.py startapp app_name
                 3. 在settings.py中注册app             # app.apps.AppConfig
                 4. 配置静态变量环境
                 5. url分管
                 6. 视图函数分管
                 5. 连接mysql  
                 6. 配置mysql日志文件                         
'''  # 请求声明周期, 搭建环境的流程

'''
AJAX: (Asynchronous Javascript And XML)
       即使用Javascript语言与服务器进行异步交互，传输的数据为XML（现在更多使用json数据）
       
       同步交互：客户端发出一个请求后，需要等待服务器响应结束后，才能发出第二个请求
       异步交互：客户端发出一个请求后，无需等待服务器响应结束，就可以发出第二个请求
       
       利用AJAX可以做:
                    1.模态对话框: 1>. 注册验证用户是否存在
                                 2>. 登录验证用户名密码
                    2.不刷新页面的情况下，增加，删除，修改数据
       
       AJAX的实现:
           1. 基于jQuery的AJAX实现:
                $.ajax({
                   url: '/url',
                   type: 'GET/POST',       # POST先注释csrf_token
                   data: {
                        # 字典                               // 可传num, str
                   },
                   contentType:                              // 发送数据的编码格式
                   traditional:true,                         // 声明后data中可传list, 要传字典转json
                   timeout:                                  // 等待时间
                   async:                                    // 是否异步
                   
                   beforeSend: function(){}                   // 发送前执行的函数
                   complete: function(){}                    // 数据接收完全后执行的函数
                   success: function(arg){                   // 回调函数，服务器返回数据时执行，arg为返回的json字符串
                         JSON.stringify(dict)                        // 相当于字典转json, json.dumps(dict)
                         JSON.parse(str)                             // 相当于json转字典, json.loads(str)
                   },
                   error: function(){}                       // 失败时执行的函数
                   
                   dataType:                                // 将接收到的数据转为指定格式, json,jsonp,text,xml,html,script
                })
               
               $('button').click(function () {             
                    var data = $('#fm').serialize();                // 相当于submit, 获取form中所有的数据
                })
                
           2. 原生AJAX: var xhr = new XMLHttpRequest()
              GET:  xhr.open('GET','/url?p=123',[true/false]);    # 创建连接(是否异步)
                    xhr.onreadystatechange = function(){          # 指定状态改变时，执行的函数
                        if (xhr.readyState==4){                   # 回调函数，数据全部接收
                            var arg = xhr.responseText()          # 服务器返回的数据，字符串类型
                        }
                    };
                    xhr.send(null)                                 # 客户端发送数据    
              
              
              POST:  xhr.open('POST','/url');                 # 创建连接
                     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset-UTF-8'); # 设置请求头
                     xhr.onreadystatechange = function(){     # 回调函数
                        if(xhr.readyState==4){
                          var arg = xhr.responseText()
                        }
                     };
                     data_json = JSON.stringify(data)
                     xhr.send(data_json)                      # 发送数据

              其他属性和方法:
                   客户端状态值: xhr.readyState   0 -- 没有使用open()方法
                                                1 -- 使用了open(),但还没有send()
                                                2 -- 已经send()了,但还没有响应
                                                3 -- 部分接收
                                                4 -- 完全接收
                   接收:
                       响应头:  xhr.getResponseHeader('Content-Type')
                               xhr.getAllResponseHeader()
                       响应码:  xhr.states
                       响应文本: xhr.statesText  
                   发送:
                       设置响应头: xhr.setRequestHeader          
                   
           
           3. 伪AJAX: 兼容性最好
                 iframe标签 + form表单: form提供数据, iframe不刷新提供通道, 返回值在iframe中
                 <iframe  name='ifra' style='display:none'></iframe>
                 <form action='/url' method='post' target='ifra'>
                     <input type='text' name='user'/>
                     <input type='button' id='btn' value='提交'/>
                 </form>
                 
                 $('#btn').click(function(){
                     $('name').onload(function(this){                          # 回调函数, 通过iframe拿到返回值
                        var arg = this.contentWindow.document.body.innerText   # iframe内部也是一个html对象
                     })
                 })                                                          
''' # AJAX: 三种实现方式

'''
跨域访问: 如http://www.bilibili.com的脚本向http://www.acfun.com发送请求
浏览器的同源策略: 浏览器不接受跨域XMLHttpRequest的结果, 但发送请求和响应是可以进行的
AJAX跨域方法:
        1. JSOP的机制:  1>. 创建script标签, 利用其src属性实现跨域
                       2>. 其跨域的结果为<script>func(返回值)</script>, 会调用本地规定好的函数, 运行结果
                       3>. 结束后删除script标签
                   
                   使用:
                         $.ajax({
                            url: '/url'      // 跨域url
                            type:'GET',
                            dataType:'jsonp',           // 声明以下内容以script src=url的方式传递, 因此只能是GET
                            jsonp:'callback',           // 告诉对方以req.GET.get('callback')获取返回函数名
                            jsonCallback:'func',        // 以func函数包裹数组
                         })
                         function func(arg){            // 定义回调函数
                           console.log(arg);
                         }
        2. CORS(Cross-Origin Resource Sharing): 跨域资源共享，设置特殊的响应头，浏览器不阻止
''' # AJAX: 跨域

'''
分页器:  属于控制器, 需要前后端传入数据
     1. 设定每页显示多少数据                               per_counts
     2. 从后端获得数据总条目                               total_counts
     3. 根据1，2计算总页数                                total_page
     4. 从前端获取当前页码                                current_page
     5. 根据1，4计算当前页码的数据在数据库中的位置            start_item, end_item
     6. 数据库中取数据
     7. 传入模板中渲染

     其他功能:
     1. 首页/尾页      front_page/tail_page
     2. 前一页/后一页   prev_page/next_page
     3. 要显示多少页码  display_pages

自定义分页器:
    传入:    1>. total_counst
            2>. current_page
            3>. per_counts
            4>. display_pages
                      
    返回:      1>. total_pages
              2>. current_page
              3>. prev_page
              4>. next_page
              5>. fron_page
              6>. next_page
              7>. 当前页的start_item, end_item     
     特点: 1>. 在一个对象中处理所有信息
           2>. 直接将current_page的异常情况处理好     
          
django内置分页器:
     from django.core import paginator
     主要内置四个类:    Paginator： 管理总页数，总数据量，总页码的索引范围，负责找到指定页
                                :input    obj_list, per_counts        # django是惰性存储，且有缓存，因此可以直接把数据全部取出
                                :return   .count        数据总量
                                          .num_pages    总页码
                                          .page_range   总页数的索引范围
                                          .page(i)      第i页的对象,可迭代获取该页面的信息
                                
                      Page：指定页是否有下一页，获取下一页，是否有上一页，获取上一页，可迭代获取该页的信息，可指向总的页码管理器
                           ：input  先生成总的页码管理器，再找到指定的页码
                           :return  has_next()               是否有下一页
                                    next_page_number()       下一页页码
                                    has_previous()           是否有上一页
                                    previous_page_number()   上一页页码
                                    start_index()            开始的下标
                                    end_index()              结束的下标
                                    .paginator               指向页码管理器
                   获取页对象的错误类型                 
                      EmptyPage:   
                               page=paginator.page(12)   # error:EmptyPage, 页面小于1或者大于最大页码数抛出异常
                    
                      PageNotAnInteger     
                               #page=paginator.page("z")   # error:PageNotAnInteger， 页码为非整数或者为空时抛出异常
      特点: 1. 有两个页码处理对象，一个作为总的页码管理器，一个作为指定页的管理，可互相指向
           2. 定义了两个页码错误的类，需要自己定义异常情况下的处理                         
''' # 分页器

'''
Form组件: Form组件是来规定前端用户输入数据的类型，并供视图函数做验证
        作用: 1. 定制生成form表单的HTML标签，限定格式
                如text, password, checkbox, radio, file(上传文件)   |   select, textarea(文本域)
             2. 验证输入信息是否符合格式
             3. 验证后, 可以保留form表单上次提交的信息(form提交后会刷新)
             4. 初始化form表单的内容
             
        用法:
             1. 定制form表单类，相当于创建用于前端交互的model类，要注意格式与后端相同
                class MyForm(forms.From):
                   field_name = fields.Field(
                         attr = value
                   )            
                Field 是一个类，用来限制输入的数据类型
                      /******** 能直接匹配后端的 ************/
                          CharField(Field):               max_length, min_length, strip = True  
                          IntegerField(Field):            max_value, min_value
                          FloatField(IntegerField):       同上
                          DecimalField(IntegerField):     同上, max_digits(总长度), decimal_places(小数位长度)
                          
                          DateField(BaseTemporalField)     格式：2015-09-01
                          DateTimeField(BaseTemporalField) 格式：2015-09-01 11:12 
                          
                          URLField(Field)
                          EmailField(CharField)
                          BooleanField(Field)
                          
                      /********** 用于前端的 *****************/
                          RegexField(CharField):           regex(正则表达式), max_length,min_length
                          ChoiceField(Field):              choices = ((0,'上海'),(1,'北京'),)  # 选择框，也可以用插件定制
            
''' # Form组件: 字段

'''
Field字段参数的作用:
          1. 限制数据:   required=True   # 默认不能为空
                        initial         # 初始值
                        disabled        # 只读
          
          2. 用于显示:   label           # 输入框名称
                        help_text       # 帮助信息      
                        show_hidden_initial  # ?????????
                        
          3. html插件: widget = widgets.标签类型
               用于定制html的类型: 输入框(text,password, check, radio)
                                 选择框(select) 
               
               常用插件: 插件也是一个类，可通过attrs={'id':'i1','class':'c1'}定义标签属性
                        TextInput(Input)
                        PasswordInput(TextInput)
                        CheckboxInput      选中返回'on'
                        
                    选择框:  选项: choices = ((0,'上海'),(1,'北京'),) 可通过插件内部属性或ChoiceField设定
                            初始值: initial = 1(单选) 或 [1,](多选)   
                            RadioSelect           单选    
                            Select                单选
                            SelectMultiple        多选
                            CheckboxSelectMultiple   多选   
                    
                    对于选择框的数据库实时更新:
                        1>. 将更新操作写入__init__(self)函数，
                            因为field字段是静态属性，只会加载一次，不能实时更新；而__init__(self)函数会在每次创建对象时执行
                            def __init__(self,*arg,**kwargs):
                                super(MyForm,self).__init__(*args,**kwargs)
                                self.fields['field_name'].widget.choices = model.Table.all().value_list('id','name') 
                                
          4. 错误反馈:
                error_messages = {
                    'attr':'错误反馈',
                    'invalid': '格式错误',    # 正则校验错误
                }     
                
          5. 自定义验证: validators = [], 自定义匹配规则
             方式一: 使用django自带的正则匹配器
                    from django.core.validators import RegexValidator
                    ret = re.compile(r'正则表达式')
                    vat_01 = RegexValidator(ret,'错误反馈')
                    validators = [vat_01,..]
          
             方式二: 使用django的ValidationError返回错误信息
                    def vat_01(value):
                        ret = re.complie(r'正则表达式')
                        if not ret.march(value):
                            raise ValidationError('错误反馈')
                    validators = [vat_01,..]
             
             扩展: form.is_valid() -> self.errors -> self.full_clean()
                   Form组件验证过程: 1. 生成一个空的错误字典self._errors = ErrorDict(); 一个干净数据字典 self.cleaned_data = {}
                                   2. self._clean_fields()
                                   3. self._clean_form()
                                   4. self._post_clean()
             
             扩展一: self._clean_fields()
                    正则表达式验证 +  后端数据验证 (只能对当前字段进行验证)
                    Form组件的验证过程:  1. 逐一判断field正则表达式
                                       2. 成功 self.cleaned_data['field_name'] = value
                                       3. if hasattr(self,'clean_%' % field_name):
                                               value = getattr(self,'clean_%' % name)()
                                               self.cleaned_data[field_name] = value
                    class MyForm():
                         user = ...
                         def clean_user(self):
                             if models.User.objects.filter(name=user).count():     # 后端验证
                                raise ValidationError('用户名已存在')                # 有错则抛出异常
                             return self.cleaned_data['user']                      # 返回值固定
             
             扩展二: self._clean_form
                    在self._clean_fields()之后，进行联合验证
                    self._clean_form执行过程: 1. cleaned_data = self.clean()
                                             2. self.cleaned_data = cleaned_data
                    在 self.clean()中可进行联合验证
                       def clean(self):
                           value_dict = self.cleaned_data                         # 获取已校验的数据
                           v1 = value_dict.get('user')
                           v2 = value_dict.get('id')
                           if v1 == 'root' and v2 == 1:                           # 进行联合验证
                              raise.ValidationError('联合验证失败')                 # 有错则抛出异常
                           return self.cleaned_data                               # 返回值固定     
                    /***** 前端 ****/
                    form.errors = {
                           '__all__': '整体错误'
                           'users': users字段的错误
                    }
                    form.errors.__all__   
             
             扩展三: self._post_clean()全局扩展钩子                                                                                                                                     
'''# Form组件: 字段参数

'''
2. 视图处理渲染:
     1>. 生成html标签
            1. 生成 form对象, view.py
                 未初始化: form = MyForm()
                 初始化:   data = {}
                          form = MyForm(data)  # 注意字段匹配
            2. 传入模板渲染 .html
                 {{form.field_name.label}}   标签名
                 {{form.field_name}}         标签信息
                 {{form.field_name.errors}}  错误信息(列表)  {{obj.field_name.errors.0}} 取第一个错误
               或者             
                  {{form.as_p}}              整体渲染 
     
     2>. 验证格式
            1.验证
                form = MyForm(req.POST)          # 获取用户信息  
                   if form.is_valid():              # 校验
                       data = form.cleaned_data     # 成功获取信息，字典
                       Table.objects.create(**data) # 存入数据，注意form字段名称与model配对    
                   else:
                       errors = form.errors         # 获取错误信息
            2. 传入模板渲染
                {{ form.field_name.errors }}       
                
                
     3>. AJAX的信息验证:
            Form表单: 有错直接render重新渲染 错误信息
            AJAX: 页面不会主动跳转(redirect也不会跳转), 用JS渲染错误信息
                  1. 后端序列化错误信息
                     data = {'messages':form.errors}
                     return json.dumps(data)          # 本来json只能序列化基本数据类型，但errors是ErrorDict(dict)的对象，可序列化
                  2. 前端得到信息后，js操作动态显示
            注意: errors = form.errors 默认为 <ul>标签
                 可转化为:  errors.as_ul()
                           errors.as_json()
                           errors.as_data()                                                             
''' # Form组件: 视图函数处理

'''
Django序列化: 生成能够保存, 传输的数据(如字符串，二进制编码)，叫序列化
             web中后端向前端传输数据: 1. return render(req,'template.html')  # 后端处理，然后把数据整个传给前端渲染
                                   2. ajax + 序列化(json) + js 前端渲染
             能json序列化的数据类型: list, tuple, dict
             
             AJAX中的数据序列化:  
                   1. QuerySet, 后端直接向前端传输obj对象: 
                      两次序列化: 1. obj对象序列化, 存入字典
                                2. 字典序列化为json
                   /***** 后端 *****/ 
                      from django.core import serializers
                      users = UserInfo.objects.all()                        # QuerySet, 内部为对象
                      users_json = serializers.serialize('json',users)      # 只能序列化对象
                      message = {'data':users_json}
                      message_json = json.dumps(message)                    # 序列化字典
                      return HTTPResponse(message_json)
                   /**** 前端 ****/
                       $.ajax({
                         ...
                         dataType: 'JSON',                                      # 解字典序列化 
                         success:function(arg){
                             users = JSON.parse(arg.data)                       # 解对象序列化
                         }
                       }) 
                   
                   2. ValueQuerySet, 后端向前端传输处理好的数据
                      ValueQuerySet: 内部为字典  .values('username','id')           
                                     内部为元组  .values_list('username','id')
                      序列化:  1. ValueQuerySet转list
                              2. 序列化字典
                      /***** 后端 *****/
                      users = UserInfo.objects.all().values('id','username')    #  ValueQuerySet: 内部字典
                      message = {'data':list(users)}                            #  转list
                      return HTTPResponse(json.dumps(message))                  #  字典序列化                                                
''' # Django序列化

'''
文件上传:  1. form表单上传:  <form enctype='mulitpart/form-data'>
             1>. 直接通过file输入框上传
                 前端: <input type='file' name='img'>
                 后端: img = req.FILES.get('img')     # 文件对象(文件名称，文件大小，文件内容)
                      file_name = img.name
                      file_size = img.size
                      for line in img.chunks():      # img.chunks()为文件内容迭代器 
                           # 保存
             
             1+>.制作上传按钮:
                 <div style='position:relative'>
                     <input type='button' value='上传'>
                     <input type='file' name='img' style='opacity:0; position:absolute; top:0;left:0'>
                 </div>
                                  
             2>. Form组件上传
                 /* myFom.py */
                 img = fields.FileField()
                 /* views.py */
                 form = myForm(req.Files)
                 if form.is_valid():
                    img = form.cleaned_data['img']
                    # 后面保存数据同1>      
          
          2. AJAX上传:
             1>. jQuery, 原生xhr: 用FormData对象来封装文件数据
                 前端: var fileobj = $('#img').files[0];
                      var formdata = new FormData();
                      formdata.append('file',fileobj);           # 文件对象封装到formdata
                      $.ajax({
                       data: form,
                       processData:false,   // 告诉jQuery不要处理数据
                       contentType:false,   // 告诉jQuery不要设置文件格式
                      })
                 后端: fileobj = req.FILES.get('file')
                      同上     
             2. iframe + form: 同form表单上传
''' # 文件上传

'''
中间件: 1. 位于request和response之间的一道处理过程, 从全局上改变django的输入输出
       2. 中间件是一些类, 客户端request和服务器response经过中间件时, 会执行相应的类方法
       3. 中间件的类方法有:
                        process_request(request): pass
                        process_view(request,callback,callback_args,callback_kwargs):pass
                        process_exception(request,exception):
                        process_response(request,response): return response
       **中间件的执行流程:
              1>. 整体从上到下依次执行
              2>. url请求-->中间件1的process_request -->中间件2的process_request --> url路由控制 --> 中间1的process_view <-- 中间2的process_view
                    ^                                                                                                            |
                    |<-- 中间件1的process_response<-- 中间2的process_response <---------------------------------------- 视图函数 <--|
                                                                                  ^                                              |
                                                                                  |                                 视图函数出错   | 
                                                                         中间1的process_exception <-- 中间2的process_exception <-- | 

              3>. 对于一个中间件而言, 在process_request时中断返回HTTPResponse, 将直接跳过所有中间过程, 到其process_response 
                                   在process_view时中断, 将直接跳过所有中间过程, 但所有的process_response都会执行
                                   
              4>. process_view可以调用视图函数: callback(request,*callback_args,**callback_kwargs) 
              
       
       使用: 1. settings.py 中注册
               MIDDLEWARE = [
                    'MyMidddleware.Md1',
                    'MyMidddleware.Md2',
               ]   
            2. 继承MiddlewareMixin, 定义相应类方法 
               from django.utils.deprecation import MiddlewareMixin     
               class  Md1(MiddlewareMixin):
                   def process_request(self,request): pass       
''' # 中间件

'''
注册: from django.contrib.auth.models import User
     1. 获取用户名, 密码等注册信息
     2. 判断用户名是否存在: if User.objects.filter(username=username)
     3. 不存在则创建新用户: new_user = User.objects.create_user(username=username,password=password,**kwargs)
                         new_user.save()  

登录: from django.contrib.auth import authenticate, login
     1. 获取用户名和密码
     2. 认证: user = authenticate(username=username,password=password)
     3. 认证成功则登录:  if user is Not None: login(request,user)
     
需要登录验证的操作: from django.contrib.auth,decorators import login_required
                 @login_required
                 def my_view(req): pass
     执行过程为:
              1. url --> my_view
              2. 判断是否登录: if not request.user.is_authenticated()    
              3. 没有登录则重定向到settings.LOGIN_URL登录页面
              4. 登录成功后重定向到req.path当前路径

修改密码:
        1. 获取旧密码
        2. 验证是否正确: if req.user.check_password(old_password):
        3. 正确则修改: user = User.objects.filter(username=username).first()
                      user.set_password(password=new_password)
                      user.save()
                      
注销: from django.contrib.auth import logout
      def logout_view(req):
         logout(req)
         # 成功页面                                                     
''' # Auth组件: 注册, 登录, 修改密码, 注销
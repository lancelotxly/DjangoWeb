from django.shortcuts import render, HttpResponse, redirect
from blog.models import *
from django.db.models import Q,F
from django.views import View

# Create your views here.
'''
Cookie & Session
'''
user_info = {
            'xzq':'123',
            'John':'456',
            'Cindy':'789'
        }
def login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        if username in user_info:
            password = req.POST.get('password')
            if password == user_info[username]:
                # Session
                # req.session['is_login']=True
                # req.session['username']=username
                # return redirect('/welcome/')

                # Cookie
                response = redirect('/welcome/')
                response.set_cookie('is_login','true')
                response.set_cookie('username',username)
                return response

    return render(req,'login.html')

def welcome(req):
    # Session
    # if req.session.get('is_login',False) == True:
    #     cookie_content = req.COOKIES
    #     session_content = req.session
    #     username = req.session.get('username',None)
    #     return render(req,'welcome.html',locals())

    # Cookie
    if req.COOKIES.get('is_login',None) == 'true':
        cookie_content = req.COOKIES
        session_content = req.session
        username = req.COOKIES.get('username',None)
        return render(req,'welcome.html',locals())

    return redirect('/login/')

def logout(req):
    # Session
    # try:
    #     del req.session['is_login']
    # except KeyError:
    #     pass
    # return redirect('/login/')

    # Cookie
    try:
        response = redirect('/login/')
        response.delete_cookie('is_login')
    except KeyError:
        pass
    return response


'''
CBV:
'''
class Test(View):
    def dispatch(self, request, *args, **kwargs):
        result = super(Test,self).dispatch(request,*args,**kwargs)
        return result

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    def get(self,req):
        return render(req,'test.html')

    def post(self,req):
        return HttpResponse('Test.post')

'''
前端获取form表单信息
'''
def formtest(req):
    return render(req,'formtest.html')

'''
分页器  
'''
USER_LIST = []
for i in range(1,101):
    item = {'name':'root'+str(i),'age':i}
    USER_LIST.append(item)

# 自定定义分页器组件
from blog.page_manager import PageManager
def pages(req):
    per_counts = 9
    total_counts = len(USER_LIST)
    current_info  = req.GET.get('p',None)
    display_pages = 5
    p = PageManager(total_counts,current_info,per_counts,display_pages)
    total_pages = p.total_pages
    current_page = p.current_page
    prev_page = p.prev_page
    next_page = p.next_page
    front_page = p.front_page
    tail_page = p.tail_page
    pages_list = p.pages_list()
    start_item, end_item = p.index()
    context = {'user_list': USER_LIST[start_item:end_item + 1],
               'prev_page': prev_page,
               'next_page': next_page,
               'pages_list': pages_list,
               'current_page': current_page,
               'front_page': front_page,
               'tail_page': tail_page
               }
    return render(req, 'pages.html', context)

# django分页器组件
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def django_pages(req):
    current_page = req.GET.get('p')
    paginator = Paginator(USER_LIST,10)    # 总的数据, 每页要显示多少项
    try:
        posts = paginator.page(current_page)  # 获取当前页
        print(posts.start_index(),posts.end_index())
    except PageNotAnInteger:
        posts = paginator.page(1)             # 如果当前页p='z'不是整数或为空p=None， 则获取第一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)      # 如果当前页超过总页数，则获取最后一页
    return render(req,'django_pages.html',{'posts':posts})

# django分页器扩展
from blog.django_page_plus import CustomPaginator
def django_pages_plus(req):
    # current_page = req.GET.get('p')
    # # paginator = CustomPaginator(current_page,4,USER_LIST,10)
    # # try:
    # #     posts = paginator.page(current_page)
    # #     print(posts.start_index(), posts.end_index())
    # # except PageNotAnInteger:
    # #     posts = paginator.page(1)
    # # except EmptyPage:
    # #     posts = paginator.page(paginator.num_pages)
    # # return render(req, 'django_pages.html', {'posts': posts})
    # print(current_page)
    return HttpResponse('ok')

'''
Form组件
'''
from blog.MyForm import MyForm
def form_part(req):
    if req.method == 'GET':
        form = MyForm()
        return render(req,'form_part.html',{'form':form})
    elif req.method == 'POST':
        form = MyForm(req.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.cleaned_data)
            print(form.errors)
    return HttpResponse('ok')


'''
中间件
'''
def middleware(req):
    print('View函数')
    return HttpResponse('ok')


'''
Auth组件
'''
from django.contrib.auth.models import User
def sign_up(req):
    state = None
    if req.method == 'POST':
        password = req.POST.get('password',None)
        username = req.POST.get('username')
        print(password,username)
        if User.objects.filter(username=username):
            state = 'user_exist'
        else:
            new_user = User.objects.create_user(username=username,password=password)
            new_user.save()
            print(new_user.is_active)
            return HttpResponse('注册成功')
        return HttpResponse('注册失败, %s' % state)
    return render(req,'sign_up.html')
    


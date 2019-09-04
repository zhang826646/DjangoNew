from django.shortcuts import render,HttpResponseRedirect

from LoginUser.models import *
import hashlib

def password_md(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def register(request):  #登录页面
    error_message=''     #错误信息
    if request.method=='POST':   #判断是否为post请求
        email=request.POST.get('email')    #获取页面的email
        password=request.POST.get('password')   #获取页面的password
        if email:
            user=LoginUser.objects.filter(email=email).first()   #找到用户
            if not user:
                new_user=LoginUser()     #数据库存储数据
                new_user.email=email
                new_user.username=email
                new_user.password=password_md(password)
                new_user.save()
            else:
                error_message='邮箱已被注册，请登录'
        else:
            error_message='请填写邮箱'
    return render(request,'register.html',locals())



def login(request):
    error_message=''
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email:
            user=LoginUser.objects.filter(email=email).first()
            if user:
                db_password=user.password
                password=password_md(password)
                if password==db_password:
                    response=HttpResponseRedirect('/index/')
                    response.set_cookie('username',user.username)
                    response.set_cookie('user_id',user.id)
                    request.session['username']=user.username
                    return response
                else:
                    error_message='密码输入不正确'
            else:
                error_message='用户不存在'
        else:
            error_message='邮箱不可以为空'

    return render(request,'login.html',locals())


def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_username=request.COOKIES.get('username')
        session_username=request.session.get('username')
        if cookie_username and session_username and cookie_username==session_username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner
@loginValid
def index(request):
    return render(request,'index.html',locals())


def logout(request):
    response = HttpResponseRedirect("/login/")
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session["username"]
    return response
# Create your views here.

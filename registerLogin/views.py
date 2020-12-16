from django.shortcuts import render, redirect
from django.http import JsonResponse
from registerLogin.utils.selfFunc import db_login, db_register


# 登录页面逻辑
def login(request):
    if request.session.get('is_login', None):  # 如果已经登陆过
        identity = request.session.get('identity')
        return redirect('{}/index/'.format(identity))
    if request.method == 'POST':  # 如果准备登陆
        # 前端拿来的数据
        identity = request.POST.get('identity')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        response = {'identity': identity}  # 记录返回的数据
        # 从数据库中拿到用户id和密码
        name = db_login(identity, user_name, password)  # 返回登录的昵称
        if name is not None:
            if name[1] is True:  # 如果成功登录
                # 在session中保存信息
                request.session['is_login'] = True
                request.session['identity'] = identity
                request.session['user_name'] = user_name
                if identity == "consumer":
                    request.session['nickname'] = name[0]
                else:
                    request.session['name'] = name[0]
                response['success'] = 'true'
                # return redirect('/index/')  # 重定向给index
            else:  # 如果登录不成功，说明密码错误
                response['success'] = 'false'
                response['user_name_exists'] = 'true'
        else:  # 如果昵称为空，说明不存在该用户名
            response['success'] = 'false'
            response['user_name_exists'] = 'false'

        return JsonResponse(response)  # 最后都返回json数据

    # 如果首次进来，需要第一次展示登录页面
    return render(request, "registerLogin/login.html")


# 注册页面逻辑
def register(request):
    if request.method == 'POST':  # 如果准备注册
        # 前端拿来的数据
        request_values = {}
        request_values['identity'] = request.POST.get('identity')
        request_values['user_name'] = request.POST.get('user_name')
        request_values['password'] = request.POST.get('password')
        request_values['phone_number'] = request.POST.get('phone_number')
        request_values['user_icon'] = request.POST.get('user_icon')

        # 如果是消费者
        if request_values['identity'] == "consumer":
            request_values['nickname'] = request.POST.get('nickname')
        else:
            request_values['name'] = request.POST.get("name")
            request_values['id_number'] = request.POST.get("id_number")
        # 从数据库中拿到结果，字典保存
        response = db_register(request_values)
        return JsonResponse(response)
    else:
        return render(request, "registerLogin/register.html")


# 退出函数
def logout(request):
    if not request.session.get('is_login', None):
        # 如果没有登录
        return redirect('/register/')
    # 如果登录过
    request.session.flush()  # 把session清空
    return redirect('/login/')

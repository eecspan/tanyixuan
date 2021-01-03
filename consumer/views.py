from django.shortcuts import render, redirect


def index(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)
    if identity != "consumer":
        target_index = '/{identity}/index/'.format(identity=identity)
        return redirect(target_index)
    # 如果登录，跳转到index页面
    return render(request, 'consumer/index.html')

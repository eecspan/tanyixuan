from django.shortcuts import render, redirect
from manager.utils.selfFunc import *
from django.http import JsonResponse
import os


def index(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "manager":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)
    # 如果登录，跳转到index页面
    return render(request, 'manager/index.html', {'name': request.session['name']})


# 摊铺名称查重：
def check_market_repeat(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "manager":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        user_name = request.session.get('user_name', None)
        market_name = request.POST.get("market-name")  # 摊铺名称
        result = db_check_market_repeat(user_name, market_name)
        return JsonResponse(result)
    else:
        return redirect("/manager/index/")


def create_market(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "manager":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        user_name = request.session.get('user_name', None)
        market_name = request.POST.get("market-name")  # 摊铺名称
        market_categorys = request.POST.getlist("market-category")
        market_category = ""  # 摊铺经营类别
        for i in range(len(market_categorys)):
            if i == 0:
                market_category += market_categorys[i]
            else:
                market_category += ('、' + market_categorys[i])
        market_introduction = request.POST.get("market-introduction")  # 经营简介
        market_address = request.POST.get("market-address")
        market_phone_number = request.POST.get("market-phone-number")
        market_capacity = request.POST.get("market-capacity")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")

        # 将这些信息存入数据库
        result = db_create_market(user_name, market_name, market_category, market_introduction, market_address,
                                  market_capacity, market_phone_number, longitude, latitude)
        # 如果摊铺创建成功
        if result['success'] == 'true':
            market_pics = request.FILES.getlist("market-pics", None)

            # 图片的路径
            pic_urls = []
            for pic_file in market_pics:
                pic_urls.append('/images/market/' + market_name + str(market_pics.index(pic_file)) + '.jpg')

            # 将摊铺的图片都存储到根目录/static/images/market
            if market_pics is not None:
                for pic_file in market_pics:
                    with open('static' + pic_urls[market_pics.index(pic_file)], 'wb') as market_pic_file:
                        for chunk in pic_file.chunks():
                            market_pic_file.write(chunk)

            # 将图片路径存到数据表pic_urls中
            db_create_pic_url(result['market_id'], 'market', pic_urls)
        return redirect('/manager/index/')

    # 如果不是post请求
    return render(request, "manager/create-market.html")


# 展示我的市场（摆摊地点）页面
def my_market(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "manager":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果登录，跳转到my_market页面
    user_name = request.session.get('user_name', None)  # 用户名
    market_list = db_get_my_market(user_name)
    return render(request, 'manager/my-market.html', {"market_list": market_list})


# 删除市场
def delete_market(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "manager":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        market_name = request.POST.get("market_name")
        user_name = request.session.get("user_name", None)
        # 返回删除的booth的id，为了方便删除pic_url
        result = db_delete_market(market_name, user_name)
        if result["success"] == "true":
            # 删除pic_urls中的图片链接 并返回这些链接，为了在静态文件夹中把他们删除
            pic_urls = db_delete_pic_url(result["market_id"], "market")
            # 在静态文件夹中删除
            for pic_url in pic_urls:
                os.remove('static' + pic_url[0])
        # 返回结果
        return JsonResponse(result)

    # 否则返回主页
    else:
        return redirect("/manager/index/")


# 伪数据
def booth_detail(request, booth_id):
    return render(request, 'manager/booth-detail.html')

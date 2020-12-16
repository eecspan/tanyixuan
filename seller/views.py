from django.shortcuts import render, redirect
from django.http import JsonResponse
from seller.utils.selfFunc import *
import os


def index(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)
    # 如果登录，跳转到index页面
    return render(request, 'seller/index.html', {'name': request.session['name']})


def get_market(request):
    pageNo = request.POST.get("pageNo")
    pageSize = request.POST.get("pageSize")
    sortItem = request.POST.get("sortItem")
    category = request.POST.get("category")
    searchItem = request.POST.get("searchItem")
    market_list = db_get_market(pageNo, pageSize, sortItem, category, searchItem)
    response = {}  # 用于返回结果
    if len(market_list) == 0:
        response["success"] = "false"
    else:
        response["success"] = "true"
        response["marketList"] = market_list
    return JsonResponse(response, safe=False)


def market_detail(request, market_id):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 进入到摆摊地点详情页面，就会将session中的market_id更改
    request.session["market_id"] = market_id
    detail = db_get_market_detail(market_id)
    return render(request, "seller/market-detail.html", {"market_detail": detail})


# 展示我的摊位页面
def my_booth(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果登录，跳转到my_booth页面
    request.session["market_id"] = 0  # 要摆摊的地点设置为0，这里只是单纯展示我的摊位
    user_name = request.session.get('user_name', None)  # 用户名
    my_booth_list = db_get_my_booth(user_name)
    return render(request, 'seller/my-booth.html', {"market_id": 0, "my_booth_list": my_booth_list})


# 点击我要摆摊 跳转到开始摆摊页面
def start_business(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果登录，跳转到my_booth页面
    market_id = request.session.get('market_id', None)  # 要选择营业的摆摊地点id
    user_name = request.session.get('user_name', None)  # 用户名
    my_booth_list = db_get_my_booth(user_name)
    return render(request, 'seller/my-booth.html', {"market_id": market_id, "my_booth_list": my_booth_list})


# 返回json格式的我的摊位
def get_my_booth(request):
    return JsonResponse(None)


# 停止营业
def close_booth(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        market_id = request.POST.get("market_id")
        booth_name = request.POST.get("booth_name")
        user_name = request.session.get("user_name", None)
        result = db_close_booth(market_id, booth_name, user_name)
        # 返回结果
        return JsonResponse(result)
    # 否则返回主页
    else:
        redirect("/seller/index/")


# 开始营业
def open_booth(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        market_id = request.POST.get("market_id")
        booth_name = request.POST.get("booth_name")
        user_name = request.session.get("user_name", None)
        result = db_open_booth(market_id, booth_name, user_name)
        # 返回结果
        return JsonResponse(result)
    # 否则返回主页
    else:
        return redirect("/seller/index/")


# 删除摊铺
def delete_booth(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        booth_name = request.POST.get("booth_name")
        user_name = request.session.get("user_name", None)
        # 返回删除的booth的id，为了方便删除pic_url
        result = db_delete_booth(booth_name, user_name)
        if result["success"] == "true":
            # 删除pic_urls中的图片链接 并返回这些链接，为了在静态文件夹中把他们删除
            pic_urls = db_delete_pic_url(result["booth_id"], "booth")
            # 在静态文件夹中删除
            for pic_url in pic_urls:
                os.remove('static' + pic_url[0])
        # 返回结果
        return JsonResponse(result)

    # 否则返回主页
    else:
        return redirect("/seller/index/")


# 摊铺名称查重：
def check_booth_repeat(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        user_name = request.session.get('user_name', None)
        booth_name = request.POST.get("booth-name")  # 摊铺名称
        result = db_check_booth_repeat(user_name, booth_name)
        return JsonResponse(result)
    else:
        return redirect("/seller/index/")


# 创建摊铺
def create_booth(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，跳转到登录页面
        return redirect('/login/')
    identity = request.session.get('identity', None)  # 身份
    if identity != "seller":
        target_index = "/{identity}/index/".format(identity=identity)
        return redirect(target_index)

    # 如果是post请求
    if request.method == "POST":
        user_name = request.session.get('user_name', None)
        booth_name = request.POST.get("booth-name")  # 摊铺名称
        booth_categorys = request.POST.getlist("booth-category")
        booth_category = ""  # 摊铺经营类别
        for i in range(len(booth_categorys)):
            if i == 0:
                booth_category += booth_categorys[i]
            else:
                booth_category += ('、' + booth_categorys[i])
        booth_introduction = request.POST.get("booth-introduction")  # 经营简介
        # 将这些信息存入数据库
        result = db_create_booth(user_name, booth_name, booth_category, booth_introduction)
        # 如果摊铺创建成功
        if result['success'] == 'true':
            booth_pics = request.FILES.getlist("booth-pics", None)

            # 图片的路径
            pic_urls = []
            for pic_file in booth_pics:
                pic_urls.append('/images/booth/' + booth_name + str(booth_pics.index(pic_file)) + '.jpg')

            # 将摊铺的图片都存储到根目录/static/images/booth
            if booth_pics is not None:
                for pic_file in booth_pics:
                    with open('static' + pic_urls[booth_pics.index(pic_file)], 'wb') as booth_pic_file:
                        for chunk in pic_file.chunks():
                            booth_pic_file.write(chunk)

            # 将图片路径存到数据表pic_urls中
            db_create_pic_url(result['booth_id'], 'booth', pic_urls)
        return redirect('/seller/my-booth/')

    # 如果不是post请求
    return render(request, "seller/create-booth.html")

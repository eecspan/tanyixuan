from django.shortcuts import render, redirect
from manager.utils.selfFunc import *
from django.http import JsonResponse


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

        # 将这些信息存入数据库
        result = db_create_market(user_name, market_name, market_category, market_introduction, market_address,
                                  market_capacity, market_phone_number)
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

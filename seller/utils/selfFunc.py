import MySQLdb
from utils.selfFunc import dictfetchall


def db_get_market(pageNo, pageSize, sortItem, category, sortBasis, searchItem):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    pageBegin = (int(pageNo)-1)*int(pageSize)  # 起始项  为了分页
    category_radio = '%' + category + '%'  # 为了得到特定类别的摆摊地点
    search_item = '%' + searchItem + '%'  # 为了得到名称中符合条件的摆摊地点

    # 按照评分
    if sortItem == "mark":
        sql = "select id, name, address, introduction, current_capacity, capacity, category, phone_number, mark, " \
          "(select url from pic_urls where category = \"market\" and id = market.id limit 0, 1) pic_url from market " \
          "where current_capacity > 0 and category like \"{radio}\" and " \
          "(name like \"{search_item}\" or address like \"{search_item}\") order by mark {sortBasis} limit {pageBegin}, {pageSize};"\
           .format(search_item=search_item, radio=category_radio, pageBegin=pageBegin,
                   pageSize=pageSize, sortBasis=sortBasis)
    # 按照默认排序
    elif sortItem == "":
        sql = "select id, name, address, introduction, current_capacity, capacity, category, phone_number, mark, " \
          "(select url from pic_urls where category = \"market\" and id = market.id limit 0, 1) pic_url from market " \
          "where current_capacity > 0 and category like \"{radio}\" and " \
          "(name like \"{search_item}\" or address like \"{search_item}\") limit {pageBegin}, {pageSize};"\
           .format(search_item=search_item, radio=category_radio, pageBegin=pageBegin, pageSize=pageSize)
    # 按照地理位置
    else:
        sql = "select id, name, address, introduction, current_capacity, capacity, category, phone_number, mark, " \
              "(select url from pic_urls where category = \"market\" and id = market.id limit 0, 1) pic_url from market " \
              "where current_capacity > 0 and category like \"{radio}\" and " \
              "(name like \"{search_item}\" or address like \"{search_item}\") order by " \
              "power({latitude} - area_northwest_latitude, 2) + power({longtitude} - area_northwest_longitude, 2) {sortBasis} " \
              "limit {pageBegin}, {pageSize};" \
            .format(search_item=search_item, radio=category_radio, latitude=sortItem[0], longtitude=sortItem[1],
                    pageBegin=pageBegin, pageSize=pageSize, sortBasis=sortBasis)
    cursor.execute(sql)
    print(sql)
    market_list = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return market_list


def db_get_market_detail(market_id):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    sql = "select id, name, address, introduction, current_capacity, capacity, category, phone_number " \
          "from market where id={market_id};".format(market_id=market_id)
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchall()[0]
    market_detail = dict(zip(columns, row))

    # 接下来把所有图片返回
    market_detail["pic_urls"] = []
    sql = "select url from pic_urls where category=\"market\" and id = {market_id};".format(market_id=market_id)
    cursor.execute(sql)
    pic_urls = cursor.fetchall()
    for pic_url in pic_urls:
        market_detail["pic_urls"].append(pic_url[0])
    cursor.close()  # 关闭
    conn.close()
    return market_detail


def db_get_my_booth(user_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    # 先找正在营业的
    sql = "select " \
          "booth.id booth_id, " \
          "booth.name booth_name, " \
          "market.id market_id, " \
          "market.name market_name, " \
          "market.address market_address, " \
          "(select url from pic_urls where category=\"booth\" and id = booth_id limit 0, 1) pic_url " \
          "from " \
          "((booth join business on booth.id=business.booth_id) join market on market.id=business.market_id) "\
          "where " \
          "booth.seller_id = (select id from seller where user_name=\"{user_name}\") order by business.start_time"\
           .format(user_name=user_name)
    cursor.execute(sql)
    my_booth_list = {"open": dictfetchall(cursor)}

    # 再找未营业的
    sql = "select id booth_id, name booth_name, category, introduction, " \
    "(select url from pic_urls where category=\"booth\" and id=booth_id limit 0, 1) pic_url " \
    "from booth " \
    "where status=0 and seller_id=" \
    "(select id from seller where user_name=\"{user_name}\");".format(user_name=user_name)
    cursor.execute(sql)
    my_booth_list["close"] = dictfetchall(cursor)

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return my_booth_list


def db_close_booth(market_id, booth_name, user_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    sql = "delete from business " \
          "where market_id = {market_id} and booth_id = "\
          "(select id from booth where name=\"{booth_name}\" and seller_id = " \
          "(select id from seller where user_name=\"{user_name}\"));"\
         .format(market_id=market_id, booth_name=booth_name, user_name=user_name)
    try:
        cursor.execute(sql)
        # 还要修改booth中的status
        sql = "update booth set status = 0 " \
              "where name=\"{booth_name}\" and seller_id = " \
              "(select id from seller where user_name=\"{user_name}\");"\
            .format(booth_name=booth_name, user_name=user_name)
        try:
            cursor.execute(sql)
            # 将摆摊地点的可容纳摊位数量+1
            sql = "update market set current_capacity = current_capacity + 1 " \
                  "where id={market_id};".format(market_id=market_id)
            try:
                cursor.execute(sql)
                # 成功了就提交
                conn.commit()
                result = {"success": "true"}
            except:
                # 回退
                conn.rollback()
                result = {"success": "false"}
        except:
            # 回退
            conn.rollback()
            result = {"success": "false"}
    except:
        # 回退
        conn.rollback()
        result = {"success": "false"}
    # 关闭数据库连接
    cursor.close()
    conn.close()
    return result


def db_open_booth(market_id, booth_name, user_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    sql = "insert into business(booth_id, market_id, start_time) " \
    "values "\
    "((select id from booth where name=\"{booth_name}\" and seller_id = " \
    "(select id from seller where user_name=\"{user_name}\")), " \
    "{market_id}, now());".format(booth_name=booth_name, user_name=user_name, market_id=market_id)

    try:
        cursor.execute(sql)
        # 还要修改booth中的status
        sql = "update booth set status = 1 " \
              "where name=\"{booth_name}\" and seller_id = " \
              "(select id from seller where user_name=\"{user_name}\");" \
            .format(booth_name=booth_name, user_name=user_name)
        try:
            cursor.execute(sql)
            # 将摆摊地点的可容纳摊位数量-1
            sql = "update market set current_capacity = current_capacity - 1 " \
                  "where id={market_id};".format(market_id=market_id)
            try:
                cursor.execute(sql)
                # 成功了就提交
                conn.commit()
                result = {"success": "true"}
            except:
                # 回退
                conn.rollback()
                result = {"success": "false"}
        except:
            # 回退
            conn.rollback()
            result = {"success": "false"}
    except:
        # 回退
        conn.rollback()
        result = {"success": "false"}

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return result


def db_delete_booth(booth_name, user_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    sql = "select id from booth where name=\"{booth_name}\" and seller_id=" \
          "(select id from seller where user_name=\"{user_name}\");".format(booth_name=booth_name, user_name=user_name)
    try:
        cursor.execute(sql)
        booth_id = cursor.fetchone()  # 是一个元组形式
        if booth_id is None:
            result = {"success": "false"}
        else:
            booth_id = booth_id[0]
            result = {"booth_id": booth_id}
            sql = "delete from booth where id={booth_id};".format(booth_id=booth_id)
            try:
                cursor.execute(sql)
                # 提交
                conn.commit()
                result["success"] = "true"
            except:
                # 回退
                conn.rollback()
                result["success"] = "false"
    except:
        # 回退
        conn.rollback()
        result = {"success": "false"}

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return result


def db_check_booth_repeat(user_name, booth_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                              database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    # 先看看有没有重复的摊铺名称
    sql = "select id from booth where name=\"{booth_name}\" and seller_id=" \
          "(select id from seller where user_name=\"{user_name}\");".format(booth_name=booth_name, user_name=user_name)
    cursor.execute(sql)
    print(cursor.fetchone())
    if cursor.fetchone() is None:
        result = {"success": "true"}
    else:
        result = {"success": "false"}
    return result


def db_create_booth(user_name, booth_name, booth_category, booth_introduction):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    sql = "insert into booth" \
            "(seller_id, name, introduction, category, location_longitude, location_latitude, status)" \
            "values "\
            "((select id from seller where user_name=\"{user_name}\"), \"{booth_name}\", \"{booth_introduction}\", " \
            "\"{booth_category}\", 0, 0, 0);".format(user_name=user_name, booth_name=booth_name,
                                                booth_category=booth_category, booth_introduction=booth_introduction)
    try:
        cursor.execute(sql)
        # 成功了就提交
        conn.commit()
        result = {"success": "true"}
        # 还要查询booth_id
        sql = "select @@identity;"
        cursor.execute(sql)
        result['booth_id'] = cursor.fetchone()[0]
    except:
        # 回退
        conn.rollback()
        result = {"success": "false", "booth_name_repeat": "false"}

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return result


# id是身份的id，category是类别，字符串类型
def db_create_pic_url(id, category, pic_urls):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    for url in pic_urls:
        sql = "insert into pic_urls (id, category, url) values ({id}, \"{category}\", \"{url}\");" \
            .format(id=id, category=category, url=url)
        try:
            cursor.execute(sql)
            # 成功了就提交
            conn.commit()
        except:
            # 回退
            conn.rollback()
    # 关闭数据库连接
    cursor.close()
    conn.close()


def db_delete_pic_url(id, category):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    # 返回路径
    sql = "select url from pic_urls where category=\"{category}\" and id={id};".format(category=category, id=id)
    cursor.execute(sql)
    pic_urls = cursor.fetchall()

    # 删除他们
    sql = "delete from pic_urls where category=\"{category}\" and id={id};".format(category=category, id=id)
    try:
        cursor.execute(sql)
        # 成功了就提交
        conn.commit()
    except:
        # 回退
        conn.rollback()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 返回路径，元组类型，在静态文件夹中把他们删除
    return pic_urls

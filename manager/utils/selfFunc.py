import MySQLdb
from utils.selfFunc import dictfetchall


def db_check_market_repeat(user_name, market_name):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
    cursor = conn.cursor()

    # 先看看有没有重复的摊铺名称
    sql = "select id from market where name=\"{market_name}\" and manager_id=" \
          "(select id from manager where user_name=\"{user_name}\");".format(market_name=market_name,
                                                                     user_name=user_name)

    print(user_name)
    print(market_name)

    cursor.execute(sql)
    print(cursor.fetchone())
    if cursor.fetchone() is None:
        result = {"success": "true"}
    else:
        result = {"success": "false"}
    return result


def db_create_pic_url(id, category, pic_urls):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
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


def db_create_market(user_name, market_name, market_category, market_introduction, market_address, market_capacity,
                     market_phone_number, longitude, latitude):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
    cursor = conn.cursor()
    """
    sql = "insert into market" \
          "(seller_id, name, introduction, category, location_longitude, location_latitude, status)" \
          "values " \
          "((select id from seller where user_name=\"{user_name}\"), \"{market_name}\", \"{market_introduction}\", " \
          "\"{market_category}\", 0, 0, 0);".format(user_name=user_name, market_name=market_name,
                                                    market_category=market_category,
                                                    market_introduction=market_introduction)
    """
    sql = "insert into market" \
          "(name, address, introduction, area_northwest_longitude, area_northwest_latitude, east_dis, south_dis, " \
          "capacity, category, phone_number, current_capacity, manager_id, mark)" \
          "values " \
          "(\"{market_name}\", \"{address}\", \"{intro}\", \"{longitude}\", \"{latitude}\", \"{east_dis}\", " \
          "\"{south_dis}\",\"{cap}\", \"{categoty}\", \"{phone_number}\", \"{current_cap}\", "\
          "(select id from manager where user_name=\"{user_name}\"), " \
          "\"{mark}\");".format(market_name=market_name,
                                address=market_address,
                                intro=market_introduction,
                                longitude=longitude,
                                latitude=latitude,
                                east_dis=1,
                                south_dis=1,
                                cap=market_capacity,
                                categoty=market_category,
                                phone_number=market_phone_number,
                                current_cap=market_capacity,
                                user_name=user_name,
                                mark=0)
    print(sql)
    try:
        cursor.execute(sql)
        # 成功了就提交
        conn.commit()
        print("Debug: 测试是否成功插入数据")
        result = {"success": "true"}
        # 还要查询market_id
        sql = "select @@identity;"
        cursor.execute(sql)
        result['market_id'] = cursor.fetchone()[0]
    except:
        # 回退
        conn.rollback()
        result = {"success": "false", "market_name_repeat": "false"}

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return result


def db_get_my_market(user_name):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
    cursor = conn.cursor()

    # 再找未营业的
    sql = "select id market_id, name market_name, category, introduction, " \
          "(select url from pic_urls where category=\"market\" and id=market_id limit 0, 1) pic_url " \
          "from market " \
          "where manager_id=" \
          "(select id from manager where user_name=\"{user_name}\");".format(user_name=user_name)
    cursor.execute(sql)
    market_list = dictfetchall(cursor)

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return market_list


def db_delete_market(market_name, user_name):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
    cursor = conn.cursor()
    sql = "select id from market where name=\"{market_name}\" and manager_id=" \
          "(select id from manager where user_name=\"{user_name}\");".format(market_name=market_name, user_name=user_name)
    print(sql)
    try:
        cursor.execute(sql)
        market_id = cursor.fetchone()  # 是一个元组形式
        if market_id is None:
            result = {"success": "false"}
        else:
            market_id = market_id[0]
            result = {"market_id": market_id}
            sql = "delete from market where id={market_id};".format(market_id=market_id)
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


def db_delete_pic_url(id, category):
    conn = MySQLdb.connect(host='localhost', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=3306)
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

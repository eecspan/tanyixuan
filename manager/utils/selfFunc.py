import MySQLdb


def db_check_market_repeat(user_name, market_name):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()

    # 先看看有没有重复的摊铺名称
    sql = "select id from market where name=\"{market_name}\" and manager_id=" \
          "(select id from manager where user_name=\"{user_name}\");".format(market_name=market_name,
                                                                             user_name=user_name)
    cursor.execute(sql)
    print(cursor.fetchone())
    if cursor.fetchone() is None:
        result = {"success": "true"}
    else:
        result = {"success": "false"}
    return result


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


def db_create_market(user_name, market_name, market_category, market_introduction):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
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
          "name, address, introduction, area_northwest_longitude, area_northwest_latitude, east_dis, south_dis, " \
          "capacity, category, phone_number, current_capacity, manager_id, mark" \
          "values" \
          "(\"{market_name}\", \"{address}\", \"{intro}\", \"{longitude}\", \"{latitude}\", \"{east_dis}\", " \
          "\"{south_dis}\",\"{cap}\", \"{categoty}\", \"{phone_number}\" \"{current_cap}\"" \
          "(select id from manager where user_name=\"{user_name}\"), " \
          "\"{mark}\");".format(market_name=market_name,
                                address="XXX", intro=market_introduction, longitude=1, latitude=1, east_dis=1,
                                south_dis=1,cap=999, categoty=market_category, phone_number=110, current_cap=0,
                                user_name=user_name,
                                mark=5)
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

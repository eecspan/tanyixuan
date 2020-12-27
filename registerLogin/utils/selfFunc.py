import MySQLdb


def db_login(identity, user_name, password):
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    # 如果身份是消费者
    if identity == "consumer":
        sql = "select nickname from {table_name} where user_name = \'{user_name}\';".format(
            table_name=identity, user_name=user_name)
    # 如果身份是摊主或者管理者
    else:
        sql = "select name from {table_name} where user_name = \'{user_name}\';".format(
            table_name=identity, user_name=user_name)
    cursor.execute(sql)
    result = cursor.fetchone()  # 结果
    if result is not None:  # 如果存在这个user_name
        if identity == "consumer":
            sql = "select nickname from {table_name} where user_name = \'{user_name}\' and password = " \
                  "\'{password}\';".format(table_name=identity, user_name=user_name, password=password)
        else:
            sql = "select name from {table_name} where user_name = \'{user_name}\' and password = " \
                  "\'{password}\';".format(table_name=identity, user_name=user_name, password=password)
        cursor.execute(sql)
        login_name = cursor.fetchone()
        if login_name is not None:  # 如果密码正确，那么存在名字
            result += (True,)
        else:                       # 密码不正确，不存在名字
            result += (False,)

    cursor.close()  # 关闭
    conn.close()
    # 不存在该用户，返回空 都返回result
    return result

def db_register(request_values):
    response = {'identity': request_values['identity']}  # 用于返回数据
    conn = MySQLdb.connect(host='36t27o3263.wicp.vip', user='tanyixuanU', password='tanyixuan1904',
                           database='tanyixuan', charset='utf8', port=18486)
    cursor = conn.cursor()
    # 身份是消费者
    if request_values['identity'] == "consumer":
        sql = "select id from consumer where user_name = \"{user_name}\";".format(user_name=request_values['user_name'])
        cursor.execute(sql)
        user_id = cursor.fetchone()

        # 如果存在id，说明数据库中有了相同的用户名  注册失败
        if user_id is not None:
            response['success'] = "false"
            response['user_name_exists'] = "true"
        # 不存在id，说明可以注册
        else:
            sql = "INSERT INTO consumer (user_name, password, phone_number, nickname, user_icon) VALUES " \
                  "(\"{user_name}\", \"{password}\", \"{phone_number}\", \"{nickname}\", \"{user_icon}\");".format(
                user_name=request_values['user_name'], password=request_values['password'], phone_number=request_values['phone_number'],
                nickname=request_values['nickname'], user_icon=request_values['user_icon'])
            cursor.execute(sql)
            conn.commit()  # 插入的 不要忘记commit
            cursor.close()
            conn.close()
            response['success'] = "true"

    # 身份是卖家或者管理者
    else:
        # 查看是否有相同的用户名
        sql = "select id from {table_name} where user_name = \"{user_name}\";".format(
            table_name=request_values['identity'], user_name=request_values['user_name'])
        print(sql)
        cursor.execute(sql)
        user_id = cursor.fetchone()
        print(user_id)
        # 存在id，说明有重复的用户名
        if user_id is not None:
            response['success'] = "false"
            response['user_name_exists'] = "true"
        else:
            response['success'] = 'true'
            response['user_name_exists'] = "false"
        # 查看是否有相同的id_number
        sql = "select id from {table_name} where id_number = \"{id_number}\";".format(
            table_name=request_values['identity'], id_number=request_values['id_number'])
        cursor.execute(sql)
        user_id = cursor.fetchone()
        if user_id is not None:
            response['success'] = "false"
            response['id_number_exists'] = "true"
        else:
            response['id_number_exists'] = "false"

        if response['success'] == "true":  # 如果可以注册
            sql = "INSERT INTO {table_name} (user_name, password, name, id_number, phone_number, user_icon) VALUES " \
                  "(\"{user_name}\", \"{password}\", \"{name}\", \"{id_number}\", \"{phone_number}\", \"{user_icon}\");"\
                .format(table_name=request_values['identity'], user_name=request_values['user_name'],
                password=request_values['password'], name=request_values['name'], id_number=request_values['id_number'],
                phone_number=request_values['phone_number'], user_icon=request_values['user_icon'])
            cursor.execute(sql)
            conn.commit()  # 插入的 不要忘记commit
            cursor.close()
            conn.close()

    return response  # 最后都要返回结果

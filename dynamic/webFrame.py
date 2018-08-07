import re
from pymysql import *
from urllib.parse import unquote
import json

url_dict = {}


def application(env, get_status):
    url_str = env["PATH_INFO"]
    if url_str not in url_dict.keys():
        body = other()
    for path, function in url_dict.items():
        match = re.match(path, url_str)
        if match:
            body = function(match)
    get_status("200 OK", [('Content-Type', 'text/html;charset=utf-8')])
    return body


def get_dict(url_str):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        url_dict[url_str] = inner
        return inner
    return wrapper


@get_dict('/index.html')
def index(match):
    path = './templates/index.html'
    with open(path, 'r') as f:
        body = f.read()
    # row_str = """
    #              <tr>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>
    #                      <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
    #                  </td>
    #              </tr>  """
    # conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    # cur = conn.cursor()
    # sql_str = ''' select * from info; '''
    # cur.execute(sql_str)
    # all_file = cur.fetchall()
    # cur.close()
    # conn.close()
    # file = ''
    # for i in all_file:
    #     file += row_str % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[1])
    # body = re.sub(r'\{%content%\}', file, body)
    return body

# 股票数据
@get_dict('/index/info.html')
def index(match):
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select * from info; '''
    cur.execute(sql_str)
    all_file = cur.fetchall()
    cur.close()
    conn.close()
    body = []
    for i in all_file:
        dict = {}
        dict["a"] = i[0]
        dict["b"] = i[1]
        dict["c"] = i[2]
        dict["d"] = i[3]
        dict["e"] = i[4]
        dict["f"] = str(i[5])
        dict["g"] = str(i[6])
        dict["h"] = str(i[7])
        # print(dict)
        body.append(dict)
    # print(body)
    body = json.dumps(body)

    return body
# 股票数据


@get_dict('/center.html')
def index(match):
    path = './templates/center.html'
    with open(path, 'r') as f:
        body = f.read()
    # row_str = """
    #             <tr>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>
    #                      <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
    #                  </td>
    #                  <td>
    #                      <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
    #                  </td>
    #              </tr> """
    # conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    # cur = conn.cursor()
    # sql_str = ''' select info.code,info.short,info.chg,info.turnover,info.price,info.highs,focus.note_info from info inner join focus on info.id = focus.info_id; '''
    # cur.execute(sql_str)
    # all_file = cur.fetchall()
    # cur.close()
    # conn.close()
    # file = ''
    # for i in all_file:
    #     file += row_str % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[0], i[0])
    # body = re.sub(r'\{%content%\}', file, body)
    return body

# center数据
@get_dict('/center/info.html')
def index(match):
    # path = './templates/center.html'
    # with open(path, 'r') as f:
    #     body = f.read()
    # row_str = """
    #             <tr>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>%s</td>
    #                  <td>
    #                      <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
    #                  </td>
    #                  <td>
    #                      <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
    #                  </td>
    #              </tr> """
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select info.code,info.short,info.chg,info.turnover,info.price,info.highs,focus.note_info from info inner join focus on info.id = focus.info_id; '''
    cur.execute(sql_str)
    all_file = cur.fetchall()
    cur.close()
    conn.close()
    body = []
    for i in all_file:
        dict = {}
        dict["a"] = i[0]
        dict["b"] = i[1]
        dict["c"] = i[2]
        dict["d"] = i[3]
        dict["e"] = str(i[4])
        dict["f"] = str(i[5])
        dict["g"] = i[6]
        # print(dict)
        body.append(dict)
        # print(body)
    body = json.dumps(body)
    return body

# center数据


def other():
    path = './templates/error.html'
    with open(path, 'r') as f:
        body = f.read()
    return body

@get_dict(r'/add/(\d+)\.html')
def add(match):
    code = match.group(1)
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select * from focus where info_id in (select id from info where code = %s); '''
    cur.execute(sql_str, (code, ))
    sql_result = cur.fetchall()
    if sql_result:
        body = "该股票已收藏"
    else:
        sql_str = ''' insert into focus(info_id) (select id from info where code = %s); '''
        cur.execute(sql_str, (code, ))
        conn.commit()
        body = "添加收藏成功"

    cur.close()
    conn.close()

    return body

@get_dict(r'/del/(\d+)\.html')
def delete(match):
    code = match.group(1)
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' delete from focus where info_id in (select id from info where code = %s); '''
    cur.execute(sql_str, (code,))

    conn.commit()
    body = "删除成功"

    cur.close()
    conn.close()

    return body

@get_dict(r'/update/(\d+)\.html')
def update(match):
    code = match.group(1)
    path = './templates/update.html'
    with open(path, 'r') as f:
        body = f.read()
    #
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' select note_info from focus where info_id =(select id from info where info.code = %s); '''
    cur.execute(sql_str, (code, ))
    all_file = cur.fetchone()
    print(all_file)
    cur.close()
    conn.close()
    body = re.sub(r'\{%code%\}', code, body)
    body = re.sub(r'\{%note_info%\}', all_file[0], body)

    return body

@get_dict(r'/update/(\d+)/(.*)\.html')
def update_commit(match):
    code = match.group(1)
    info = match.group(2)
    info = unquote(info)
    conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='mysql', charset='utf8')
    cur = conn.cursor()
    sql_str = ''' update focus set note_info=%s where info_id = (select id from info where code=%s); '''
    cur.execute(sql_str, (info, code))
    conn.commit()
    cur.close()
    conn.close()
    body = "修改成功"
    return body

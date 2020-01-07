#coding=utf-8
import os,requests,json
from xlrd import open_workbook
from common.Log import MyLog as Log
from common.configHttp import ConfigHttp
from xml.etree import ElementTree
import readConfig
localConfigHttp = ConfigHttp()
localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
log = Log.get_log()
logger = log.get_logger()

caseNo = 0

#获取登录后的token
def get_visitor_token():
    host = localReadConfig.get_http('baseurl')
    response = requests.post(host+'passenger/login')
    info = response.json()
    token = info['data']['token']
    logger.debug("create token:%s"%(token))
    return token

#获取登录后的token
def set_visitor_token_to_config():
    token_Login = get_visitor_token()
    localReadConfig.set_headers("TOVEN_LOGIN",token_Login)

#获取返回值
def get_value_from_return_json(json,name1,name2):
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


#请求返回结果
def show_return_msg(response):
    url = response.url
    msg = response.text
    print("请求地址为:"+url)
    print("请求返回值为:"+json.loads(msg),verify=False,ensure_ascii=False, sort_keys=True, indent=4)

#从excel文件中读取测试用例
def get_xls(xls_name,sheet_name):
    cls = []
    #用例路径
    xlsPath = os.path.join(proDir,"testFile",xls_name)
    file = open_workbook(xlsPath)
    sheet = file.sheet_by_name(sheet_name)
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != 'ID':
            cls.append(sheet.row_values(i))
    return cls


database = {}
def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(proDir,'testFile',"")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name,table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict

def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    print('common类中的url_path为;'+url_path)
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/'.join(url_list)
    print('接口为:'+url)
    return url




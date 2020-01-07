#coding=utf-8
from common import common
from common import configHttp
import readConfig

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls('test_api.xlsx','login')

def login():
    url = common.get_url_from_xml("login")
    localConfigHttp.set_url(url)
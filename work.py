# -*- coding:utf8 -*-
import os
import time
import logging
import requests
from lxml import etree


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
username = ""  # 账户名(不是邮箱)
password = ""  # 密码


def getLogger(name):
    logger = logging.getLogger(name)
    filehandler = logging.FileHandler(
        BASE_DIR + os.sep + 'logging.log', 'a+', 'utf8'
    )
    streamhandler = logging.StreamHandler()
    record_format = logging.Formatter(
        "[%(levelname)s]-[%(filename)s]-[%(asctime)s]-[%(message)s]"
    )
    filehandler.setFormatter(record_format)
    streamhandler.setFormatter(record_format)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(logging.INFO)
    return logger


class DailyTask(object):
    """
        pythonanywhere web应用程序、计划任务自动延期
    """

    def __getattribute__(self, name):
        o = super().__getattribute__(name)
        if type(o).__name__ == 'method':
            time.sleep(1)
        return o

    def __init__(self):
        self.logger = getLogger(username)
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "Host": "www.pythonanywhere.com",
            "Origin": "https://www.pythonanywhere.com",
            "Referer": f"https://www.pythonanywhere.com/user/{username}/webapps/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        })
        self.enable = False
        if self.checkDate():
            self.enable = True

    def checkDate(self):
        '''
            检测日期
            每月1号和15号触发延期操作
            其他时间无操作
        '''
        day = int(time.strftime('%d', time.localtime(time.time() + 60 * 60 * 8)))
        if day == 1 or day == 15:
            return True
        return False

    def login(self):
        '''
            登录
        '''
        self.session.headers['Referer'] = 'https://www.pythonanywhere.com/login/?next=/login/'
        data = {
            "csrfmiddlewaretoken": self.csrfmiddlewaretoken('login'),
            "auth-username": username,
            "auth-password": password,
            "login_view-current_step": "auth"
        }
        url = 'https://www.pythonanywhere.com/login/?next=/login/'
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        self.logger.info(f'登录 状态码:{resp.status_code}')
        self.session.headers['Referer'] = f'https://www.pythonanywhere.com/user/{username}/webapps/'

    def csrfmiddlewaretoken(self, query):
        '''
            参数
        '''
        if query == 'login':
            url = 'https://www.pythonanywhere.com/login/?next=/login/'
            self.session.headers['Referer'] = 'https://www.pythonanywhere.com/login/?next=/login/'
        elif query == 'task':
            url = f'https://www.pythonanywhere.com/user/{username}/tasks_tab/'
        else:
            url = f'https://www.pythonanywhere.com/user/{username}/webapps/'
        resp = self.session.get(url=url)
        self.session.headers['Referer'] = f'https://www.pythonanywhere.com/user/{username}/webapps/'
        resp.encoding = 'utf-8'
        e = etree.HTML(resp.text)
        if query == 'extend':
            return e.xpath(f'string(//form[@action="/user/{username}/webapps/{username}.pythonanywhere.com/extend"]//input[1]/@value)')
        elif query == 'reload':
            return e.xpath(f'string(//form[@action="/user/{username}/webapps/{username}.pythonanywhere.com/reload"]//input[1]/@value)')
        elif query == 'login':
            return e.xpath('string(//form/input[1]/@value)')
        elif query == 'task':
            return e.xpath('string(//div[@class="container"]/ul[1]//form[@action="/logout/"]/input[1]/@value)')

    def reload(self):
        '''
            重新启动web应用
        '''
        url = f'https://www.pythonanywhere.com/user/{username}/webapps/{username}.pythonanywhere.com/reload'
        self.session.headers['X-CSRFToken'] = self.csrfmiddlewaretoken('reload')
        resp = self.session.post(url=url)
        resp.encoding = 'utf8'
        self.session.headers.pop('X-CSRFToken')
        record = f'重载 状态码:{resp.status_code}'
        self.logger.info(record)

    def extend(self):
        '''
            延长web应用停运时间
        '''
        url = f'https://www.pythonanywhere.com/user/{username}/webapps/{username}.pythonanywhere.com/extend'
        data = {
            'csrfmiddlewaretoken': self.csrfmiddlewaretoken('extend')
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        record = f'续命 状态码:{resp.status_code}'
        # self.logger.info(resp.text)
        self.logger.info(record)

    def schedule(self):
        '''
            获取计划任务Id
        '''
        url = f'https://www.pythonanywhere.com/api/v0/user/{username}/schedule/'
        self.session.headers['Refefer'] = f'https://www.pythonanywhere.com/user/{username}/tasks_tab/'
        resp = self.session.get(url=url)
        resp.encoding = 'utf8'
        data = resp.json()
        return data[0]['id']

    def taskextend(self):
        '''
            延长计划任务停运时间
        '''
        scheduleId = self.schedule()
        url = f'https://www.pythonanywhere.com/user/{username}/schedule/task/{scheduleId}/extend'
        data = {
            'csrfmiddlewaretoken': self.csrfmiddlewaretoken('task')
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        record = f'任务 状态码:{resp.status_code}'
        self.logger.info(record)

    def main(self):
        if not self.enable:
            return self.logger.info('不进行操作'), self.logger.info('-' * 48)
        self.login()
        self.extend()
        self.taskextend()
        self.reload()
        self.logger.info('-' * 48)


DailyTask().main()

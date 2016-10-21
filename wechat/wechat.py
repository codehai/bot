# coding:utf8

import os
import unittest
from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import argparse
import json

PLATFORM_VERSION = '4.4.4'

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

parser = argparse.ArgumentParser(description="微信助手")
parser.add_argument("device",help="连接机器地址")
parser.add_argument("server",help="appium服务端地址")
parser.add_argument("-u", "--user", action="store",help="待添加人")
args = parser.parse_args()

class Wechat():
    '''微信助手'''
    def __init__(self):

        desired_caps = {
            'platformName': 'Android',
            'deviceName': args.device, 
            'udid':args.device,
            'platformVersion': PLATFORM_VERSION,
            'appPackage': 'com.tencent.mm',
            'appActivity':'.ui.LauncherUI',
            'noReset':True,
            'app': PATH('./wechat.apk'),
        }
        print desired_caps
        server = 'http://localhost:%s/wd/hub' %(args.server)
        print server
        self.driver = webdriver.Remote(server, desired_caps)
        # if not self.driver.is_app_installed('com.tencent.mm'):
        #     self.driver.install_app(app)
        #     self.login()
        # self.username = username
        # self.password = password
        self.driver.launch_app()
        self.driver.implicitly_wait(10)

    def login(self):
        '''登录'''
        self.driver.find_element_by_id('com.tencent.mm:id/c7m').click()
        self.driver.find_element_by_id('com.tencent.mm:id/b9c').click()
        self.driver.find_element_by_id('com.tencent.mm:id/b8r').find_element_by_id('com.tencent.mm:id/fo').send_keys(self.username)
        self.driver.find_element_by_id('com.tencent.mm:id/b8s').find_element_by_id('com.tencent.mm:id/fo').send_keys(self.password)
        self.driver.find_element_by_id('com.tencent.mm:id/b8t').click()
        if self.has_element(By.CLASS_NAME,'android.widget.LinearLayout') and self.has_element(By.ID,'com.tencent.mm:id/ayq'):
                print self.driver.find_element_by_id('com.tencent.mm:id/ayq').text
                self.quit()
        else:
            print 'login success'

    def add(self,uS):
        '''加人'''
        if not self.has_element(By.XPATH,'//android.widget.RelativeLayout[contains(@content-desc,"更多功能按钮")]'):
            print 'no 更多功能按钮'
        else:
            self.driver.find_element_by_xpath('//android.widget.RelativeLayout[contains(@content-desc,"更多功能按钮")]').click()
            self.driver.find_elements_by_id('com.tencent.mm:id/i6')[1].click()
            for u in uS:
                self.driver.find_element_by_id('com.tencent.mm:id/fo').send_keys(u)
                self.driver.find_element_by_id('com.tencent.mm:id/atv').find_element_by_class_name('android.widget.RelativeLayout').click()
                if self.has_element(By.XPATH,'//android.widget.Button[contains(@text,"添加到通讯录")]'):
                    self.driver.find_element_by_xpath('//android.widget.Button[contains(@text,"添加到通讯录")]').click()
                    if self.has_element(By.XPATH,'//android.widget.TextView[contains(@text,"发送")]'):
                        self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"发送")]').click()
                        print '添加已发送',u
                        sleep(6)
                    else:
                        print '!!!',u
                    self.driver.find_element_by_xpath('//android.widget.ImageView[contains(@content-desc,"返回")]').click()
                    sleep(9)
                elif self.has_element(By.XPATH,'//android.widget.Button[contains(@text,"发消息")]'):
                    print '已添加',u
                    sleep(5)
                    self.driver.find_element_by_xpath('//android.widget.ImageView[contains(@content-desc,"返回")]').click()
                elif self.has_element(By.ID,'com.tencent.mm:id/atp'):
                    print self.driver.find_element_by_id('com.tencent.mm:id/atp').text
                else :
                    print '???',u
            self.driver.find_element_by_xpath('//android.widget.ImageView[contains(@content-desc,"返回")]').click()
    
    def get_people(self):
        '''获得朋友电话信息'''
        self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"通讯录")]').click()
        # sleep(1)
        self.driver.implicitly_wait(10)
        people_name_list = []
        people_info_list = []
        while True:
            people_list = self.driver.find_elements_by_xpath('//android.view.View')
            for people in people_list:
                if people.text and people.text not in people_name_list:
                    people_info = {}
                    people_info['name'] = people.text
                    people_name_list.append(people.text)
                    people.click()
                    if self.has_element(By.XPATH,'//android.widget.TextView[contains(@text,"电话号码")]'):
                        phone = self.driver.find_element_by_id('com.tencent.mm:id/bxp').find_element_by_class_name('android.widget.TextView').text
                        people_info['phone'] = phone
                    self.driver.find_element_by_xpath('//android.widget.ImageView[contains(@content-desc,"返回")]').click()
                    people_info_list.append(people_info)
            if self.has_element(By.ID,'com.tencent.mm:id/aad'):
                break
            else:
                self.driver.swipe(400, 1000, 400, 100, 1000)
        print json.dumps(people_info_list,ensure_ascii=False)

    def has_element(self,selector,element):
        '''有无给定的元素'''
        try:
            self.driver.find_element(selector,element)
            return True
        except Exception, e:
            return False

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    app = Wechat()
    # app.login()
    # app.add()
    try:
        if args.user:
            app.add(json.loads(args.user))
        else:
            app.get_people()
    except Exception, e:
        raise
    finally:
        app.quit()

# -*- coding: utf-8 -*-
import os
import time
import json
import threading
import uuid
import shutil

import logging
from logging import handlers

import toml
from sdk.appmanager import ApplicationManager
from urllib.parse import urlparse

from flask import Flask,request
from sqlalchemy import create_engine,String,JSON,Integer
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,Session
from werkzeug.utils import secure_filename

################ 配置区，一般不用动 ###############
class Config:
    logFile = os.path.join("./app","logs","common.log")
    backCount = 7
    when = "midnight"
    fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    dbFile = os.path.join("./app","notice.db")
    expireDays = 365
    port = 5000
    tmpDir = os.path.join("./app","tmp")

    @classmethod
    def show(cls):
        print("*********** notice 服务配置如下 ***********")
        print("日志文件是 {}".format(cls.logFile))
        print("日志文件备份数是 {}".format(cls.backCount))
        print("日志文件备份频率是 {}".format(cls.when))
        print("日志文件格式是 {}".format(cls.fmt))
        print("db 文件格式 {}".format(cls.dbFile))
        print("db 数据保存最长 {} 天".format(cls.expireDays))
        print("notice 服务监听端口是 {}".format(cls.port))
        print("*********** notice 服务配置如上 ***********")

    @classmethod
    def resolver(cls):
        print("解析配置文件")
        path = os.path.join("/app","notice.toml")
        if not os.path.exists(path):
            print("配置文件不存在，使用默认配置")
            return
        if not os.path.isfile(path):
            raise ValueError("{} 不是有效的配置文件".format(path))
        print("配置文件是 {}".format(path))
        config = toml.load(path)
        for key,val in config.items():
            if hasattr(cls,key):
                setattr(cls,key,val)
        if not os.path.dirname(Config.tmpDir):
            print("创建临时目录 ".format(Config.tmpDir))
            os.mkdir(Config.tmpDir)


Config.resolver() and Config.show()
################ 配置区 ###############


#######################日志接口，对内使用，一般不需要动##############################
class Logger(object):
    def __init__(self,filename,when,backCount,fmt):
        '''
        日志接口，一般直接初始化后，调用该类的 info、warn、debug、error、critical 接口即可；
        :param filename: 要保存的日志文件位置，带文件夹路径和文件名，默认保存在用户目录下 notice 文件夹的 common.log 文件中；
        :param when: 日志会定时分割，默认每天凌晨会生成新的日志文件，相关参数可以参考 TimedRotatingFileHandler 类的说明；
        :param backCount: 回滚的日志文件最大数量;
        :param fmt: 输出的日志格式；

        Example:
        >>> log = Logger()
        >>> log.info("info message")
        >>> log.debug("debug message")
        >>> log.warn("warn message")
        >>> log.error("error message")
        >>> log.critical("critical message")
        '''
        if not isinstance(backCount,int) or backCount < 0:
            raise ValueError("backCount 参数必须是大于 0 的整数，当前值是" + str(backCount))
        rootDir = os.path.dirname(filename)
        if not os.path.isdir(rootDir):
            print("{} 文件夹不存在，需要先创建".format(rootDir))
            os.mkdir(rootDir)

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt) # 设置日志格式
        sh = logging.StreamHandler() # 往屏幕上输出
        sh.setFormatter(format_str) # 设置屏幕上显示的格式
        self.logger.setLevel(logging.INFO)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8') # 往文件里写入
        th.setFormatter(format_str) # 设置文件里写入的格式
        self.logger.addHandler(sh) # 把对象加到logger里
        self.logger.addHandler(th)


    def info(self,msg):
        self.logger.info(msg)

    def warn(self,msg):
        self.logger.warning(msg)

    def debug(self,msg):
        self.logger.debug(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)
log = Logger(Config.logFile,Config.when,Config.backCount,Config.fmt) # 全局日志对象，从这里开始，下面所有接口都可以使用这个实例进行日志记录，建议必要信息都存下来
#######################日志接口##############################

#######################数据库区，对内存储使用#############################
engine = create_engine("sqlite:///"+Config.dbFile, echo=True)

class Base(DeclarativeBase):
    pass

class Record(Base):
    __tablename__ = "record"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    category: Mapped[str] = mapped_column(String(10)) # 种类，短信、邮件 等
    createdAt: Mapped[int] = mapped_column(Integer) # 创建时间戳，秒
    result: Mapped[int] = mapped_column(Integer)  # 结果，0 表示成功，1 表示失败
    reason: Mapped[str] = mapped_column(String(100)) # 失败原因，需要和 result 一起使用
    content: Mapped[str] = mapped_column(JSON(),nullable=True) # 内容，反正每个方法要写什么就自己写什么

class Clean:
    def __init__(self):
        self.lock = threading.Lock()
        self.lastCleanAt = 0

    def do(self):
        now = int(time.time())
        if now - self.lastCleanAt > 3600:
            log.info("距离上次清理过早，不需要清理")
            return

        try:
            self.lock.acquire(timeout=1)
        except:
            return
        try:
            log.info("准备清理过期数据")
            with Session(engine) as sec:
                thresholdTime = now - Config.expireDays * 86400
                sec.query(Record).where("createdAt < >",thresholdTime).delete()
                sec.commit()
                log.info("清理完毕")
        except Exception as e:
            log.error("清理失败: {}".format(e))
        finally:
            self.lastCleanAt = int(time.time())
            self.lock.release()


Record.metadata.create_all(engine)
clean = Clean()
#######################数据库区#########################################



############################## 自定义接口区，需要根据项目上的实际情况进行对接 #########
def send_platform(platform:str,content,receivers:list=None,key:str=None,secret:str=None,appid:str=None,webhooks:list=None):
    platforms = ['wechat','dingtalk','feishu']
    error_list = []
    if platform in platforms:

        if (receivers is None or len(receivers) == 0) and (webhooks is None or len(webhooks) == 0):
            error_info = {"type": "no receivers&webhooks","errcode": "200","errmsg": "接收人为空"}
            error_list.append(json.dumps(error_info))
            return error_list
        
        app = ApplicationManager.create_application(platform)
        notice = app.createClient(app.newAuthentication(key,secret)).getNotification()
        
        if receivers is not None and len(receivers) > 0:
            otoRobot = notice.getOtoRobot(appid)
            msg = otoRobot.createMessageWithDefault(receivers=receivers,content=content)
            resp = otoRobot.send(msg)
            if resp.getErrCode() != '0':
                error_info = {
                    "type": "oto_robot",
                    "errcode": resp.getErrCode(),
                    "errmsg": resp.getErrMsg()
                }
                error_list.append(json.dumps(error_info))

        if webhooks is not None and len(webhooks) > 0:
            for url in webhooks:
                robot = notice.getWebhookRobot(url)
                msg = robot.createMessageWithDefault(content)
                resp = robot.send(msg)
                if resp.getErrCode() != '0':
                    error_info = {
                        "type": "webhook_robot",
                        "errcode": resp.getErrCode(),
                        "errmsg": resp.getErrMsg()
                    }
                    error_list.append(json.dumps(error_info))
        
    else:
        error_info = {"type": "unsupported platform","errcode": "200","errmsg": "暂不支持该平台"}
        error_list.append(json.dumps(error_info))
    return error_list
        

############################# 自定义接口区 #######################################


############ notice 服务监听区######################

app = Flask(__name__)
@app.route("/notice/")
@app.route("/notice/platform",methods=["post"])
def platform():
    log.info('发送第三方平台请求')
    data = request.get_json()
    body = {}
    keys = ['platform','receivers','content','key','secret','agentid','webhook_urls']
    for key in keys:
        if key in data:
            body[key] = data[key]
    log.info("接收参数是 {}".format(body))
    item = Record(category='第三方平台',result=0,createdAt=int(time.time()),content=json.dumps(body))
    resp = 'ok'
    errlist = send_platform(
        platform=body.get('platform'),
        content=body.get('content'),
        receivers=body.get('receivers'),
        key=body.get('key'),
        secret=body.get('secret'),
        appid=body.get('agentid'),
        webhooks=body.get('webhook_urls')
    )
    log.info("存储结果到 db")
    if errlist:
        error_list = []
        for err in errlist:
            log.error("推送失败: {}".format(err))
            error_list.append(err)
        resp = ', '.join(error_list)
        item.result = 1
        item.reason = resp
    with Session(engine) as sec:
        try:
            sec.add(item)
            sec.commit()
        except Exception as e:
            log.error("存储失败: {}".format(e))
    clean.do()
    return resp

if __name__ == '__main__':
    app.run(debug = True,host="0.0.0.0",port=Config.port)

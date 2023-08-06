from queue import Queue
from .db import model
from .db import sqlite as kcwsqlite
import threading,time,os,hashlib,random
queuesdbpath=os.path.split(os.path.realpath(__file__))[0]+"/Queues"
class model_task(model.model):
    "任务"
    config={'type':'sqlite','db':queuesdbpath}
    model.dbtype.conf=config
    table="Queues" 
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "taskid":model.dbtype.varchar(LEN=32,DEFAULT=''),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=1024,DEFAULT=''),      #名称
        "describes":model.dbtype.varchar(LEN=2048,DEFAULT=''),  #描述
        "code":model.dbtype.int(LEN=11,DEFAULT=2),              #状态码 0成功 1失败 2等待中 3正在执行  4完成
        "msg":model.dbtype.text(),                              #状态描述
        "error":model.dbtype.text(),                            #异常信息
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0)            #添加时间
    }
class Queues():
    __globalqueue=None
    def start():
        Queues.__globalqueue=Queue()
        t=threading.Thread(target=Queues.__messagequeue)
        t.daemon=True
        t.start()
    def __messagequeue():
        if not os.path.isfile(queuesdbpath):
            t=model_task()
            t.create_table()
        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where(True).delete()
        while True:
            if not Queues.__globalqueue.empty(): 
                value=Queues.__globalqueue.get()
                kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":3,"msg":"正在执行","error":""})
                if value['args']:
                    try:
                        value['target'](*value['args'])
                    except Exception as e:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,"msg":"失败","error":str(e)})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"msg":"执行完成"})
                else:
                    try:
                        value['target']()
                    except Exception as e:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":1,"msg":"失败","error":str(e)})
                    else:
                        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").where("taskid = '"+value['task']['taskid']+"' and code!=4").update({"code":4,"msg":"执行完成"})
            else:
                time.sleep(1)
    def insert(target,args=None,title="默认任务",describes="",msg='等待中'): #add_queue
        """添加队列
        
        target 方法名  必须

        args 方法参数 非必须  如

        title 任务名称

        describes 任务描述

        return taskid
        """
        if not os.path.isfile(queuesdbpath):
            t=model_task()
            t.create_table()
        ttt=int(time.time())
        print(ttt)
        m = hashlib.md5()
        m.update((str(ttt)+str(random.randint(100000,999999))).encode(encoding='utf-8'))
        taskid=m.hexdigest()
        task={"taskid":taskid,"title":title,"describes":describes,"code":2,"msg":msg,"error":"","addtime":ttt}
        key={"target":target,"args":args,"task":task}
        Queues.__globalqueue.put(key)
        kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").insert(task)
        return taskid
    def getall(code=''):
        """获取全部队列

        code 1获取失败的任务   2获取等待中的任务   3获取正在执行中的任务  4获取执行完成的任务
        """
        if not os.path.isfile(queuesdbpath):
            t=model_task()
            t.create_table()
        where=False
        if code:
            where="code="+code
        # else:
        #     where="code!=4"
        return kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").field("taskid,title,describes,code,msg,error,addtime").where(where).select()
    def status(taskid):
        """获取任务状态
        
        taskid  任务id
        """
        if not os.path.isfile(queuesdbpath):
            t=model_task()
            t.create_table()
        return kcwsqlite.sqlite().connect(queuesdbpath).table("Queues").field("taskid,title,describes,code,msg,error,addtime").where("taskid",taskid).find()
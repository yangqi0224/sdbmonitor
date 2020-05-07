import os
import datetime
import logging
import socket

_meminfo_ = "/proc/meminfo"
_cpuinfo_ = "/proc/cpuinfo"
_sdbpath_ = "/opt/sequoiadb"
_sdbuser_ = 'sdbadmin'
_sdbpwd_ = 'sdbadmin'
logger = logging.getLogger()


def __init__():
    """
    初始化日志信息
    :return:
    """
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("restart.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_currtime():
    """
    获取当前时间
    :return: current time
    """
    cur = datetime.datetime.now()
    return cur


def get_mem():
    """
    读取/proc/meminfo文件，获取内存使用信息
    """
    command = "cat " + _meminfo_ + " |awk '{print $2}'"
    logger.info(command)
    mem = os.system(command)
    logger.info(mem)
    ava = mem[2]
    return ava


def get_prinode():
    """
    找出本机的主节点
    """
    command = _sdbpath_ + "/bin/sdblist -l -r data|awk 'NR>1&&$7==\"Y\"{print $2}'"
    logger.info(command)
    sdblist = os.system(command)
    logger.info(sdblist)
    return sdblist


def get_session():
    """
    获取正在执行的会话数量
    :return:
    """
    new_sdb = _sdbpath_ + '/bin/sdb "db = new Sdb(\'localhost\',11810,\'' + _sdbuser_+'\',\''+_sdbpwd_+'\')"'
    logger.info(new_sdb)
    os.system(new_sdb)
    session_size = _sdbpath_ + '/bin/sdb "db.snapshot(2,{Status:\'Runnint\',Type:\'ShardAgent\'}).size()"'
    size = os.system(session_size)
    logger.info(session_size+' is '+size)
    return size
#coding:utf-8
import os
import datetime
import logging
import sys
from getopt import getopt
import socket

_meminfo_ = "/proc/meminfo"
_cpuinfo_ = "/proc/cpuinfo"
_sdbpath_ = "/opt/sequoiadb"
_sdbuser_ = 'sdbadmin'
_sdbpwd_ = 'sdbadmin'
logger = logging.getLogger()


def log_init():
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
    command = "cat " + _meminfo_ + " |awk 'NR==3{print $2}'"
    logger.info(command)
    mem = os.system(command)
    logger.info(mem)
    return mem


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
    new_sdb = _sdbpath_ + '/bin/sdb "db = new Sdb(\'localhost\',11810,\'' + _sdbuser_ + '\',\'' + _sdbpwd_ + '\')"'
    logger.info(new_sdb)
    os.system(new_sdb)
    session_size = _sdbpath_ + '/bin/sdb "db.snapshot(2,{Status:\'Runnint\',Type:\'ShardAgent\'}).size()"'
    size = os.system(session_size)
    logger.info(session_size + ' is ' + size)
    return size


def help_info():
    print("-u or --user         sdb user name default sdbadmin \n" +
          "-p or --password     sdb password default sdbadmin \n" +
          "-h or --help         get help info")


def __init__(args):
    """
    初始化参数
    :param args:
    :return:
    """
    args,opts = getopt(args, "-u-p:-h", ['user=', 'password=', 'help'])

    for k,v in opts:
        if k in ('-h', '--help'):
            help_info()
            sys.exit(0)
        if k in ('-u', '--user'):
            # global _sdbuser_
            global _sdbuser_
            _sdbuser_ = v
        if k in ('-p', '--password'):
            # global _sdbpwd_
            global _sdbpwd_
            _sdbpwd_ = v
        else:
            help_info()
            sys.exit(0)


def node_restart(node):
    """
    重启指定节点并重新选主
    :param node:
    :return:
    """
    command = _sdbpath_+"/bin/sdblist -l|grep '+node+'|awk '{print $8}'"
    logger.info(command)
    gp = os.system(command)
    logger.info("Restart node localhost:" + node + " group is "+gp)
    sdbstop = _sdbpath_+"/bin/sdbstop -p"+node
    sdbstart = _sdbpath_+"/bin/sdbstart -p"+node
    os.system(sdbstop)
    logger.info(sdbstop)
    os.system(sdbstart)
    logger.info(sdbstart)
    new_sdb = _sdbpath_ + '/bin/sdb "db = new Sdb(\'localhost\',11810,\'' + _sdbuser_ + '\',\'' + _sdbpwd_ + '\')"'
    os.system(new_sdb)
    reelect = _sdbpath_ + '/bin/sdb "db.getRG(\''+gp+').reelect"'
    os.system(reelect)
    logger(reelect)


def main():
    """
    判断是否重启：
    如果内存可是用量小于：40g
    并且当前正在执行的会话数小于：134
    :return:
    """
    avamem = get_mem()
    prinode = get_prinode()
    session_size = get_session()
    if avamem<40*1024*1025*1024:
        if session_size<134:
            for node in prinode:
                node_restart(node)


if __name__ == '__main__':
    __init__(sys.argv[1:])
    log_init()
    main()
import os
import socket
import datetime
import sys


def getpath(path):
    os.system("/opt/sequoiadb/bin/sdblist -l |sort |awk 'NR>2{print p}{p=$0}'|awk '{print $10}' >"+path+"/path.txt")
    allp = open(path+"/path.txt")
    pa = []
    for lin in allp:
        pa.append(lin.strip()+'diaglog/sdbdiag.log')
    return pa


def getname(path):
    os.system("/opt/sequoiadb/bin/sdblist -l |sort |awk 'NR>2{print p}{p=$0}'|awk '{print $2}' >"+path+"/name.txt")
    os.system("/opt/sequoiadb/bin/sdblist -l |sort |awk 'NR>2{print p}{p=$0}'|awk '{print $8}' >"+path+"/group.txt")
    group = open(path+"/group.txt")
    alln = open(path+"/name.txt")
    na = []
    gr = []
    allname = []
    for lin in alln:
        na.append(lin.strip())
    for lin in group:
        gr.append(lin.strip())
    for l in range(0, na.__len__()):
        allname.append(socket.gethostname().strip()+'_'+na[l]+'_'+gr[l])
    return allname


path = os.path.abspath(os.path.join(os.getcwd()))
# -1代表检查所有日期的日志，0代表当日日志，n代表当前日至前n日内的日志（n+1天）
days = -1
logday = []
logday2 = []
if sys.argv.__len__() > 1:
    le = int(sys.argv[1])
    if le < 0 or le > 30:
        print("Illegal parameter")
        quit()
    else:
        days = le
if days != -1:
    curr = datetime.datetime.now()
    n = 0
    while n <= days:
        logday.append((curr+datetime.timedelta(days=0-n)).strftime('%Y-%m-%d'))
        logday2.append((curr+datetime.timedelta(days=0-n)).strftime('%Y%m%d'))
        n = n+1
paths = getpath(path)
svcnames = getname(path)

n = 0

for i in paths:
    print("current node :" + svcnames[n])
    if len(logday) > 1:
        error = open(path+"/"+svcnames[n].strip()+'.error_'+logday2[-1]+'_'+logday2[0], 'w')
    elif len(logday) > 0:
        error = open(path+"/"+svcnames[n].strip()+'.error_'+logday2[-1], 'w')
    else:
        error = open(path+"/"+svcnames[n].strip()+'.error', 'w')
    n = n+1
    node = open(i)
    flag = False
    for line in node:
        if line.__contains__("ERROR"):
            if logday.__len__() > 0:
                for dates in logday:
                    if dates in line:
                        flag = True
                        break
            else:
                flag = True
        if line == '\n':
            flag = False
        if line == '':
            break
        if flag:
            error.write(line)

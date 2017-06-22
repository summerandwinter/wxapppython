from datetime import datetime, timezone
from dateutil.tz import tzutc, tzlocal

def timebefore(d):  
    chunks = (  
                       (60 * 60 * 24 * 365, u'年'),  
                       (60 * 60 * 24 * 30, u'月'),  
                       (60 * 60 * 24 * 7, u'周'),  
                       (60 * 60 * 24, u'天'),  
                       (60 * 60, u'小时'),  
                       (60, u'分钟'),  
     )  
    #如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime):
        d = datetime(d.year,d.month,d.day)
    now = datetime.now(timezone.utc)
    delta = now - d
    #忽略毫秒
    before = delta.days * 24 * 60 * 60 + delta.seconds
    #刚刚过去的1分钟
    if before <= 60:
        return '刚刚'
    if(d.year != now.year):
        return '%s年%s月%s日'%(d.year,d.month,d.day)
    if(before > 60 * 60 * 24 * 7):
        return '%s月%s日'%(d.month,d.day) 
    for seconds,unit in chunks:
        count = before // seconds
        if count != 0:
            break
    return str(count)+unit+"前"

d = datetime(2017,6,22,13,31)
time = timebefore(d)
print(time)    
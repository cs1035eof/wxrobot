# coding:utf-8
import itchat, time
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
import random

# 一些备选问候语
greetWorkTimeList = []
greetWorkTimeList.append(u'好好工作，晚上争取把冒险模式开了。')
greetWorkTimeList.append(u'好好工作，顺便把圣教军也解锁了。')
greetWorkTimeList.append(u'好好工作，死灵法师已经上线了，不要198，只要58。')
greetWorkTimeList.append(u'好好工作，能不能玩上“狗头人与地下世界就看你的了”。')
greetWorkTimeList.append(u'好好工作，伊利丹又出新皮肤了。')
greetWorkTimeList.append(u'好好工作，太空服的李奥瑞克真是酷毙了，你会喜欢的。')
greetWorkTimeList.append(u'好好工作，据说今年的暴雪嘉年华有惊喜噢。')
greetWorkTimeList.append(u'好好工作，诺娃的隐秘任务你就可以顺利带回家了。')

greetNoneWorkTimeList = []
greetNoneWorkTimeList.append(u'来局炉石？')
greetNoneWorkTimeList.append(u'风暴一起开黑去？')
greetNoneWorkTimeList.append(u'据说D3又开新赛季了，一起开荒去？')
greetNoneWorkTimeList.append(u'我的魔法会把你撕成碎片')
greetNoneWorkTimeList.append(u'知道吗，你如果在暗黑3里这样做的话，我甚至理都不会理你，唉，开始怀念那种感觉了。')
greetNoneWorkTimeList.append(u'唉，要是有一名追随者就好办多了。寇马克，你到底死哪去了?。')
greetNoneWorkTimeList.append(u'只有蠢货才会涉足连天使都不敢踏足的地方。')
greetNoneWorkTimeList.append(u'曾经有个战士以为把灵魂石插在自己额头上还可以安然无恙，这真是个无聊可悲的故事。')
greetNoneWorkTimeList.append(u'你知道吗，我其实并不坏，真的，我只是被误解了。')
greetNoneWorkTimeList.append(u'我走到哪里，哪里就变成了奶牛关。')
greetNoneWorkTimeList.append(u'伙计，我见过的人比你吃过的草还多，而且他们统统都成了我的粉丝。')
greetNoneWorkTimeList.append(u'时间就是金钱，朋友。但是你两样都没有。')
greetNoneWorkTimeList.append(u'霜之哀伤在哀嚎。')
greetNoneWorkTimeList.append(u'你知道吗?时空枢纽最棒的地方就是，每隔二十分钟，我就能看到一个全新的世界。')

# 问候时间列表
timeList = []
timeList.append(8 * 3600 + 15 * 60 + 22)
timeList.append(9 * 3600 + 15 * 60 + 37)
timeList.append(10 * 3600 + 15 * 60 + 11)
timeList.append(11 * 3600 + 15 * 60 + 3)
timeList.append(14 * 3600 + 15 * 60 + 55)
timeList.append(15 * 3600 + 15 * 60 + 40)
timeList.append(16 * 3600 + 15 * 60 + 51)
timeList.append(17 * 3600 + 15 * 60 + 19)
timeList.append(18 * 3600 + 15 * 60 + 32)
timeList.append(19 * 3600 + 15 * 60 + 48)
timeList.append(20 * 3600 + 15 * 60 + 30)
timeList.append(21 * 3600 + 15 * 60 + 20)
timeList.append(22 * 3600 + 15 * 60 + 10)
timeList.sort(reverse=True)
# print(timeList)

work_time_begin = 8 * 3600 + 30 * 60 + 0
work_time_end = 18 * 3600 + 30 * 60 + 0

# 获取下一次的问候时间
def get_next_tick_time(srcTime):
    lenList = len(timeList)
    if lenList < 1:
        return srcTime + dt.timedelta(hours=1)
	
    timeListStart = timeList[lenList - 1]
    timeListFinish = timeList[0]
	
    total_sec = srcTime.hour * 3600 + srcTime.minute * 60 + srcTime.second
    nextTime = srcTime - dt.timedelta(seconds=total_sec)
    print('total_sec = %d' % total_sec)
    print(dt.datetime.strftime(nextTime, '%Y-%m-%d %H:%M:%S'))	
	
    if total_sec > timeListFinish:
        nextTime += dt.timedelta(days=1)
        nextTime += dt.timedelta(seconds=timeListStart)
        return nextTime

    i = 1
    while i < lenList:
        print('i=%d' % i)
        if total_sec > timeList[i]:
            nextTime += dt.timedelta(seconds=timeList[i - 1])
            print(dt.datetime.strftime(nextTime, '%Y-%m-%d %H:%M:%S'))
			
            return nextTime
        else:
            i += 1

    return nextTime + dt.timedelta(seconds=timeListStart)

def is_work_time(srcTime):
    ret = False
    wday = srcTime.weekday()
    
    if wday == 5 or wday == 6:
        return False
    
    total_sec = srcTime.hour * 3600 + srcTime.minute * 60 + srcTime.second
    print('total_sec = %d' % total_sec)
	
    if total_sec < work_time_begin or total_sec > work_time_end:
        return False
	
    return True
	
def tick():
    friendName=u'wxrobottest'
    users = itchat.search_friends(name=friendName) # 找到微信好友的名称
    if len(users) <= 0:
        print('Not found friend %s.' % friendName)
        print('\a\a\a')
        return

    print('len(users) = %d' % len(users) )
    print('users = %s' % users)
    userName = users[0]['UserName']
    print('userName = %s' % userName)

    now = dt.datetime.now()     # 现在的时间
    
    greeting = ""
    if is_work_time(now):
        greeting = random.sample(greetWorkTimeList,1)[0]
    else:
        greeting = random.sample(greetNoneWorkTimeList,1)[0]
	
    print('\a')	
    itchat.send(u'%s'%(greeting), toUserName=userName) # 发送问候语给微信好友
    time.sleep(10)
    now = dt.datetime.now()     # 现在的时间
    nextTickTime = get_next_tick_time(now) # 获取下一次问候的时间
    my_scheduler(nextTickTime)

def my_scheduler(runTime):
    scheduler = BackgroundScheduler() # 生成对象
    scheduler.add_job(tick, 'date', run_date=runTime)  # 在指定的时间，只执行一次
    scheduler.start()

if __name__ == '__main__':
    #itchat.auto_login(enableCmdQR=True) # 在命令行中展示二维码，默认展示的是图片二维码
    itchat.auto_login(hotReload=True) # 这个是方便调试用的，不用每一次跑程序都扫码
	
    now = dt.datetime.now() # 获取当前时间
    nextTickTime = get_next_tick_time(now) # 获取下一次问候的时间
    print(dt.datetime.strftime(nextTickTime, '%Y-%m-%d %H:%M:%S'))
    my_scheduler(nextTickTime) # 启用定时操作
	
    itchat.run() # 跑微信服务
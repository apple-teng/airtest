# -*- encoding=utf8 -*-
__author__ = "xiaomei.teng"
import logging
from airtest.core.api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# using(r"E:\airTest\airtest\MoreResetMaps.air")
# from MoreResetMaps import *
# using(r"E:\airTest\airtest\EnterQuitDevice.air")
# from EnterQuitDevice import *


poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
auto_setup(__file__)
logging.basicConfig(level=logging.DEBUG)

# '''
# =========手机端时区操作==========
# 难点：
# 设置时区，2种方案
# 1.root手机，直接通过命令设置，图像操作只有ecovacsHome  --》root手机失败
# 2.图形界面，把所有时区的城市写成列表，循环通过搜索set-text设置  --》可以实现
# --已解决
# 注意：
# 1.app关闭后，时区设置界面是否还在，，是否需要从设置一步步进入
# '''

timezone_city = ['芝加哥','东京','柏林 (德国)', '巴黎', '伦敦','莫斯科','萨马拉','叶卡捷琳堡','新西伯利亚','克拉斯诺亚尔斯克','阿纳德尔','伯尔尼','安卡拉','阿布扎比']

def set_timezone(city):    
    # 选择时区
    poco(text="时区").click()

    # 点击搜索
    poco(desc="搜索查询").click()

    # 搜索框中填写城市
    poco("android:id/search_src_text").set_text(city)
    #对搜索框中的结果进行处理
    try:
        # 搜索结果符合
        if city in poco(name="android:id/text1").get_text():
            # 设置时区
            poco("android:id/text1").click()
            sleep(2)
            '''
            时区设置完毕，切换ecovacsHome进行操作
            '''
        else:
            logging.info(city + 'no timezone found!')
    finally:
        pass
#         不管找没找到列表中的时区，程序都回到主界面
#         home()

    

# '''
# 手机本身操作和app单操作都ok的前提下，有个难点：相互切换
# 1.进入设置（name :  android.widget.TextView 
# 	       text :  设置 ）
# 2.找到时间与日期的设置（由于该项设置不在进入页面的显示范围，
# 处理方法：1.滑动页面，但是滑动范围不好确定
# 2. TBD）
# '''
timezone_element=poco(text="日期和时间")
def loop_find_timezone():
    # 前提：保证程序开始时时处于home界面
    home()
    # 进入设置
    poco(name="设置",text="设置").click(sleep_interval=5)
    # 为进入系统，下滑
    poco(name='com.android.settings:id/category').swipe('up')
    poco(text="系统").click(sleep_interval=5)
    i = 0
    while True:
        if timezone_element.exists():
            timezone_element.click()
            break
#         设定最多滑动次数（因为系统中只有4个category元素）
        elif i < 5:
#             按category坐标来滑动
            x,y=poco.get_position()
            dir=[0,-0.5]
            poco.swipe([x,y],dir)
            i+=1
        else:
            raise PocoNoSuchNodeException
   
    
    

def start_close_app(action='start'):
    '''
    打开关闭app
    arg：action(obj:str)
        -start(default)
        -close
    '''    
    if action == 'start':
        # 打开ecovacsHome app
        start_app('com.eco.global.app')
        sleep(10)
    elif action == 'close':
        # 关闭app
        stop_app('com.eco.global.app')
        sleep(5)
        


# '''
# =========app端勿扰+预约设置=============
# 1.不在勿扰时间内的（勿扰时间设置的尽量的小），集中测试完，再测试勿扰时间内（勿扰时间设置尽量的大）
# 2.注意预约条数的限制，考虑是没测完一条删一条，还是设置teardown
# 难点：
# 1.时间都是不好输入，需要滑动
# '''
def schedule_clean(clean_type):
    '''
    设置预约
    arg:clean_type(obj:str)
        -auto
        -area
    '''
    # 点击“+”,唤出下来框
    poco(name='com.eco.global.app:id/right').click()

    if clean_type == "auto":
        # 点击“自动预约”
        poco(name='com.eco.global.app:id/auto_add' , text='预约自动清扫').click()

    elif clean_type == "area":
         # 点击“区域预约”
        poco(name='com.eco.global.app:id/area_add' , text='预约区域清扫').click()
    
    # 在当前时间的基础上，下滑来实现1min后的预约
    # '''
    # 1.选择分钟--（采用绝对定位或元素列表），
    # 2.分钟下滑1个--swipe使用函数自定义的“up”
    # '''
    poco(name='android.widget.NumberPicker').\
    child(name='android:id/numberpicker_input')[1].swipe('up')
    
# #     在勿扰模式下，提交保存时会有弹框
#     try:
#         有弹框
#     finally:
#         点击保存
        

'''
保存时要注意，勿扰时间保存，是有弹框的
'''
# # 点击保存预约，并等待3s
# poco(resourceId='com.eco.global.app:id/right').click(sleep_interval=3)

# logging.info('自动清扫设置完成')
'''
设置完成后，去清扫页面查看预约出发的消息
1.等待检查消息时间未1min
2.检查主机运行状态（调用张雷写好的函数） 和 检查弱消息弹框
3.结束主机运行（调用张雷写好的函数）
'''

# # 点击“区域预约”
# # 点击“+”,唤出下来框
# poco(name='com.eco.global.app:id/right').click()

# # 点击“区域预约”
# poco(name='com.eco.global.app:id/area_add' , text='预约区域清扫').click()

# # 设置预约时间
# poco(name='android.widget.NumberPicker').child(name='android:id/numberpicker_input')[1].swipe('up')

# # 选择清扫区域
# # 点击“清扫区域按钮”
# poco(name='com.eco.global.app:id/tv_appoint_area_value',text="未选择").click('center',3)

# # 选择地图中的区域
# '''
# 难点：
# 无法选择区域，因为地图上没有元素，类似是个大图层
# --》使用图像识别出区域A（只要是整图，必有A区域，且A的图像显示不变）
# '''
# sleep(5)
# touch(Template(r"tpl1585386736702.png", record_pos=(0.274, 0.056), resolution=(576, 1024)))

# # 点击保存预约，并等待3s
# poco(resourceId='com.eco.global.app:id/right').click(sleep_interval=3)

# logging.info('区域清扫设置完成')





            
           

if __name__ == '__main__':
    # 循环设置时区
    for city in timezone_city: 
        loop_find_timezone()
        set_timezone(city)
        sleep(5)
        home()
        start_close_app('start')
        # 进入设备-更多

# -*- encoding=utf8 -*-
__author__ = "xiaomei.teng"
import logging
from airtest.core.api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)
logging.basicConfig(level=logging.DEBUG)

'''
=========手机端时区操作==========
难点：
设置时区，2种方案
1.root手机，直接通过命令设置，图像操作只有ecovacsHome  --》root手机失败
2.图形界面，把所有时区的城市写成列表，循环通过搜索set-text设置  --》可以实现
--已解决
注意：
1.app关闭后，时区设置界面是否还在，，是否需要从设置一步步进入
'''

# timezone_city = ['芝加哥','东京','柏林 (德国)', '巴黎', '伦敦','莫斯科','萨马拉','叶卡捷琳堡','新西伯利亚','克拉斯诺亚尔斯克','阿纳德尔','伯尔尼','安卡拉','阿布扎比']

# # 选择时区
# # poco(text="时区").click()
# poco(resourceId='android:id/title',text="选择时区").click()

# # 点击搜索
# # poco("android:id/search_src_text").click()
# poco(resourceId='com.android.settings:id/search',desc="搜索").click()
# # 循环设置时区
# poco("android:id/search_src_text").set_text(timezone_city[0])

# # 获取对应时区
# try:
#     if poco(name="android:id/text1").get_text()==timezone_city[0]:
# #     poco(text=timezone_city[0]).click()
#         poco("android:id/text1").click()
# except poco.exceptions.PocoNoSuchNodeException as e:
#     logging.info('no timezone found'+e)
    
    
# # 返回主界面
# # home()

# # 打开ecovacsHome app
# # start_app('com.eco.global.app')

# # '''
# # =========app端勿扰+预约设置=============
# # 1.不在勿扰时间内的（勿扰时间设置的尽量的小），集中测试完，再测试勿扰时间内（勿扰时间设置尽量的大）
# # 2.注意预约条数的限制，考虑是没测完一条删一条，还是设置teardown
# # 难点：
# # 1.时间都是不好输入，需要滑动
# # '''
# # 点击“+”,唤出下来框
# poco(name='com.eco.global.app:id/right').click()

# # 点击“自动预约”
# poco(name='com.eco.global.app:id/auto_add' , text='预约自动清扫').click()

# # 在当前时间的基础上，下滑来实现1min后的预约
# '''难点在图像定位不行，元素定位中元素resourceID值一样
# 1.选择分钟--（采用绝对定位或元素列表），
# 2.分钟下滑1个--swipe使用函数自定义的“up”
# '''
# poco(name='android.widget.NumberPicker').child(name='android:id/numberpicker_input')[1].swipe('up')

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


# 关闭app
# stop_app('com.eco.global.app')

'''
手机本身操作和app单操作都ok的前提下，有个难点：相互切换
1.进入设置（name :  android.widget.TextView 
	       text :  设置 ）
2.找到时间与日期的设置（由于该项设置不在进入页面的显示范围，
处理方法：1.滑动页面，但是滑动范围不好确定
2. TBD）
'''
timezone_element=poco(text="日期和时间")
def loop_find_timezone():
    while True:
        if timezone_element.exists():
            timezone_element.click()
            break
        else:

# 进入设置
# poco(name='android.widget.TextView',text="设置").click(sleep_interval=5)

# 找到时间与日期的设置
poco(name='com.android.settings:id/title',text='日期和时间').click(sleep_interval=3)

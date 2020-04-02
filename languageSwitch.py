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


'''
脚本测试大前提：
1.主机有图，图有区域A
2.主机的勿扰时间需手动设置，设置范围尽量的大

脚本测试的步骤：
1.手动设置勿扰时间
2.修改系统时区
3.在ecovacsHome上设置预约（自动/区域）
4.检查预约在勿扰时间的响应
5.删除设置的预约
'''
# 0：勿扰关闭/勿扰时间外  2：勿扰时间内
disturb_mode = 0

timezone_element = poco(text="日期和时间")
def loop_find_timezone():
    # 前提：保证程序开始时时处于home界面
    home()
    # 进入设置
    poco(name="设置",text="设置").click(sleep_interval=5)
    # 为进入系统，上滑
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
#         pass
#         不管找没找到列表中的时区，程序都回到主界面
        home()

    
def start_close_app(action):
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
        

def set_schedule_clean(clean_type):
    '''
    确保当前的页面为：更多
    设置预约
    arg:clean_type(obj:str)
        -auto
        -area
    
    '''
    # 点击”工作预约“
    poco(text="工作预约").click()
    sleep(5)
    # 点击“+”,唤出下来框
    poco(name='com.eco.global.app:id/right').click()
    if clean_type == "auto":
        # 点击“自动预约”
        poco(name='com.eco.global.app:id/auto_add' , text='预约自动清扫').click()
    elif clean_type == "area":
         # 点击“区域预约”
        poco(name='com.eco.global.app:id/area_add' , text='预约区域清扫').click()
        # 点击“清扫区域按钮”
        poco(name='com.eco.global.app:id/tv_appoint_area_value',text="未选择").click('center',3)        
        sleep(5)
        # 选中区域A
        touch(Template(r"tpl1585386736702.png", record_pos=(0.274, 0.056), resolution=(576, 1024)))  
        sleep(2)
        #点击返回，回到设置页面
        poco(name='com.eco.global.app:id/back_to').click()
    # 设置预约时间
    poco(name='android.widget.NumberPicker').\
    child(name='android:id/numberpicker_input')[1].swipe([0,-0.2])
    sleep(2)
    # #####保存预约设置##########
    # 在勿扰模式下，提交保存时会有弹框
    pop_message="请避开这一时间段并预留充足时间"
    try:
        poco(text="保存").click(sleep_interval=3)
        if pop_message in poco(name='com.eco.global.app:id/tv_content').get_text():
            # 有弹窗，点击"仍然设定"
            poco(text="仍然设定").click()
            # 修改全局变量disturb_mode，改为在勿扰时间内
            global disturb_mode
            disturb_mode = 1
            sleep(2)
    finally:
        # 无论成功失败，返回更多页面
        poco(name='com.eco.global.app:id/title_back').click()
        if poco(name='com.eco.global.app:id/titleContent').get_text() == "更多":
            log("当前页面：更多")
        return disturb_mode


        
# 删除预约
def teardown_schedule(clean_type):
    '''
    确保当前的页面为：更多
    设置预约
    arg:clean_type(obj:str)
        -auto
        -area
    '''
    clean_text = {'auto':'自动清扫','area':'区域清扫'}
    schdule_item = 'com.eco.global.app:id/tv_appoint_type'
    # 点击”工作预约“
    poco(text="工作预约").click()
    sleep(5)
    try:        
        # 点击自动清扫的title
        poco(name='com.eco.global.app:id/tv_tab_title',text=clean_text[clean_type]).click()
        if poco(name=schdule_item, text=clean_text[clean_type]).exists():
#             左滑，滑出删除按钮
            poco(name=schdule_item, text=clean_text[clean_type]).swipe([-0.5, 0])
            sleep(2)
            if poco(text="删除").exists:
                # 点击删除
                poco(text="删除").click()
                sleep(8)
    
                print(clean_text[clean_type] + " 预约删除成功")
        else:
            print(clean_text[clean_type] + " 没有预约")

    finally:
        # 无论删除成功失败，返回更多页面
        poco(name='com.eco.global.app:id/title_back').click()
        if poco(name='com.eco.global.app:id/titleContent').get_text() == "更多":
            log("当前页面：更多")
        
           
def check_effect_of_schedule(): 
    '''
    检查勿扰下预约是否生效
    returns:
        - popmsg_flag (0：ok  1:没有弱消息)
        - deboot_flag (0：ok  1:主机状态不正确)
    raises:
        - PocoTargetTimeout: when timeout
    确保当前的页面为：更多
    disturb_mode为set_schedule_clean()的返回值
    '''
    popmsg_flag = 0
    deboot_flag = 0
    # 在勿扰时间内
    if disturb_mode:
        # 勿扰的设置使当前时间的2min后，所以在3min内捕获 弱消息
        try:
            Template(r"tpl1585820585953.png", record_pos=(0.008, 0.285), resolution=(720, 1440)).wait_for_appearance(180)
        except PocoTargetTimeout as e:
            popmsg_flag = 1
            log("勿扰时间段内没弹出 预约任务无法执行 的弱消息")
        # 主界面检查勿扰时间内，主机状态为待机
        # 返回主界面
        poco(name='com.eco.global.app:id/title_back').click()
        sleep(3)
        try:
            Template(r"tpl1585821764025.png", record_pos=(0.003, 0.747), resolution=(720, 1440)).wait_for_appearance(5)
        except PocoTargetTimeout as e:
            deboot_flag = 1
            log("勿扰时间段内主机没有保持 待机 状态")
        return popmsg_flag,deboot_flag
    # 勿扰关闭或者在勿扰时间外
    else:
        try:
            Template(r"tpl1585822026085.png", record_pos=(0.01, 0.278), resolution=(720, 1440)).wait_for_appearance(180)
        except PocoTargetTimeout as e:
            popmsg_flag = 1
            log("勿扰时间段外，主机响应预约，没有弹出弱消息")
         try:
            Template(r"tpl1585822379315.png", record_pos=(0.003, 0.753), resolution=(720, 1440)).wait_for_appearance(5)
        except PocoTargetTimeout as e:
            deboot_flag = 1
            log("勿扰时间段外主机没有运行")
        return popmsg_flag,deboot_flag   
            
        
    
    
    
        
# def set_disturb_mode():
#     '''
#     默认app当前所在页面为“更多”主页
#     '''
#     #勿扰模式，默认关闭勿扰0(0:勿扰关闭，1:勿扰时间外，2:勿扰时间内）
#     disturb_mode= [0,1,2]
#     for i in disturb_mode:
#         if disturb_mode=0:
            

            
            
# if __name__ == '__main__':
#     # 循环设置时区
#     for city in timezone_city: 
#         loop_find_timezone()
#         set_timezone(city)
#         sleep(5)
#         home()
#         start_close_app('start')
#         # 进入设备-更多
#         set_schedule_clean(auto)
#         check_schdule(auto)
set_schedule_clean('auto')
set_schedule_clean('area')

teardown_schdule('area')
# check_schedule('auto')

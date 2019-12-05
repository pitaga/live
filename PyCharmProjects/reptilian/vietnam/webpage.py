from selenium import webdriver
import time
import win32api
import win32con


# 键盘操作
def click_keyboard():
    # 模拟键盘操作
    win32api.keybd_event(17, 0, 0, 0)  # 按下ctrl
    win32api.keybd_event(65, 0, 0, 0)  # 按下a
    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放a
    win32api.keybd_event(83, 0, 0, 0)  # 按下s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放s
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放ctrl
    time.sleep(0.8)
    win32api.keybd_event(13, 0, 0, 0)  # 按下enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放enter
    # 预估下载时间，后期根据实际网速调整
    time.sleep(0.8)


# 从文件中读取links
def read_links(path):
    file = open(path, 'r')
    result = file.read().split()
    file.close()
    return result


# 将链接写入文件中
def write_urls(path, news_list):
    file = open(path, 'a+')
    for item in news_list:
        file.write(item + "\n")
    file.close()


# 启动webdriver
def webdriver_start(num, link_list):
    # 打开chrome的另存为mhtml功能
    options = webdriver.ChromeOptions()
    options.add_argument('--save-page-as-mhtml')
    driver = webdriver.Chrome(chrome_options=options)
    # 开始循环
    circle_time = 0
    for link in link_list:
        try:
            driver.get(link)
            click_keyboard()
            circle_time = circle_time + 1
            print("第", num, "轮循环已进行", circle_time, "\t次。")
        except:
            circle_time = circle_time + 1
            print(circle_time, "\t次循环爬取失败。")
    # 关闭webdriver
    driver.quit()
    print("chromedriver已关闭。")
    return link_list



# 主函数
if __name__ == "__main__":
    # 全局变量文件路径
    start_path = "../vietnam/mht_start.txt"
    end_path = "../vietnam/print.txt"

    for times in range(600):
        # 从文件中读取链接
        start_list = read_links(start_path)
        end_list = read_links(end_path)
        start_list = list(set(end_list) - set(start_list))

        # 获取已经保存的网页
        saved_links = webdriver_start(times+1, start_list[:100])

        # 写入已经保存的网页
        write_urls(start_path, saved_links)

        # 输出阶段信息
        print("===================================")
        print("已循环", (times+1) * 100, "次，缓存文件已生成，开始下一次缓存。")
        # select = input("是否继续？(y/n)")
        # if select == 'n':
        #     exit(1)
        print("===================================")

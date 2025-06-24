from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def getHtml(url, timeout=10, headless=True):
    """
    使用Selenium获取网页完整HTML内容
    
    参数:
    url (str): 目标网页URL
    timeout (int): 页面加载超时时间(秒)，默认10秒
    headless (bool): 是否使用无头模式(不显示浏览器窗口)，默认True
    
    返回:
    str: 网页HTML内容字符串
    """
    # 创建Chrome选项
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速
    chrome_options.add_argument("--no-sandbox")   # 禁用沙箱
    chrome_options.add_argument("--disable-dev-shm-usage")  # 防止内存不足崩溃
    
    try:
        # 使用WebDriver Manager自动管理驱动版本(需安装)
        # from webdriver_manager.chrome import ChromeDriverManager
        # service = Service(ChromeDriverManager().install())
        
        # 手动指定驱动路径(如果不用WebDriver Manager)
        service = Service()  # 替换为你的chromedriver路径
        
        # 初始化浏览器实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(timeout)  # 设置页面加载超时
        
        # 访问目标URL
        driver.get(url)
        
        # 显式等待页面加载完成（等待body标签出现）
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(('tag name', 'body')))
        
        # 可选：等待JavaScript执行完成（滚动到页面底部触发懒加载）
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # 短暂等待动态内容加载
        
        # 获取页面HTML源码
        html_content = driver.page_source
        
        # 关闭浏览器
        driver.quit()
        
        return html_content
    
    except Exception as e:
        print(f"获取页面时出错: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return None


def get_url(query):
    url = "https://www.baidu.com/s?wd=" + query
    response = getHtml(url)
    soup = BeautifulSoup(response, 'html.parser')

    li = soup.find_all("div", attrs={"class":"result c-container xpath-log new-pmd"})
    urls = []
    for i in li:
        urls.append(i.attrs['mu'])
    ans = '网站搜寻信息如下：\n'
    for i in urls[:min(len(urls),3)]:
        str = getHtml(i)
        soup = BeautifulSoup(str, 'html.parser')
        ans_list = soup.text.split('\n')
        for txt in ans_list:
            if len(txt) >0:
                ans += txt+'\n'

    return ans

if __name__ == '__main__':
      print(get_url(query='今日天气'))
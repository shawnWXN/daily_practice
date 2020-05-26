chrome浏览器的上网代理服务器插件。
使用方法

from util import create_proxyauth_extension


proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host="10.191.131.12",
    proxy_port=3128,
    proxy_username="F1331479",
    proxy_password="Leon168a"
)
co = webdriver.ChromeOptions()
co.add_extension(proxyauth_plugin_path)

browser = webdriver.Chrome('chromedriver.exe', chrome_options=co)
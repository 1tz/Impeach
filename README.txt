请将此项目放在英文路径下，中文路径会报编码错误。如果非要放到中文路径下，请在main.py中添加以下代码：
reload(sys)
sys.setdefaultencoding('utf-8')

但是不推荐使用该方法，原因见：https://www.v2ex.com/t/254744 以及 https://www.google.com/
search?q=site:v2ex.com/t+setdefaultencoding(%27utf-8%27)
目前没找到更合适的解决方法，Python 2.x版本的缺点
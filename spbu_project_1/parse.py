from bs4 import BeautifulSoup
from urllib.request import urlopen
from parsing import split_txt

def html_parse(url):

    html = urlopen(url).read()

    soup = BeautifulSoup(html, features="html.parser")

    # удаляем все элементы script, style, footer
    # 删除所有脚本，样式，页脚元素
    for script in soup(["script", "style", "footer"]):
        script.extract()

    # получаем текст
    # 获取文字
    text = soup.get_text()



    # разбиваем на строчки и удаляем первый и последний пробелы
    # 分成几行并删除第一个和最后一个空格
    lines = (line.strip() for line in text.splitlines())


    # разбиваем многострочные заголовки построчно
    # 多行标题分解
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # # удаляем пустые строки
    # # 删除空行
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # text = ' '.join(chunk for chunk in chunks if chunk)
    text = split_txt(text)
    
    return text
import json
from pathlib import Path
import logging


try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape


class json_to_html(object): #создаем класс.Его задача-конвертация json в html

    def __init__(self):
        self._init_log()

    def _init_log(self):
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        self.log.addHandler(handler)

    def loader(self):#функция загрузки файла
        path = Path('source.json')#cм.импорт
        data = json.loads(path.read_text(encoding='utf-8'))#ставим флаг на utf
        return data

    def dictionary_to_xml(self, node):
        return "<h1>" + node.get('title')+"</h1><p>"+node.get('body')+"</p>"

    def parse(self, data):
        new_items = []
        for i in data:
            new_items.append(self.dictionary_to_xml(i))
        print(u''.join(new_items))


if __name__ == '__main__':
    example = json_to_html()
    data = example.loader()
    example.parse(data)

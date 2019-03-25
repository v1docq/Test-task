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

    def list_checking(self, data):
        if isinstance(data, list):
            item = self.parse(data)
        else:
            item = self.dictionary_to_xml(data)
        return item

    def dictionary_to_xml(self, node):
        new_tags = []
        for tag, value in node.items():
            if isinstance(value, dict):
                new_tags.append("<"+tag+">" + self.dictionary_to_xml(value) + "</"+tag+">")
            elif isinstance(value, list):
                new_tags.append("<" + tag + ">" + self.parse(value) + "</" + tag + ">")
            else:
                new_tags.append("<" + tag + ">" + value + "</" + tag + ">")
        return u''.join(new_tags)

    def parse(self, data):
        new_items = []
        for i in data:
            new_items.append("<li>" + self.dictionary_to_xml(i) + "<li>")
        return '<ul>' + u''.join(new_items) + '</ul>'

if __name__ == '__main__':
    example = json_to_html()
    data = example.loader()
    print (example.list_checking(data))
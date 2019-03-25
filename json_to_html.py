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
                new_tags.append("<" + self.parse_opening_tag(tag) + ">" + self.dictionary_to_xml(value) + "</" + self.parse_closing_tag(tag) + ">")
            elif isinstance(value, list):
                new_tags.append("<" + self.parse_opening_tag(tag) + ">" + self.parse(value) + "</" + self.parse_closing_tag(tag) + ">")
            else:
                new_tags.append("<" + self.parse_opening_tag(tag) + ">" + self.parse_value(value) + "</" + self.parse_closing_tag(tag) + ">")
        return u''.join(new_tags)

    def parse(self, data):
        new_items = []
        for i in data:
            new_items.append("<li>" + self.dictionary_to_xml(i) + "<li>")
        return '<ul>' + u''.join(new_items) + '</ul>'

    def parse_value(self, value_mark):
        return value_mark.replace('<', '&lt;').replace('>', '&gt;')

    def parse_opening_tag(self, tag_mark):
        result = ''
        id = ''
        classes = []
        isId = False
        isClass = False

        for ch in tag_mark:
            if ch == '#':
                isId = True
                isClass = False
                continue
            if ch == '.':
                isClass = True
                isId = False
                classes.append("")
                continue

            if isId:
                id += ch
            elif isClass:
                classes[-1] += ch
            else:
                result += ch
        return result + ('' if len(classes) == 0 else (' class=\"' + u' '.join(classes) + "\"")) + ('' if id == '' else (" id=\"" + id + "\""))

    def parse_closing_tag(self, tag_mark):
            result = ''
            isId = False
            isClass = False

            for ch in tag_mark:
                if ch == '#':
                    isId = True
                    isClass = False
                    continue
                if ch == '.':
                    isClass = True
                    isId = False
                    continue

                if isId | isClass:
                    continue
                else:
                    result += ch
            return result

if __name__ == '__main__':
    example = json_to_html()
    data = example.loader()
    my_file = open("./stdout", "w")
    my_file.write(example.list_checking(data))
    my_file.close()
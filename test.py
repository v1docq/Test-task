import unittest

from json_to_html import json_to_html


class TestJsonToHtmlConverter(unittest.TestCase):

    def test(self):
        data = {"p.my-class#my-id": "hello", "p.my-class1.my-class2": "example<a>asd</a>"}
        example = json_to_html()
        data = json_to_html.list_checking(data)
        self.assertEqual(data, u'<p id="my-id" class="my-class">hello</p><p class="my-class1 my-class2">example&lt;a&gt;asd&lt;/a&gt;</p>')


if __name__ == '__main__':
    unittest.main()

from pprint import pprint
from tika import parser


class PDFUtils:

    def __init__(self, path, xmlContent=False):
        self.raw = parser.from_file(path, xmlContent=xmlContent)

    def get_content(self):
        return self.raw['content']

    def __str__(self):
        return self.raw['content']


if __name__ == '__main__':
    p = PDFUtils('', True)



from .article import article

class inproceedings(article):
    def __init__(self):
        super().__init__(self)
        self.tipo = 'inproceedings'

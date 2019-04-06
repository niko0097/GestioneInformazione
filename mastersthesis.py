from .phdthesis import phdthesis

class mastersthesis(phdthesis):
    def __init__(self):
        super().__init__(self)
        self.tipo = 'mastersthesis'

from stateless.utils import *

class TexValidate(Validate):
    def __init__(self, exe):
        self.exe = exe

validator = TexValidate('./examples/tex/tex.py')

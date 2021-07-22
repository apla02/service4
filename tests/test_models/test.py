#!/usr/bin/python
from .models.base_class import FileClass

namefile= "validProfile_word.docx"
f = open("./test_examples/validProfile_word.docx", "rb" )
object1 = FileClass(name_file, f)
print(object1)
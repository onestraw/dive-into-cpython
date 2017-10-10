'''
$ python -m dis bytecode.py
$ python -m py_compile bytecode.py  #generate .pyc

 
>>> codeobj = compile('x = 2\nprint "X is", x', 'fakemodule', 'exec')
>>> eval(codeobj)
X is 2

>>> c = compile(open('bytecode.py').read(), '', 'exec')
>>> dir(c)
>>> exec(c)
5


- cpython/Include/opcode.h  #generate bytecode (compiled code)  
- cpython/Lib/dis.py        #mnemonics for bytecode
- cpython/Python/ceval.c    #execute bytecode

Reference
- byteplay: https://wiki.python.org/moin/ByteplayDoc
- cPython Internals: https://goo.gl/ASFmXE
'''


x = 2
y = 3
z = x + y
print z

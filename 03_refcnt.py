>>> import sys
>>> sys.getrefcount('onestraw')
3
>>> x = 'onestraw'
>>> sys.getrefcount('onestraw')
3
>>> y = 'onestraw'
>>> sys.getrefcount('onestraw')
4
>>> z = 'onestraw'
>>> sys.getrefcount('onestraw')
5
>>> 



>>> sys.getrefcount(99)
7
>>> x = range(90, 100)
>>> sys.getrefcount(99)
8
>>> x
[90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
>>> x[-1] = 999
>>> x
[90, 91, 92, 93, 94, 95, 96, 97, 98, 999]
>>> sys.getrefcount(99)
7
>>> 

# def function(a, (b, c)):
#     return a+b+c
#
# function(1, (2,3))
#
#
# # where we have nodes store against a __getitem__ -> we'd like names?
# # more generally the 'Args' thing should know about keys
# # implements Args(*args) first, indexing is after that.
# # Args can be smart: by inspecing the function signature
# #
# # but for __getitem___ all we have is item -> is this ok
# # how does it look in the cache?
#
#
# { 'item' : <item>, v}

'''
what's the right abstraction for __get__ etc.
__getattribute__

default scope case must work just like pythong
so __getitem__(inst, desc) = desc.__get__(inst)
__setitem__(inst, desc, value ) -> desc.__set__(inst, desc, value)

when on graph:

-> can use __getattribute__ to avoid the recursion. is that better?
-> unwrap the __getitem__ behaviour? or keep it.
-> defer to __missing__ for the __getitem__ -> easier.

problem is that __getattribute__ slows us down? (not in C).
make nowd automatic on properties?
how to signal?




'''

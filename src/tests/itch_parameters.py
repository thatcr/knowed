def function(a, (b, c)):
    return a+b+c

function(1, (2,3))


# where we have nodes store against a __getitem__ -> we'd like names?
# more generally the 'Args' thing should know about keys
# implements Args(*args) first, indexing is after that.
# Args can be smart: by inspecing the function signature
#
# but for __getitem___ all we have is item -> is this ok
# how does it look in the cache?


{ 'item' : <item>, v}


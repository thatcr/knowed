

# do we allow graphs to be avaulated in a 'discover' mode:
# i.e. where all values from the cache are not real?
# i.e. we want to price without touching any external system.

# this involves spoof data.

# argument for: let's us discover the graph without evaluation
# but graph is not structurally static
# against: we should always be able to value int he base case (quickliy)
#  and do so before ditribution

#  you can also ahve a node that 'declares' other nodes as it's valuses:

# then we build another node that changes only if deps change.
#  instance pur
class Thing(object):

    # node wrapper will resolve the dependnece on graph underneat th Yellow node,
    # but the Purple node will still be on graph: by registering a different
    #  descriptor type we can then inspect the graph.

    # if we do all nodes in this way, then we know the deps ahead of evaluation.
    # really the dep query (for fslib, or for howard's evaulator) is a special optimization.

    @nowd
    def Yellow(self, fish : float, chips : float) -> float:
        return fish * chips

    @nowd.dependencies
    def Purple(self):
        return {
            'fish' : (market, SomeRate),
            'chips' : (model, SomeParameter)
        }

# in this world: if we want a more optimzed evaulation tree( do we)
# can we 'detect' if thegraph changes on re-evaluation, and keep the
# topological sort in order?
#  or is the on-demand walking of the graph fine.
# is there a neater data structure for the dependencies stuff, better than
#  node -> { dependents }
# what if the depenents list was as list of everything we need to re-eval?
# you could mark a 'fixed' node as one who's deps don't change, unless a purple
# dep changes:
# in which case we lose the child list.


# Args / Index(...) notes:
# vts with arguments or indices need to do some cache lookup to resolve: this is unavoidable.
#  Args ones are read-only, Index ones are not (settable).
#
#  Syntax is
#     sec.MyArgVt(1, 2, 3)
#     sec.MyIdxVt[1,2,3]
#     sec.MyIdvVt[1,2,3] = 'fish'
#
#  under the hood there is an 'Args' type associated with the object, and cached on it, so we resolve
#  1, 2, 3 -> Arg(1,2,3), in sec.__args__, then the node comes from
#     ( sec.__args__[1,2,3], MyArgVt )
#  however the getter is still def MyArgVt(self, 1, 2, 3) on the object
#  Index is the same:
#     ( sec.__keys__[1,2,3], MyIdxVt )
#
#  the unnamed case is the fastest (all that is supported by the idx)
#  however named arguments, and perhaps *args, **kwargs may be supported, but with slower lookups
# mapping into the database:
#   these are stored as sub-objects of the security, they are not separate
#   they should always be named: no unnaed keys, so the idx version will have to
#   have something clever





getitem
indexing
just
a
further
node:

# it's arg caching on the dictionary object
#
# so self.KyedItem returns a dictionary with a wrapper
# wrapper is  regular object hat put's the underlying node values
# on graph, with the dict as the object!)
# then we just use tuple based args indexing on the __getitem__ method
#




















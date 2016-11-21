# implement argument holders for nodes
# they shoudl be specific to the descriptor, so we can optimize the cache lookup
#  hence they live in descriptors?
# does that sit well with the __getatttr__ ting?
# no, needs indirection.
# perhaps __getattribute__ thing is wrong, should always defer to the descriptor.

s
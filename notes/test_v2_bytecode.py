from bytecode import Bytecode, dump_bytecode, Instr, Label, Compare


def my_function(a, b, c=None):
    print(locals())
    if c:
        return c
    return a + b

# what to do:
# invoke with locals - if we have a value return it, otherwise store the cache key, in locals for later.
# process all RETURN_VALUES
# this is actually tricky in python, in C, we can be more direct - but important to store the locals() on entry
# to the function,

def prefix():
    print('hello from prefix')
    return Ellipsis

def postfix(x):
    print('postfix', x)



if __name__ == '__main__':

    def test_it():
        x = prefix()
        if x is Ellipsis:
            return x
        return 123

    import dis
    dis.dis(test_it.__code__)

    bytecode = Bytecode.from_code(my_function.__code__)
    # dump_bytecode(bytecode)



    # requires 3x calls to do this.
    def store_locals():
        __key__ = tuple(locals().items())

    #    can we do this with a finally?

    def generate_bytecodes(bytecode):
        # can we do this, ref the const to our own function?
        return_finally = Label()
        calculate = Label()

        yield Instr("LOAD_CONST", prefix)
        yield Instr('CALL_FUNCTION', 0)
        yield Instr('DUP_TOP')
        yield Instr('LOAD_CONST', Ellipsis) # or some noncached sinlgeton
        yield Instr('COMPARE_OP', Compare.IS)
        yield Instr('POP_JUMP_IF_TRUE', calculate)
        yield Instr('RETURN_VALUE')

        # need to check the reurn value of the call, and return it directly before the finally block is setup
        yield calculate
        yield Instr('SETUP_FINALLY', return_finally)

        for instr in bytecode:
            yield instr

        # return value is now on the top of the stack, so we can cache it in postfix?
        yield return_finally
        yield Instr('DUP_TOP')
        yield Instr('LOAD_CONST', postfix)
        yield Instr('ROT_TWO')
        yield Instr('CALL_FUNCTION', 1)
        yield Instr('END_FINALLY')


    bytecode[:] = list(generate_bytecodes(bytecode))

    dump_bytecode(bytecode)

    my_function.__code__ = bytecode.to_code()
    my_function(1,2,3)



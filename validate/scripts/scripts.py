from utils.utils import hash160
from ecdsa.ecdsa import verify_signture


def op_dup(stack):

    if len(stack) < 1:
        return False
    stack.append(stack[-1])

    return True


def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    h160 = hash160(bytes.fromhex(element)).hex()
    stack.append(h160)
    return True


def op_equal(stack):
    if len(stack) < 2:
        return False

    element1 = stack.pop()
    element2 = stack.pop()

    if element1 == element2:
        stack.append(1)
    else:
        stack.append(0)

    return True


def op_verify(stack):
    if len(stack) < 1:
        False
    element = stack.pop()

    if element == 0:
        return False

    return True


def op_equalverify(stack):
    return op_equal(stack) and op_verify(stack)


def op_checksig(stack, msg):
    if len(stack) < 1:
        return False

    pubkey = stack.pop()
    signature = stack.pop()

    if verify_signture(pubkey, msg, signature):
        stack.append(1)
        return True
    else:
        stack.append(0)
        return False


OP_CODE_FUNCTION = {118: op_dup, 136: op_equalverify, 169: op_hash160, 172: op_checksig}


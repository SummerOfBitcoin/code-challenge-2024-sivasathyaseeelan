from ecdsa.ecdsa import verify_signture
from utils.utils import int_to_little_endian, int_to_compact_size, byte_size_to_little_endian, byte_size, hash256
from validate.msghash.msghash import sighash_preimage_legacy, sighash_preimage_segwit
from validate.scripts.scripts import OP_CODE_FUNCTION


def validate(tx, vin, index, txid, inputs, sequences, outputs):
    scriptpubkey_type = vin["prevout"]["scriptpubkey_type"]

    if(scriptpubkey_type == "p2pkh"):
        
        h160 = vin["prevout"]["scriptpubkey_asm"].split()[3]

        cmds = [0x76, 0xA9, h160, 0x88, 0xAC]

        stack = []

        scriptsig = vin["scriptsig_asm"].split()
        signature = scriptsig[1]
        pubkey = scriptsig[3]

        stack.append(signature)
        stack.append(pubkey)
        
        msg = hash256(bytes.fromhex(sighash_preimage_legacy(tx, bytes.fromhex(signature)[-1]))).hex()

        while len(cmds) > 0:
            cmd = cmds.pop(0)

            if type(cmd) == int:
                operation = OP_CODE_FUNCTION[cmd]

                if cmd == 172:
                    if not operation(stack, msg):
                        return False

                elif not operation(stack):
                    return False
            else:
                stack.append(cmd)
        return True


    
    if(scriptpubkey_type == "v0_p2wpkh"):

        h160 = vin["prevout"]["scriptpubkey_asm"].split()[2]

        cmds = [0x76, 0xA9, h160, 0x88, 0xAC]

        stack = []

        signature = vin["witness"][0]
        pubkey = vin["witness"][1]

        stack.append(signature)
        stack.append(pubkey)

        msg = hash256(bytes.fromhex(sighash_preimage_segwit(tx, bytes.fromhex(signature)[-1], index, txid, inputs, sequences, outputs))).hex()
        
        while len(cmds) > 0:
            cmd = cmds.pop(0)

            if type(cmd) == int:
                operation = OP_CODE_FUNCTION[cmd]

                if cmd == 172:
                    if not operation(stack, msg):
                        return False

                elif not operation(stack):
                    return False
            else:
                stack.append(cmd)
        return True

    return False
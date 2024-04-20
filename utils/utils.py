import hashlib
from hashlib import sha256
from utils.ripemd160.ripemd160 import ripemd160
from math import log
import json

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
WITNESS_RESERVED_VALUE = "0000000000000000000000000000000000000000000000000000000000000000"

def hash256(s):
    """Two rounds of SHA256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hash160(s):
    return ripemd160(sha256(s).digest())


def byte_size(string):
  return len(bytes.fromhex(string))


def byte_size_to_little_endian(byte_string):
  return byte_string[::-1]


def int_to_compact_size(value):
  if value < 0xfd:
    return value.to_bytes(1, 'little')
  elif value <= 0xffff:
    return b'\xfd' + value.to_bytes(2, 'little')
  elif value <= 0xffffffff:
    return b'\xfe' + value.to_bytes(4, 'little')
  else:
    return b'\xff' + value.to_bytes(8, 'little')


def int_to_little_endian(input_integer, length):
  """Int_to_little_endian takes an interger and return the little-endian byte sequence of length"""
  return input_integer.to_bytes(length, byteorder='little')


def gen_pre_hash_raw_tx(tx):
  pre_hash_raw_data = ""
  pre_hash_raw_data += int_to_little_endian(tx["version"], 4).hex()
  pre_hash_raw_data += int_to_compact_size(len(tx["vin"])).hex()
  for vin in tx["vin"]:
    pre_hash_raw_data += byte_size_to_little_endian(bytes.fromhex(vin["txid"])).hex() + int_to_little_endian(vin["vout"], 4).hex() + int_to_compact_size(byte_size(vin["scriptsig"])).hex() + vin["scriptsig"] + int_to_little_endian(vin["sequence"], 4).hex()
  pre_hash_raw_data += int_to_compact_size(len(tx["vout"])).hex()
  for vout in tx["vout"]:
    pre_hash_raw_data += int_to_little_endian(vout["value"], 8).hex() + int_to_compact_size(byte_size(vout["scriptpubkey"])).hex() + vout["scriptpubkey"]
  pre_hash_raw_data += int_to_little_endian(tx["locktime"], 4).hex()
  return pre_hash_raw_data


def gen_pre_hash_raw_wtx(tx):
  if not is_segwit(tx):
     return gen_pre_hash_raw_tx(tx)
  pre_hash_raw_data = ""
  pre_hash_raw_data += int_to_little_endian(tx["version"], 4).hex()
  pre_hash_raw_data += "0001"
  pre_hash_raw_data += int_to_compact_size(len(tx["vin"])).hex()
  for vin in tx["vin"]:
    pre_hash_raw_data += byte_size_to_little_endian(bytes.fromhex(vin["txid"])).hex() + int_to_little_endian(vin["vout"], 4).hex() + int_to_compact_size(byte_size(vin["scriptsig"])).hex() + vin["scriptsig"] + int_to_little_endian(vin["sequence"], 4).hex()
  pre_hash_raw_data += int_to_compact_size(len(tx["vout"])).hex()
  for vout in tx["vout"]:
    pre_hash_raw_data += int_to_little_endian(vout["value"], 8).hex() + int_to_compact_size(byte_size(vout["scriptpubkey"])).hex() + vout["scriptpubkey"]
  for vin in tx["vin"]:
      if "witness" in vin:
        length = len(vin["witness"])
      else:
        length = 0
      pre_hash_raw_data += int_to_compact_size(length).hex()
      if length != 0:
        for wit_item in vin["witness"]:
          pre_hash_raw_data += int_to_compact_size(byte_size(wit_item)).hex() + wit_item
  pre_hash_raw_data += int_to_little_endian(tx["locktime"], 4).hex()
  return pre_hash_raw_data


def is_segwit(tx):
  for vin in tx["vin"]:
    if "witness" in vin:
      return True
  return False


def gen_size_of_pre_hash_raw_tx(tx):
  return byte_size(gen_pre_hash_raw_tx(tx))


def gen_size_of_additional_segwit_tx(tx):
  witness_block = ""
  if(is_segwit(tx)):
    for vin in tx["vin"]:
      if "witness" in vin:
        length = len(vin["witness"])
      else:
        length = 0
      witness_block += int_to_compact_size(length).hex()
      if length != 0:
        for wit_item in vin["witness"]:
          witness_block += int_to_compact_size(byte_size(wit_item)).hex() + wit_item
    return byte_size(witness_block) + 2
  return 0


tx = "020000000125c9f7c56ab4b9c358cb159175de542b41c7d38bf862a045fa5da51979e37ffb010000006b4830450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd012102c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667dffffffff0254e80500000000001976a9141ef7874d338d24ecf6577e6eadeeee6cd579c67188acc8910000000000001976a9142e391b6c47778d35586b1f4154cbc6b06dc9840c88ac00000000"
binary_data = bytes.fromhex(tx)
byte_string = hash256(binary_data)

#print(byte_size_to_little_endian(byte_string).hex())


# Input integer
input_integer = 330

# Convert integer to little-endian hexadecimal string with 4 bytes
hex_string = int_to_little_endian(input_integer, 8)

#print(hex_string.hex())

#print(hex(byte_size("3044022035345342616cb5d6eefbbffc1de179ee514587dd15efe5ca892602f50336e30502207864061776e39992f317aee92dcc9595cc754b8f13957441d5ccd9ebd1b5cc0c01"))[2:])



# Example usage
integer_value = byte_size("473044022100a7e3beccc1ba05981d5d02b9a387fca7dd352e26249b6b98601b90b641c93b1d021f72ace36567e8eeb09ffedda0708efe61a6d29cc928d6dca4cd7ec2540d3025012102e57d639eb8ad9feeda51d951c33feed17c2ad7946c3a7223513fb912a5b2363b")

compact_size_bytes = int_to_compact_size(integer_value)
#print(compact_size_bytes.hex())

json_tx = '''
{
  "txid": "0a930f20c108af089e864f6290a3c9b8db6dab092b3a77583b34bb4ff4b35c1e",
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "fde72ccf63b4320bbd96a4b3fd958bdfe5ee5209bef80e95685e78050a889b08",
      "vout": 9,
      "prevout": {
        "scriptpubkey": "512068a6b4092dd7f4ead75ed8a772d41b824919ceb000896346e57f5feeda935672",
        "scriptpubkey_asm": "OP_PUSHNUM_1 OP_PUSHBYTES_32 68a6b4092dd7f4ead75ed8a772d41b824919ceb000896346e57f5feeda935672",
        "scriptpubkey_type": "v1_p2tr",
        "scriptpubkey_address": "bc1pdzntgzfd6l6w4467mznh94qmsfy3nn4sqzykx3h90a07ak5n2eeq7pae58",
        "value": 1711
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "02",
        "750063036f726401010a746578742f706c61696e00367b2270223a226272632d3230222c226f70223a226d696e74222c227469636b223a2261616161222c22616d74223a223130303030227d6851",
        "c1782891272861d4104f524ac31855e20aa1bdb507ac4a6619c030768496b90e84"
      ],
      "is_coinbase": false,
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "scriptpubkey": "0014a40897ac0756778584e7dbe457cca54abc6daf4c",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 a40897ac0756778584e7dbe457cca54abc6daf4c",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1q5syf0tq82emctp88m0j90n99f27xmt6v2f79lx",
      "value": 294
    }
  ],
  "size": 200,
  "weight": 446,
  "fee": 1417,
  "status": {
    "confirmed": true,
    "block_height": 834460,
    "block_hash": "00000000000000000000484a79b643b2524bbce82e5d8a442013fa5b8905ed98",
    "block_time": 1710307468
  },
  "hex": "02000000000101089b880a05785e68950ef8be0952eee5df8b95fdb3a496bd0b32b463cf2ce7fd0900000000ffffffff012601000000000000160014a40897ac0756778584e7dbe457cca54abc6daf4c0301024e750063036f726401010a746578742f706c61696e00367b2270223a226272632d3230222c226f70223a226d696e74222c227469636b223a2261616161222c22616d74223a223130303030227d685121c1782891272861d4104f524ac31855e20aa1bdb507ac4a6619c030768496b90e8400000000"
}
'''

# print(gen_pre_hash_raw_wtx(json.loads(json_tx)))

def gen_tx_id(tx):
    pre_hash_raw_tx = gen_pre_hash_raw_tx(tx)
    binary_data = bytes.fromhex(pre_hash_raw_tx)
    byte_string = hash256(binary_data)

    return byte_size_to_little_endian(byte_string).hex()

#print(gen_tx_id(json.loads(json_tx)))

#print(gen_size_of_pre_hash_raw_tx(json.loads(json_tx)) + gen_size_of_additional_segwit_tx(json.loads(json_tx)))



def little_endian_to_int(b):
    """takes a byte sequence and returns an integer"""
    return int.from_bytes(b, "little")

def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1


def decode_base58(s):
    num = 0

    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder="big")
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f"bad Address {checksum} {hash256(combined[:-4][:4])}")

    return combined[1:-4]


def encode_varint(i):
    """encodes an integer as a varint"""
    if i < 0xFD:
        return bytes([i])
    elif i < 0x10000:
        return b"\xfd" + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b"\xfe" + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b"\xff" + int_to_little_endian(i, 8)
    else:
        raise ValueError("integer too large: {}".format(i))


def hash256_hex(input):
    h1 = hashlib.sha256(bytes.fromhex(input)).digest()
    return hashlib.sha256(h1).hexdigest()

def generateMerkleRoot(txids):
    if len(txids) == 0:
        return None

    # Reverse the txids
    level = [bytes.fromhex(txid)[::-1].hex() for txid in txids]

    while len(level) > 1:
        next_level = []

        for i in range(0, len(level), 2):
            pair_hash = None
            if i + 1 == len(level):
                # In case of an odd number of elements, duplicate the last one
                pair_hash = hash256_hex(level[i] + level[i])
            else:
                pair_hash = hash256_hex(level[i] + level[i + 1])
            next_level.append(pair_hash)

        level = next_level

    return level[0]


def target_to_bits(target):
    """Turns a target integer back into bits"""
    raw_bytes = target.to_bytes(32, "big")
    raw_bytes = raw_bytes.lstrip(b"\x00")  # <1>
    if raw_bytes[0] > 0x7F:  # <2>
        exponent = len(raw_bytes) + 1
        coefficient = b"\x00" + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)  # <3>
        coefficient = raw_bytes[:3]  # <4>
    new_bits = coefficient[::-1] + bytes([exponent])  # <5>
    return new_bits


def calculateWitnessCommitment(wtxids):
   witnessRoot = generateMerkleRoot(wtxids)
   witnessReservedValue = WITNESS_RESERVED_VALUE
   return hash256(bytes.fromhex(witnessRoot + witnessReservedValue))

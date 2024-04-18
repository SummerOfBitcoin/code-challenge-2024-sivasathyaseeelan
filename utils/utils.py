import hashlib
from hashlib import sha256
from Crypto.Hash import RIPEMD160
from math import log
import json

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def hash256(s):
    """Two rounds of SHA256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()


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
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "91841aff383692268b6e6e8dd4db468b193980f06a11a674593ced444c5f092b",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "5120175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
        "scriptpubkey_asm": "OP_PUSHNUM_1 OP_PUSHBYTES_32 175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
        "scriptpubkey_type": "v1_p2tr",
        "scriptpubkey_address": "bc1pzaw4zhp42aurftgx387rezzx9qalgvgt0h9uvtayzzy7ef77cq5s69sjt9",
        "value": 92137
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "7a4368c89eca7fec24a5e427781894ed734ca65930f2765e8ae3e9098ab62e42efbe8a227b149fb51bdc7052233b5af6dde7614d6bf83932b59e54bad76ab89d"
      ],
      "is_coinbase": false,
      "sequence": 4294967293
    },
    {
      "txid": "22f443847db662d39d023dea545e115840c307160df0ea19df41cdb39f11c428",
      "vout": 0,
      "prevout": {
        "scriptpubkey": "5120175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
        "scriptpubkey_asm": "OP_PUSHNUM_1 OP_PUSHBYTES_32 175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
        "scriptpubkey_type": "v1_p2tr",
        "scriptpubkey_address": "bc1pzaw4zhp42aurftgx387rezzx9qalgvgt0h9uvtayzzy7ef77cq5s69sjt9",
        "value": 65919
      },
      "scriptsig": "",
      "scriptsig_asm": "",
      "witness": [
        "4dffde1251cd90f4afd0dd614b7622642fb598876a080bcfd89d9d51af955ae09a1ab95e14435a3d708a83ecc3e5db04366d67cd4d7e9c1904d4fbbf4f72df13"
      ],
      "is_coinbase": false,
      "sequence": 4294967293
    }
  ],
  "vout": [
    {
      "scriptpubkey": "00145f35a124069683ddeb2f1726e9a1173f9340c87e",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 5f35a124069683ddeb2f1726e9a1173f9340c87e",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1qtu66zfqxj6pam6e0zunwnggh87f5pjr7vdr5cd",
      "value": 100000
    },
    {
      "scriptpubkey": "0014fb7a185fc47428a9992c09f70c6add47a5c19223",
      "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 fb7a185fc47428a9992c09f70c6add47a5c19223",
      "scriptpubkey_type": "v0_p2wpkh",
      "scriptpubkey_address": "bc1qldapsh7yws52nxfvp8msc6kag7jury3rxrw4dm",
      "value": 30000
    },
    {
      "scriptpubkey": "5120175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
      "scriptpubkey_asm": "OP_PUSHNUM_1 OP_PUSHBYTES_32 175d515c35577834ad0689fc3c8846283bf4310b7dcbc62fa41089eca7dec029",
      "scriptpubkey_type": "v1_p2tr",
      "scriptpubkey_address": "bc1pzaw4zhp42aurftgx387rezzx9qalgvgt0h9uvtayzzy7ef77cq5s69sjt9",
      "value": 22622
    }
  ]
}
'''

#print(gen_pre_hash_raw_tx(json.loads(json_tx)))

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


def merkle_parent_level(hashes):
    """takes a list of binary hashes and returns a list that's half of the length"""

    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])

    parent_level = []

    for i in range(0, len(hashes), 2):
        parent = hash256(bytes.fromhex(hashes[i]) + bytes.fromhex(hashes[i + 1])).hex()
        parent_level.append(parent)
    return parent_level


def merkle_root(hashes):
    """Takes a list of binary hashes and return the merkle root"""
    current_level = hashes

    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)

    return current_level[0]


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

from utils.utils import int_to_little_endian, int_to_compact_size, byte_size_to_little_endian, byte_size, hash256
from hashlib import sha256
import json
import binascii

def sighash_preimage_legacy(tx, flag):
    preimage = ""
    preimage += int_to_little_endian(tx["version"], 4).hex()
    preimage += int_to_compact_size(len(tx["vin"])).hex()
    for vin in tx["vin"]:
        preimage += byte_size_to_little_endian(bytes.fromhex(vin["txid"])).hex() + int_to_little_endian(vin["vout"], 4).hex() + int_to_compact_size(byte_size(vin["prevout"]["scriptpubkey"])).hex() + vin["prevout"]["scriptpubkey"] + int_to_little_endian(vin["sequence"], 4).hex()
        preimage += int_to_compact_size(len(tx["vout"])).hex()
    for vout in tx["vout"]:
        preimage += int_to_little_endian(vout["value"], 8).hex() + int_to_compact_size(byte_size(vout["scriptpubkey"])).hex() + vout["scriptpubkey"]
    preimage += int_to_little_endian(tx["locktime"], 4).hex()
    preimage += int_to_little_endian(flag, 4).hex()

    return preimage


def sighash_preimage_segwit(tx, flag, index, txid, inputs, sequences, outputs):
    preimage = ""
    preimage += int_to_little_endian(tx["version"], 4).hex()
    if txid not in inputs:
        inputs[txid] = ""
        for vin in tx["vin"]:
            inputs[txid] += byte_size_to_little_endian(bytes.fromhex(vin["txid"])).hex() + int_to_little_endian(vin["vout"], 4).hex()
    preimage += hash256(bytes.fromhex(inputs[txid])).hex()
    if txid not in sequences:
        sequences[txid] = ""
        for vin in tx["vin"]:
            sequences[txid] += int_to_little_endian(vin["sequence"], 4).hex()
    preimage += hash256(bytes.fromhex(sequences[txid])).hex()
    for i, vin in enumerate(tx["vin"]):
        if i == index:
          preimage += byte_size_to_little_endian(bytes.fromhex(vin["txid"])).hex() + int_to_little_endian(vin["vout"], 4).hex()
          preimage += f"1976a914{vin['prevout']['scriptpubkey'][4::]}88ac"
          preimage += int_to_little_endian(vin["prevout"]["value"], 8).hex()
          preimage += int_to_little_endian(vin["sequence"], 4).hex()
    if txid not in outputs:
        outputs[txid] = ""
        for vout in tx["vout"]:
            outputs[txid] += int_to_little_endian(vout["value"], 8).hex() + int_to_compact_size(byte_size(vout["scriptpubkey"])).hex() + vout["scriptpubkey"]
    preimage += hash256(bytes.fromhex(outputs[txid])).hex()
    preimage += int_to_little_endian(tx["locktime"], 4).hex()
    preimage += int_to_little_endian(flag, 4).hex()

    return preimage
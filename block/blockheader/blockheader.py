from utils.utils import (
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    int_to_little_endian,
    byte_size_to_little_endian
)


class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.blockHash = ""
        self.serialize = ""

    def mine(self, target):
        lower = target + 1

        while lower > target:
            hash_in = ""
            hash_in += int_to_little_endian(self.version, 4).hex()
            hash_in += bytes.fromhex(self.prevBlockHash)[::-1].hex()
            hash_in += bytes.fromhex(self.merkleRoot)[::-1].hex()
            hash_in += int_to_little_endian(self.timestamp, 4).hex()
            hash_in += self.bits[::-1].hex()
            hash_in += int_to_little_endian(self.nonce, 4).hex()

            self.blockHash = hash256(bytes.fromhex(hash_in))[::-1].hex()

            lower = int(self.blockHash, 16)           
             
            self.nonce += 1
            print(f"Mining Started {self.nonce}", end="\r")
        self.serialize = hash_in
        self.bits = self.bits[::-1].hex()

    def to_dict(self):
        return {
            "version": self.version,
            "prevBlockHash": self.prevBlockHash,
            "merkleRoot": self.merkleRoot,
            "timestamp": self.timestamp,
            "bits": self.bits,
            "nonce": self.nonce,
            "blockHash": self.blockHash
        }
    
    def Serialize(self):
        return self.serialize
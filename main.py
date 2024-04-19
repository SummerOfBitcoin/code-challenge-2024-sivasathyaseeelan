import os
import json
import time
import utils.utils
from validate.validate import validate
from block.blockheader.blockheader import BlockHeader
from block.tx.tx import CoinbaseTx
import algorithms.knapsack

# Specify the directory containing the JSON files
directory_path = './mempool'

mempool = []

inputs = {}
sequences = {}
outputs = {}

MAX_WEIGHT = 4000000

ZERO_HASH = "0" * 64
VERSION = 4
INITIAL_TARGET = 0x0000ffff00000000000000000000000000000000000000000000000000000000                


def addBlock(BlockHeight, prevBlockHash):
    current_target = INITIAL_TARGET
    bits = utils.utils.target_to_bits(INITIAL_TARGET)
    timestamp = int(time.time())

    coinbaseInstance = CoinbaseTx(BlockHeight)
    coinbaseTx = coinbaseInstance.CoinbaseTransaction()
    coinbase_wt = 4*len(coinbaseTx.serialize())
    left_weight ,total_fee, selected_entries = algorithms.knapsack.knapsack_greedy(mempool, MAX_WEIGHT - 320 - coinbase_wt)
    coinbaseTx.tx_outs[0].amount = coinbaseTx.tx_outs[0].amount + total_fee
    coinbase_serialize =  coinbaseTx.serialize().hex()

    selected_entries.insert(0, utils.utils.hash256(coinbaseTx.serialize()).hex())

    merkleRoot_input = selected_entries
    merkleRoot = utils.utils.generateMerkleRoot(merkleRoot_input)

    blockheader = BlockHeader(
        VERSION, prevBlockHash, merkleRoot, timestamp, bits
    )
    blockheader.mine(current_target)
    blockheader_serialize = blockheader.Serialize()

    with open("./output.txt", 'w') as file:
        file.write(blockheader_serialize + '\n')
        file.write(coinbase_serialize + '\n')
        # file.write('[' + '\n')
        for entry in selected_entries:
            file.write(entry + '\n')
        # file.write(']' + '\n')

    return left_weight ,total_fee
    


def isvalid_tx(tx, txid):
    for i, vin in enumerate(tx["vin"]):
        if not validate(tx, vin, i, txid, inputs, sequences, outputs):
            return False
    return True


def gen_tx_id(tx):
    pre_hash_raw_tx = utils.utils.gen_pre_hash_raw_tx(tx)
    binary_data = bytes.fromhex(pre_hash_raw_tx)
    byte_string = utils.utils.hash256(binary_data)

    return utils.utils.byte_size_to_little_endian(byte_string).hex()


def calculate_tx_fee(tx):
    fee = 0
    vins = tx["vin"]
    for vin in vins:
        fee += vin["prevout"]["value"]
    vouts = tx["vout"]
    for vout in vouts:
        fee -= vout["value"]
    return fee


def calculate_tx_weight(tx):
    return 4*utils.utils.gen_size_of_pre_hash_raw_tx(tx) + utils.utils.gen_size_of_additional_segwit_tx(tx)


def mempool_entry(tx):
    tx_id = gen_tx_id(tx)
    fee = calculate_tx_fee(tx)
    weight = calculate_tx_weight(tx)

    return (tx_id, fee, weight)


def read_txs(directory):
    # Check if the provided directory exists
    if not os.path.isdir(directory):
        print("Directory does not exist.")
        return
    
    valid_tx = 0
    invalid_tx = 0
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
                tx = json.load(file)
                entry = mempool_entry(tx)
                if isvalid_tx(tx, entry[0]):
                    mempool.append(mempool_entry(tx))
                    valid_tx = valid_tx + 1
                    print(f"{entry[0]} is Verified")
                else:
                    invalid_tx = invalid_tx + 1
                    print(f"{entry[0]} is Unverified")

    return valid_tx
    


if __name__ == "__main__":

    start_time = time.time()

    # Call the function to read JSON files
    valid_tx = read_txs(directory_path)
    print(len(mempool))


    left_wt, total_fee = addBlock(0, ZERO_HASH)


    print("Total verified txs:", valid_tx)
    print("Weight and Total fee:", MAX_WEIGHT - left_wt, total_fee)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")



# SOLUTION

## Block Formation from Mempool Transactions

This Python script(`main.py`) is designed to create a block of transactions from a mempool of transactions stored in JSON files. It utilizes various modules and algorithms to construct a valid block according to the rules of a blockchain network.

## Overview

The script performs the following main tasks:

1. **Reading Mempool Transactions**: It reads JSON files containing transaction data from a specified directory (`./mempool` by default). Each transaction is validated to ensure its correctness and integrity.

2. **Transaction Validation**: Transactions(P2PKH and P2WPKH) are validated to ensure that each input is legitimate and authorized, preventing double-spending and other malicious activities.

3. **Block Construction**: After validating the transactions, the script constructs a new block containing a selected set of transactions from the mempool. It utilizes a knapsack algorithm to optimize the selection of transactions based on their fees and weights.

4. **Block Header Generation**: The block header is constructed with necessary information such as the previous block hash, Merkle root of transactions, timestamp, and mining difficulty.

5. **Mining**: The block is mined by finding a nonce that satisfies the target difficulty, ensuring the block is valid according to the network's consensus rules.

6. **Output**: The resulting block header, coinbase transaction, and selected transactions are written to an output file (`output.txt`).

## Dependencies

The script requires the following dependencies:

- `utils`: Custom utilities for hash calculations, Merkle tree generation, and other blockchain-related functions.
- `validate`: Module for transaction validation.
- `blockheader`: Module for constructing and serializing block headers.
- `tx`: Module for creating coinbase transactions.
- `knapsack`: Algorithm module for optimizing transaction selection based on fees and weights.

## Usage

1. **Prepare Mempool Transactions**: Ensure that the mempool directory contains valid JSON files, each representing a transaction.

2. **Execute the Script**: Run the script using Python (`python3 main.py`). Ensure that the script file (`main.py`) is in the same directory as the mempool directory.

3. **Output**: After execution, the script will generate an output file (`output.txt`) containing the block header, coinbase transaction, and selected transactions.

## Configuration

- `directory_path`: Path to the directory containing mempool JSON files.
- `MAX_WEIGHT`: Maximum weight limit for transactions in the block.
- `ZERO_HASH`: Initial hash value for the first block.
- `VERSION`: Version number of the block.
- `INITIAL_TARGET`: Initial target difficulty for mining.
- `WTXID_COINBASE`: Witness transaction ID for the coinbase transaction.

def knapsack(mempool, block_size_limit):
    n = len(mempool)
    dp = [[0] * (block_size_limit + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, block_size_limit + 1):
            if mempool[i - 1][2] <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - mempool[i - 1][2]] + mempool[i - 1][1])
            else:
                dp[i][j] = dp[i - 1][j]

    selected_transactions = []
    i, j = n, block_size_limit
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_transactions.append(mempool[i - 1])
            j -= mempool[i - 1][2]
        i -= 1

    return selected_transactions[::-1], dp[n][block_size_limit]


def fractional_knapsack(entries, total_weight):
    # Sort entries by their value per unit weight in descending order
    entries.sort(key=lambda x: x[1] / x[2], reverse=True)

    total_fee = 0
    selected_entries = []

    for entry in entries:
        id_, fee, weight = entry
        if total_weight >= weight:
            total_fee += fee
            selected_entries.append(entry)
            total_weight -= weight
        else:
            continue

    return total_fee, selected_entries

def knapsack_greedy(entries, total_weight):
    # Sort entries by their fee in descending order
    entries.sort(key=lambda x: x[1] / x[2], reverse=True)

    total_fee = 0
    selected_entries = []

    for entry in entries:
        id_, fee, weight = entry
        if total_weight >= weight:
            total_fee += fee
            selected_entries.append(id_)
            total_weight -= weight

    return total_weight ,total_fee, selected_entries

def select_transactions(mempool, block_size_limit):
    sorted_transactions = sorted(mempool, key=lambda x: x[1], reverse=True)
    selected_transactions = []
    current_block_size = 0
    max_fee = 0

    for tx in sorted_transactions:
        if current_block_size + tx[2] <= block_size_limit:
            selected_transactions.append(tx)
            max_fee += tx[1]
            current_block_size += tx[2]

    return block_size_limit - current_block_size ,max_fee, selected_transactions

if __name__ == "__main__":
    # Example list of entries
    entries = [
        ("Item 1", 60, 10),
        ("Item 2", 100, 20),
        ("Item 3", 120, 30),
        ("Item 4", 20, 5),
        ("Item 5", 50, 15),
        ("Item 6", 80, 25)
        # Add more entries here if needed
    ]

    total_weight = 4000000

    selected_entries, max_fee = knapsack(entries, total_weight)
    print("Maximum fee that can be collected:", max_fee)
    print("Selected entries:")
    for entry in selected_entries:
        print(entry)

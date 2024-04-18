# Compressed public key
compressed_public_key = "02c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d"
uncompressed_public_key = "04c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d43eb535ed8a7235ee588c94fe285f0ba962b603fc21a9bb0143d31251b6aa3b8"




def pubkey_to_point(pubkey):
    # Extract prefix 
    prefix = pubkey[:2]
    
    if prefix == "04":
        # Extract x and y coordinates
        x_hex = pubkey[2:66]
        y_hex = pubkey[66:]

        # Convert x and y coordinates from hexadecimal to integers
        x = int(x_hex, 16)
        y = int(y_hex, 16)

        return (x, y)
    
    #Extract x coordinate
    x_hex = pubkey[2:]

    # Convert x coordinate from hexadecimal to integer
    x = int(x_hex, 16)

    # Elliptic curve parameters
    a = 0
    b = 7
    p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    # Calculate y coordinate based on the prefix
    if prefix == "02":
        # If prefix is "02", y is even
        y_square = (x ** 3 + a * x + b) % p
        y = pow(y_square, (p + 1) // 4, p)  # Square root modulo p
        if y % 2 == 1:  # If y is odd, use the other root
            y = p - y
    else:
        # If prefix is "03", y is odd
        y_square = (x ** 3 + a * x + b) % p
        y = pow(y_square, (p + 1) // 4, p)  # Square root modulo p
        if y % 2 == 0:  # If y is even, use the other root
            y = p - y
    return (x, y)




# Print x and y coordinates
#print(pubkey_to_point(uncompressed_public_key))
#print(pubkey_to_point(compressed_public_key))
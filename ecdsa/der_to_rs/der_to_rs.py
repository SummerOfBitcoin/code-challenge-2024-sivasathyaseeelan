# import asn1
# import binascii

# def der_to_rs(der_signature):
#     # Parse DER signature
#     decoder = asn1.Decoder()
#     decoder.start(binascii.unhexlify(der_signature))

#     # Read SEQUENCE
#     decoder.enter()

#     # Read r
#     _, r = decoder.read()

#     # Read s
#     _, s = decoder.read()

#     # Return r and s as hex strings
#     return (r, s)

# DER encoded signature
der_signature = '30450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd01'

def der_to_rs(der_signature):
    len_r = 2*int(der_signature[6:8], 16)
    r = int(der_signature[8: 8 + len_r], 16)

    len_s = 2*int(der_signature[2 + 8 + len_r: 8 + len_r + 2 + 2], 16)
    s = int(der_signature[8 + len_r + 2 + 2: 8 + len_r + 2 + 2 + len_s], 16)
    return (r, s)

        
der_to_rs(der_signature)
#print("r:", r)
#print("s:", s)

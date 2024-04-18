import asn1
import binascii
from pem import class_id_to_string,tag_id_to_string,value_to_string
import sys
import base64


der='30450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd'
# See https://asecuritysite.com/encryption/sigs2


indent=0

if (len(sys.argv)>1):
  der=str(sys.argv[1])

def make_pem(st):
  bff="-----BEGIN PUBLIC KEY-----\n"
  bff=bff+base64.b64encode(st).decode()+"\n"
  bff=bff+"-----END PUBLIC KEY-----\n"
  print (bff)

def read_pem(data):
    """Read PEM formatted input."""
    data = data.replace("\n","")
    data = data.replace("","")
    data = data.replace("-----BEGIN PUBLIC KEY-----","")
    data = data.replace("-----END PUBLIC KEY-----","")
    return binascii.hexlify(base64.b64decode(data))

def show_asn1(string, indent=0):

    while not string.eof():
        tag = string.peek()
        if tag.typ == asn1.Types.Primitive:
            tag, value = string.read()
            print(' ' * indent,end='')
            print('[{}] {}: {}'.format(class_id_to_string(tag.cls), tag_id_to_string(tag.nr),value_to_string(tag.nr, value)))

            if (tag.nr==4): 
              private_key=binascii.hexlify(value)
              print(' ' * indent,end='')
              print("Private key: ",private_key.decode())

            if (tag.nr==3):
              
              res=binascii.hexlify(value).decode()
              length=len(res)
              if (res.__contains__('10001')):  # RSA
                
                rtn=res[1:].find("02")
                print (res[rtn+3:rtn+5])
                byte = int(res[rtn+3:rtn+5],16)-1

                rtn=res[1:].find("00")
                N=res[rtn+3:rtn+3+(byte)*2]
                e=res[length-5:]
                print(' ' * indent,end='')
                print(f"RSA Modulus ({len(N)*4}) bits: {N}")
                print(f"RSA e: {e}")
              else :  # ECC
                public_key_x=res[4:length//2]
                public_key_y=res[length//2:]
                print(' ' * indent,end='')
                print(f"Public key ({public_key_x}, {public_key_y})")

        elif tag.typ == asn1.Types.Constructed:
            print(' ' * indent,end='')
            print('[{}] {}'.format(class_id_to_string(tag.cls), tag_id_to_string(tag.nr)))
            string.enter()
            show_asn1(string, indent + 2)
            string.leave()

Print=True
if (len(der)>500): Print=False

if (der.__contains__("BEGIN")):
  print("Found PEM")
  der=read_pem(der)


if (Print): print (f"PEM: {der}\n")


st=binascii.unhexlify(der)
decoder = asn1.Decoder()
decoder.start(st)
show_asn1(decoder)
print()

if (Print): make_pem(st)

import base64
import asn1
import binascii

def read_pem(data):
    """Read PEM formatted input."""
    data = data.replace("-----BEGIN PUBLIC KEY-----","")
    data = data.replace("-----END PUBLIC KEY-----","")
    data = data.replace("\n","")
    data = data.replace("","")
    return binascii.hexlify(base64.b64decode(data))

tag_id_to_string_map = {
    asn1.Numbers.Boolean: "BOOLEAN",
    asn1.Numbers.Integer: "INTEGER (02)",
    asn1.Numbers.BitString: "BIT STRING",
    asn1.Numbers.OctetString: "OCTET STRING",
    asn1.Numbers.Null: "NULL",
    asn1.Numbers.ObjectIdentifier: "OBJECT (06)",
    asn1.Numbers.PrintableString: "PRINTABLESTRING",
    asn1.Numbers.IA5String: "IA5STRING",
    asn1.Numbers.UTCTime: "UTCTIME",
    asn1.Numbers.Enumerated: "ENUMERATED",
    asn1.Numbers.Sequence: "SEQUENCE (30)",
    asn1.Numbers.Set: "SET"
}

class_id_to_string_map = {
    asn1.Classes.Universal: "U",
    asn1.Classes.Application: "A",
    asn1.Classes.Context: "C",
    asn1.Classes.Private: "P"
}

object_id_to_string_map = {
    "1.2.840.113549.1.1.1": "RSA Encryption",
    "1.2.840.10040.4.1": "DSA",
    "1.2.840.10046.2.1": "Diffie-Hellman",  	
	  "1.2.840.10045.2.1": "ECC",  
	  "1.2.840.10045.3.1.1": "secp192r1",  
	  "1.3.132.0.33": "secp224r1",        	 
	  "1.2.840.10045.3.1.7": "secp256r1",  
	  "1.3.132.0.34": "secp384r1",  
	  "1.3.132.0.35": "secp521r1",  
	  "1.3.36.3.3.2.8.1.1.1": "brainpoolP160r1",       	 
	  "1.3.36.3.3.2.8.1.1.3": "brainpoolP192r1",  
	  "1.3.36.3.3.2.8.1.1.5": "brainpoolP224r1",  
	  "1.3.36.3.3.2.8.1.1.7": "brainpoolP256r1",  
	  "1.3.36.3.3.2.8.1.1.9": "brainpoolP320r1",  
	  "1.3.36.3.3.2.8.1.1.11": "brainpoolP384r1",

	  "1.3.101.112": "Ed25519",  
	  "1.3.101.113": "Ed448",  
 

    "1.3.6.1.5.5.7.1.1": "authorityInfoAccess",

    "2.5.4.3": "commonName",
    "2.5.4.4": "surname",
    "2.5.4.5": "serialNumber",
    "2.5.4.6": "countryName",
    "2.5.4.7": "localityName",
    "2.5.4.8": "stateOrProvinceName",
    "2.5.4.9": "streetAddress",
    "2.5.4.10": "organizationName",
    "2.5.4.11": "organizationalUnitName",
    "2.5.4.12": "title",
    "2.5.4.13": "description",
    "2.5.4.42": "givenName",

    "1.2.840.113549.1.9.1": "emailAddress",

    "2.5.29.14": "X509v3 Subject Key Identifier",
    "2.5.29.15": "X509v3 Key Usage",
    "2.5.29.16": "X509v3 Private Key Usage Period",
    "2.5.29.17": "X509v3 Subject Alternative Name",
    "2.5.29.18": "X509v3 Issuer Alternative Name",
    "2.5.29.19": "X509v3 Basic Constraints",
    "2.5.29.30": "X509v3 Name Constraints",
    "2.5.29.31": "X509v3 CRL Distribution Points",
    "2.5.29.32": "X509v3 Certificate Policies Extension",
    "2.5.29.33": "X509v3 Policy Mappings",
    "2.5.29.35": "X509v3 Authority Key Identifier",
    "2.5.29.36": "X509v3 Policy Constraints",
    "2.5.29.37": "X509v3 Extended Key Usage"
}
def tag_id_to_string(identifier):
    """Return a string representation of a ASN.1 id."""
    if identifier in tag_id_to_string_map:
        return tag_id_to_string_map[identifier]
    return '{:#02x}'.format(identifier)


def class_id_to_string(identifier):
    """Return a string representation of an ASN.1 class."""
    if identifier in class_id_to_string_map:
        return class_id_to_string_map[identifier]
    raise ValueError('Illegal class: {:#02x}'.format(identifier))


def object_identifier_to_string(identifier):
    if identifier in object_id_to_string_map:
        return object_id_to_string_map[identifier]
    return identifier


def value_to_string(tag_number, value):
    if tag_number == asn1.Numbers.ObjectIdentifier:
        return object_identifier_to_string(value)
    elif isinstance(value, bytes):
        return '0x' + str(binascii.hexlify(value).upper())
    elif isinstance(value, str):
        return value
    else:
        return repr(value)
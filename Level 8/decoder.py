import base64



secret = "3d3d516343746d4d6d6c315669563362"


def decoder(encoded_hex):
    # Step 1: Convert hex to the reversed Base64 encoded string
    reversed_base64 = bytes.fromhex(encoded_hex).decode('utf-8')
    
    # Step 2: Reverse the Base64 encoded string to its original form
    original_base64 = reversed_base64[::-1]
    
    # Step 3: Decode the Base64 encoded string to get the original input
    original_string = base64.b64decode(original_base64).decode('utf-8')
    
    return original_string

secret_decodedd = decoder(secret)
print(secret_decodedd)
import base64

def encode_base64(image_url):
    with open(image_url, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

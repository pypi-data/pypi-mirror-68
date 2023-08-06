import uuid

def generate_uuid():
    result = '0'
    while result[0] not in {'a', 'b', 'c', 'd', 'e', 'f'}:
        result = uuid.uuid4().hex
        result = result[0:8] + '_' + result[8:12] + '_' + result[12:16] + '_' + result[16:20] + '_' + result[20:]
    return result
def guid_generator():
    k = 0
    while True:
        yield k
        k += 1

guid = guid_generator()

def next():
    return guid.next()

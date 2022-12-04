import random

def charN(str, N):
    if N < len(str):
        return str[N]
    return 'X'
    
def xor(str1, str2):
    length = max(len(str1),len(str2))
    return ''.join(chr(ord(charN(str1,i)) ^ ord(charN(str2,i))) for i in range(length))

def randChunkNums(total_chunks):
    size = random.randint(1,min(5, total_chunks))
    return random.sample(range(total_chunks), size)
import os
from random import seed, random
from hashlib import md5

def __random_md5(rand_num):
    return str(md5(str(rand_num).encode()).hexdigest())

# Create and store or retrieve a valid hardware id for authentication
def generate_hwid():
    file_name = "hwid.txt"
    hwid = None
    f_hwid = None
    try:
        f_hwid = open(file_name, "r+")
        hwid = f_hwid.readline()
    except IOError:
        print("Creating hwid.txt")
        f_hwid = open(file_name, "w").close()

    if hwid:
        print("Found a hardware id")
        print(hwid)
    else:
        print("Generating a new hardware id")
        seed(None, 2)

        short_md5 = __random_md5(random())[:-8]

        hwid = "#1-{}:{}:{}-{}-{}-{}-{}-{}".format(
            __random_md5(random()),
            __random_md5(random()),
            __random_md5(random()),
            __random_md5(random()),
            __random_md5(random()),
            __random_md5(random()),
            __random_md5(random()),
            short_md5
        )
        print("Saving hardware id to {}".format(file_name))
        print(hwid)
        f_hwid.write(hwid)
    
    f_hwid.close()

    return hwid
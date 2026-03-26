import os
import hashlib


def resetDir():
    """ Sets current working directory to the folder containing the script
        (For Relative Pathing)
    """
    fileName = __file__
    if type(fileName.split("\\")) == list and len(fileName.split("\\"))>1:
        fileName = fileName.split("\\")[-1]
        filePath = __file__.replace(fileName,"")
    else:
        fileName = fileName.split("/")[-1]
        filePath = __file__.replace(fileName,"")
    os.chdir(filePath)
    return os.path.abspath(filePath)

def generateRowIDHash(RowTextRaw : str):
    encoded_input = RowTextRaw.encode('utf-8')
    hash_object = hashlib.sha256(encoded_input)
    hex_digest = hash_object.hexdigest()
    return hex_digest
"""
To reformat the file path, changing the number postfix from v1, v2 to v001, v002 etc...
"""

__author__ = 'wei ning'

import os
import re


def fixNumberPadding(filePath, padding=4, numberPrefix=''):

    """
    To fix the padding of the number in the given file path, e.g.

    D:\\etc\\file (01).jpg -> D:\\etc\\file (0001).jpg

    :param filePath:
    :return: True if the given file has been fixed; False otherwise
    """

    result = re.search('[0-9]{1,}', filePath)
    if not result:
        return False
    origNumStr = result.group()
    origNum = int(origNumStr)
    newFilePath = ('%s%s'%(numberPrefix, '%%0%dd'%padding%origNum)).join(filePath.split(origNumStr))
    os.rename(filePath, newFilePath)

if __name__ == "__main__":
    dirPath = r'C:\TDDOWNLOAD\pingshu\three'
    for fileName in os.listdir(dirPath):
        filePath = os.path.join(dirPath, fileName)
        fixNumberPadding(filePath)
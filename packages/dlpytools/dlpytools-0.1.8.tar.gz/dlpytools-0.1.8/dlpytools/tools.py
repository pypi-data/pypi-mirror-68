import os
import sys
import time 

osPlatform = sys.platform
if osPlatform == 'win32':
    FPSLASH = '\\'
if osPlatform == 'linux1' or osPlatform == 'linux2' or osPlatform == 'linux':
    FPSLASH = '/'


def getAFiles(cwd='.',fileList=[]):
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
    if os.path.isfile(path):
      fileList.append(path)
  for each in dirs:
    getAFiles(each,fileList)
  return fileList

def getADirs(cwd='.',dirList=[]):  
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
      dirList.append(path)
  for each in dirs:
    getADirs(each,dirList)
  return dirList

def getCFiles(cwd='.'):
  allPath = os.listdir(cwd)
  files = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isfile(path):
      files.append(path)
  return files

def getCDirs(cwd='.'):
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
  return dirs

# copy file from src1 to src2
def copy(src1,src2):
    with open(src1,'rb') as f:
        data = f.read()
    with open(src2,'wb') as f:
        f.write(data)
def getDate():
    localtime = time.localtime()
    monthStr = str(localtime[1]) if localtime[1] >= 10 else "0"+str(localtime[1])
    dateStr = str(localtime[2]) if localtime[2] >= 10 else "0"+str(localtime[2])
    timeString = f"{str(localtime[0])}-{monthStr}-{dateStr}"
    return timeString

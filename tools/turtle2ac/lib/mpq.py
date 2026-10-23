import ctypes,os
import os
L=ctypes.CDLL(os.environ.get('STORMLIB','/home/claude/StormLib/build/libstorm.so'))
H=ctypes.c_void_p
def open_archive(p):
    h=H(); ok=L.SFileOpenArchive(p.encode(),0,0x100,ctypes.byref(h))
    if not ok: raise OSError('open fail %s'%p)
    return h
class FIND(ctypes.Structure):
    _fields_=[('cFileName',ctypes.c_char*1024),('szPlainName',ctypes.c_char_p),('dwHashIndex',ctypes.c_uint),('dwBlockIndex',ctypes.c_uint),('dwFileSize',ctypes.c_uint),('dwFileFlags',ctypes.c_uint),('dwCompSize',ctypes.c_uint),('dwFileTimeLo',ctypes.c_uint),('dwFileTimeHi',ctypes.c_uint),('lcLocale',ctypes.c_uint)]
def listfiles(h,mask='*'):
    fd=FIND(); out=[]
    L.SFileFindFirstFile.restype=H
    f=L.SFileFindFirstFile(h,mask.encode(),ctypes.byref(fd),None)
    if not f: return out
    out.append((fd.cFileName.decode('latin1'),fd.dwFileSize))
    while L.SFileFindNextFile(H(f),ctypes.byref(fd)): out.append((fd.cFileName.decode('latin1'),fd.dwFileSize))
    L.SFileFindClose(H(f)); return out
def read(h,name):
    fh=H()
    if not L.SFileOpenFileEx(h,name.encode(),0,ctypes.byref(fh)): return None
    sz=L.SFileGetFileSize(fh,None); buf=ctypes.create_string_buffer(sz); rd=ctypes.c_uint()
    L.SFileReadFile(fh,buf,sz,ctypes.byref(rd),None); L.SFileCloseFile(fh); return buf.raw[:rd.value]

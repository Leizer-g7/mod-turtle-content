import ctypes,os,sys
import os
L=ctypes.CDLL(os.environ.get('STORMLIB','/home/claude/StormLib/build/libstorm.so'))
def make(out, files):
    if os.path.exists(out): os.remove(out)
    h=ctypes.c_void_p()
    ok=L.SFileCreateArchive(out.encode(), 0x00100000|0x00200000|0x01000000, max(64, len(files) + 16), ctypes.byref(h))
    assert ok, 'create failed'
    for local, arch in files:
        ok=L.SFileAddFileEx(h, local.encode(), arch.encode(), 0x00000200|0x80000000, 0x02, 0xFFFFFFFF)
        assert ok, 'add failed '+arch
    L.SFileCompactArchive(h, None, 0)
    L.SFileCloseArchive(h)
if __name__=='__main__':
    root=sys.argv[2]; files=[]
    for d,_,fs in os.walk(root):
        for f in fs:
            p=os.path.join(d,f); files.append((p, os.path.relpath(p,root).replace('/','\\')))
    make(sys.argv[1], files); print(sys.argv[1], os.path.getsize(sys.argv[1]), files)

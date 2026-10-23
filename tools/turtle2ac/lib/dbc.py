import struct
def load(path):
    b=open(path,'rb').read()
    magic,n,f,rs,ss=struct.unpack('<4s4I',b[:20])
    assert magic==b'WDBC',magic
    recs=b[20:20+n*rs]; strs=b[20+n*rs:20+n*rs+ss]
    rows=[]
    for i in range(n):
        r=recs[i*rs:(i+1)*rs]
        rows.append(list(struct.unpack('<%dI'%(rs//4),r)))
    def s(o):
        if o==0 or o>=len(strs): return ''
        e=strs.index(b'\0',o); return strs[o:e].decode('utf8','replace')
    return n,f,rs,rows,s,strs

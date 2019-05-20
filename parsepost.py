import uuid,os

def main(b):
    useruuid=uuid.uuid4()
    os.mkdir('uploads/'+str(useruuid))
    f=b.split(b'-----------------------------')
    while b'' in f:
        f.remove(b'')
    while '\r\n' in f:
        f.remove(b'\r\n')
    for i in f:
        i=i[i.find(b'\r\n')+2:]
        if i==b'':
            pass
        elif i.startswith(b'Content-Disposition: form-data; name="fileToUpload1"'):
            filename=i[i.find(b'filename="')+10:i.find(b'"\r\n')].decode()
            if filename.split('.')[-1]=='asm':
                i=i[i.find(b'\r\n')+2:]
                i=i[i.find(b'\r\n\r\n')+4:]
                i=i[:-2]
                file=open('uploads/'+str(useruuid)+'/patch.asm','wb')
                file.write(i)
                file.close()
                #if i!='': print(i)
            else:
                pass
        elif i.startswith(b'Content-Disposition: form-data; name="fileToUpload2"'):
            filename=i[i.find(b'filename="')+10:i.find(b'"\r\n')].decode()
            if filename.split('.')[-1]=='smc':
                i=i[i.find(b'\r\n')+2:]
                i=i[i.find(b'\r\n\r\n')+4:]
                i=i[:-2]
                file=open('uploads/'+str(useruuid)+'/rom.smc','wb')
                file.write(i)
                file.close()
            else:
                pass
    return useruuid

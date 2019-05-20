import http.server,threading,queue,uuid,os,base64,parsepost,shutil #people always forget that you can do this (seperate by ",")

cur=True
corlist={}

##def convert(inputtype,outputtype,data,useruuid):
##    global corlist
##    bytesdata=base64.b64decode(data)
##    fname=str(useruuid)+'.'+inputtype
##    foutname=str(useruuid)+' - out'+'.'+outputtype
##    file=open(fname,'wb')
##    file.write(bytesdata)
##    file.close()
##    os.system('ffmpeg -i "'+fname+'" "'+foutname+'"')
##    file=open(foutname,'rb')
##    outbytesdata=base64.b64encode(file.read())
##    file.close()
##    outbytesdata=b'<data>'+outbytesdata+b'</data>'
##    corlist.update({useruuid: outbytesdata})
    

def server():
    global cur
    class handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            global wfile
            global cur
            global corlist
            """Serve a GET request."""
            cur = not cur
            message = str(cur).lower() #str(int(cur))
            #print(poll)

            useruuid=None
            if 'submit=Upload' in self.path:
                useruuid=self.do_POST()
                #cpath=(self.path[1:] if self.path.startswith('/') else self.path).split('?')[0]
                #cfile=open('index.html','rb')
##                cfile=open('uploads/'+str(useruuid)+'/rom.smc','rb')
##                cr=cfile.read()
##                self.protocol_version = "HTTP/1.1"
##                self.send_response(200)
##                self.send_header("Content-Length", len(cr))
##                self.end_headers()
##                self.wfile.write(cr)
##                cfile.close()
##                print('served page',self.path)
##            elif self.path.startswith('/convert/'):
##                inputtype=self.path[9:self.path.find('/',9)].lower()
##                outputtype=self.path[10+len(inputtype):self.path.find('/',10+len(inputtype))].lower()
##                print('from',inputtype,'to',outputtype)
##                data=self.path[11+len(inputtype)+len(outputtype):]
##                print('got data')
##                useruuid=uuid.uuid4()
##                th=threading.Thread(target=convert,args=(inputtype,outputtype,data,useruuid))
##                th.start()
##                message=None
##                attempt=0
##                while message==None:
##                    message=corlist.get(useruuid)
##                    if message==None and not th.isAlive() and attempt==100:
##                        message=b'None'
##                    elif message==None and not th.isAlive():
##                        attempt+=1
##                self.protocol_version = "HTTP/1.1"
##                self.send_response(200)
##                self.send_header("Content-Length", len(message))
##                self.end_headers()
##                self.wfile.write(message)#bytes(message, 'ASCII'))#"utf8"))
##                print('served conversion')
            else:
                if self.path!='/':
                    cpath=(self.path[1:] if self.path.startswith('/') else self.path).split('?')[0]
                else:
                    cpath='index.html'
                try:
                    if useruuid!=None:
                        cfile=open('uploads/'+str(useruuid)+'/rom.smc','rb')
                    else:
                        cfile=open(cpath,'rb')
                    cr=cfile.read()
                    self.protocol_version = "HTTP/1.1"
                    self.send_response(200)
                    if useruuid!=None:
                        self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Length", len(cr))
                    self.end_headers()
                    self.wfile.write(cr)
                    cfile.close()
                    print('served page',self.path)
                except FileNotFoundError:
                    message=b'404!'
                    self.protocol_version = "HTTP/1.1"
                    self.send_response(404)
                    self.send_header("Content-Length", len(message))
                    self.end_headers()
                    self.wfile.write(message)
                    print('served 404')
                #self.wfile.close()
            return
        #def do_POST(self):
        #    th=threading.Thread(target=self.POST)#,args=(self,))
        #    th.start()
        def do_POST(self):
            global rfile,rbt
            #print(dir(self.headers))
            rfile=self.rfile
            print('received post')
            self.protocol_version = "HTTP/1.1"
            self.send_response(200)
            print('readable:',rfile.readable())
            #exit()
            rb=b''
            rbln=0
            while True:
                rbt=self.rfile.read(1)
                #if rbt==b'':
                #    break
                #if rbt==b'-':
                #    print('-',len(rb))
                rb+=rbt
                if rb.endswith(b'Content-Disposition: form-data; name="submit'):
                    #print('submit')
                    #print(rb[-100:])
                    break
                #rbln+=1
                #if rbln<100:
                #    print(rb)
                #if rbln%20000==0:
                #    print(rbln)
                #print(rbt)
            print('read done')
            #print(rb[-100:])
            #r=rb.decode()
            #print(r)
            useruuid=parsepost.main(rb)
            os.system('asar\\asar.exe "uploads/'+str(useruuid)+'/patch.asm" "uploads/'+str(useruuid)+'/rom.smc"')
            cpath=(self.path[1:] if self.path.startswith('/') else self.path).split('?')[0]
            if useruuid!=None:
                cfile=open('uploads/'+str(useruuid)+'/rom.smc','rb')
            else:
                cfile=open(cpath,'rb')
            cr=cfile.read()
            if useruuid!=None:
                self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", len(cr))
            self.end_headers()
            self.wfile.write(cr)
            cfile.close()
            print('served page for post request on page',self.path)
            print('now deleting user content')
            shutil.rmtree('uploads/'+str(useruuid))
            print('deleted user content for UUID'+str(useruuid)+'.')
##            cfile=open('uploads/'+str(useruuid)+'/rom.smc','rb')
##            cr=cfile.read()
##            self.protocol_version = "HTTP/1.1"
##            self.send_response(200)
##            self.send_header("Content-Length", len(cr))
##            self.end_headers()
##            self.wfile.write(cr)
##            cfile.close()
##            print('served page',self.path)
            
            #print('asar\\asar.exe "uploads/'+str(useruuid)+'/patch.asm" "uploads/'+str(useruuid)+'/rom.smc"')
            #cpath=self.path[1:] if self.path.startswith('/') else self.path
            #cfile=open(cpath,'rb')
            #cr=cfile.read()
##            cr=b'http://localhost:5314/index.html'
##            self.protocol_version = "HTTP/1.1"
##            self.send_response(301)
##            self.send_header("Content-Length", len(cr))
##            self.end_headers()
##            self.wfile.write(cr)
            #cfile.close()
            #print('served page',self.path)
            return useruuid
        def log_message(self, format, *args): return
    https=http.server.HTTPServer(('localhost',80),handler)
    print('server start')
    https.serve_forever()
if __name__=='__main__':
    server()


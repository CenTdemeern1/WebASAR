import http.server
import uuid
import subprocess
import parsepost
import shutil
#i put them in seperate lines. here you go randomdude.    

def server():
    global cur
    class handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """Serve a GET request."""
            useruuid=None
            try:
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
            except:
                pass #for if someone tries to do something stupid
            return
        def do_POST(self):
            print('received post')
            self.protocol_version = "HTTP/1.1"
            self.send_response(200)
            rb=b''
            rbln=0
            while True:
                rbt=self.rfile.read(1) #may be slow, i'll look at this later
                rb+=rbt
                if rb.endswith(b'Content-Disposition: form-data; name="submit'):
                    break #yeah we got the information
            print('read done')
            useruuid=parsepost.main(rb)
            try:
                subprocess.check_output('asar\\asar.exe "uploads/'+str(useruuid)+'/patch.asm" "uploads/'+str(useruuid)+'/rom.smc"',timeout=10)#hey, a timeout of 10 seconds is enough.
                cpath=(self.path[1:] if self.path.startswith('/') else self.path).split('?')[0]
            except subprocess.TimeoutExpired:
                shutil.rmtree('uploads/'+str(useruuid))
                useruuid=None
                cpath='oops.txt'
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
            if useruuid!=None:
                shutil.rmtree('uploads/'+str(useruuid))
                print('deleted user content for UUID'+str(useruuid)+'.')
            return
        def log_message(self, format, *args): return
    https=http.server.ThreadingHTTPServer(('localhost',80),handler)
    print('server start')
    https.serve_forever()
if __name__=='__main__':
    server()


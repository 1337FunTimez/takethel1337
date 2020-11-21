from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, os, random, re, urllib.parse

prev_list=[]
for root, dirs, files in os.walk('.'):
    for file in files:
        fn=os.path.join(root,file)
        if(fn.endswith('.quiz.html')):
            prev_list.append(re.sub('.quiz.html','',fn))

w_list = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ' #characters you want in string
def generate_pin(length=30):
    tp = random.sample(w_list, length)
    pin = ''.join(tp)
    if pin not in prev_list: #list of already generated pins
       prev_list.append(pin)
       return pin
    else:
       return generate_pin()

class BasicHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-Type", 'text/html')
        self.end_headers()
        
        path=self.path[1:]
        if path=='' or path.endswith('/'):
            path+='index.html'
        path=path.split('?')
        print(path[0])
        if path[0] == 'special.html':
            print(path[1])
            pin=generate_pin()
            r=open(pin+'.user.html','w')
            r.write('')
            r.close()
            r=open(pin+'.quiz.html','w')
            r.write(path[1])
            r.close()
            self.wfile.write(open(path[0],'rb').read()+b' Your game id is: '+pin.encode()+b'<script>setTimeout(()=>{location.href="game.html?'+pin.encode()+b'"},10000)</script>')
        elif path[0].endswith('.quiz.html'):
            self.wfile.write(open(path[0],'rb').read())
            r=open(re.sub('.quiz.html','',path[0])+'.user.html','a')
            r.write(urllib.parse.unquote(path[1])+'<br>')
            r.close()
        elif path[0] == 'game.html':
            self.wfile.write(b'Join At: '+path[1].encode()+b'<br>'+open(path[1]+'.user.html','rb').read()+b'<script>pp=setTimeout(()=>{location.reload()},1000)</script>')
        else:
            self.wfile.write(open(path[0],'rb').read())

s=HTTPServer(('',sys.argv[1]),BasicHTTPRequestHandler);
try:
    s.serve_forever();
except KeyboardInterrupt:
    print("Keyboard input!!! Exiting!");
    sys.exit(0)

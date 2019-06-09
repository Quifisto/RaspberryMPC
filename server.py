from http.server import BaseHTTPRequestHandler, HTTPServer
from os import system, popen, curdir, sep

port = 8080
html_file = "index.html"
actions = {'play':'play', 'pause':'pause', 'next':'next', 'prev':'prev', 'volup':'volume +10', 'voldown':'volume -10'}

#This class will handle any incoming request from the browser.
class myHandler(BaseHTTPRequestHandler):
    
    # Handle mpc actions with the os library.
    def mpc_action(self):
        action = self.path[1:]
        if action in actions.keys():
            command = 'mpc ' + actions[action]
            print('Executing action', command)
            action_status = popen(command, 'r').read()
            print(action_status)       

            return True
        return False


    # Handle get requests.
    def do_GET(self):
        # Check for actions in the url. 
        self.mpc_action()

        # Get mpc status and playlist
        mpc_status = popen('mpc status', 'r')
        curr_playlist = popen('mpc playlist', 'r')
        all_songs = popen('mpc listall', 'r')

        # Send the html page.
        with open(curdir + sep + html_file, 'r') as webpage:
            # Replace lines with the mpc status.
            response = ''
            for line in webpage:
                if 'MPCSTATUS' in line:
                    response += mpc_status.read()
                
                elif 'PLAYLIST' in line:
                    front, back = line.split('PLAYLIST')
                    response += front + curr_playlist.read() + back
                
                elif 'ALLSONGS' in line:
                    front, back = line.split('ALLSONGS')
                    response += front + all_songs.read() + back
                
                else:
                    response += line
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

        return


#### MAIN ####

# set up starting playlist
playlist =  popen('mpc playlist', 'r').readline()
if playlist == '':
    system('mpc ls | mpc add')
    print("Added all songs to playlist")
else:
    print("found open playlist")

try:
    # Create the server and the handler for the incoming request
    server = HTTPServer(('', port), myHandler)
    print(' Started httpserver on port ', port)
    server.serve_forever()

except KeyboardInterrupt:
    print(' interrupt received, server shuttingdown')
    server.socket.close()


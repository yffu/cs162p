import socket
import struct
import threading
import time

#https://www.youtube.com/watch?v=VvwLXnY-mKk
# server is authoritative, makes all decisions about what is allowed. 
class GameServer:
    def __init__(self, host='127.0.0.1', port=49152):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0
        self.players = []

    def run_listener(self, conn):
        self.thread_count += 1
        conn.setsockopt(socket.AF_INET, socket.TCP_NODELAY, True)
        conn.settimeout(1)
        with conn:
            while not self.kill:
                try:
                    data = conn.recv(4096)
                    if len(data):
                        target_space = struct.unpack_from('B', data, 0)[0]
                except socket.timeout:
                    pass
        self.thread_count -= 1

    def connection_listen_loop(self):
        self.thread_count += 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #TCP
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True) # easier for address to be reused, after server is killed
            s.bind((self.host, self.port))
            while not self.kill:
                s.settimeout(1) # sockets can prevent thread from closing, so if kill = true we can exit this loop
                s.listen()
                try:
                    conn, addr = s.accept()
                    print('new connection: ', conn, addr)
                    if len(self.players) < 2:
                        self.players.append(conn)
                        # spawn listener task
                except socket.timeout:
                    continue
                time.sleep(0.01)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print('killed')

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()
        try:
            while True:
                time.sleep(0.05)
        except KeyboardInterrupt:
            self.await_kill()
            

if __name__ == '__main__':
    GameServer().run()

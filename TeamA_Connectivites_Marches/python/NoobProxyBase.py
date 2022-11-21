import socket
import select
import sys

class NoobProxyBase(object):
   def __init__(self):
      self.sockets = []
      self.connections = []
      self.period = 0.001

      self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.buffer_server_address = ('localhost', 30017)

      print("[PROXY] Starting on %s port %s" % self.buffer_server_address)
      self.sock_server.bind(self.buffer_server_address)
      self.sock_server.listen(1)
      self.sockets.append(self.sock_server)

      self.sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_address = ('localhost', 31017)

   def run(self):
      self.process_idle()
      readable, writable, errored = select.select(self.sockets, [], [], self.period)

      try:
         for s in readable : 
            if s is self.sock_server:
               client_socket, client_address = self.sock_server.accept()

               self.sockets.append(client_socket)
               self.connections.append(client_socket)

               print("[PROXY] Recv connection from", client_address)

               print("[PROXY] Connecting to server %s %s", self.server_address)
               self.sock_client.connect(self.server_address)

               message = b'MarketData request'
               print("[PROXY] Send message : %s", message)
               self.sock_client.sendall(message)

               self.sockets.append(self.sock_client)

            elif s is self.sock_client:
               data = self.sock_client.recv(104)
               if data:
                  print(f"[PROXY] Recv [{data}]")
                  self.on_data_received(data)
      
            else:
               data = s.recv(1024)
               if data:
                  print(data)
               else:
                  print("[PROXY] Closing connection {s}")
                  self.disconnect(s)

      except ConnectionResetError:
          self.disconnect(s)

   def disconnect(self, s):
      print("[PROXY] Disconnect client {s}")
      self.sock_client.close()
      s.close()
      self.sockets.remove(s)
      self.connection.remove(s)  


   def send_message(self, message):
      self.connections[0].sendall(message)

   def on_data_received(self, data):
      pass

   def process_idle(self):
      pass

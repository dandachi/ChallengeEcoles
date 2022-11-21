import NoobProxy
import socket 
import select
import sys
import threading
import time

from datetime import datetime

HEADER = "START=1.1|"
FOOTER = "END=SG|"

LENGTH_TAG = "LENGTH"
SECURITY_TAG = "SECURITY"
BIDPX_TAG = "BIDPX"
OFFERPX_TAG = "OFFERPX"
BIDSIZE_TAG = "BIDSIZE" 
OFFERSIZE_TAG = "OFFERSIZE" 
MKTREF_TAG = "MKTREF" 

SEP = "|"

class Decoder:
   def __init__(self):
      self.buffer = ""

   def get_body_length(self, msg):
      start = msg.find(LENGTH_TAG)
      if start != -1 :
         end = msg[start + len(LENGTH_TAG):].find(SEP)
         if end != -1:
            length = msg[start + len(LENGTH_TAG) + 1: start + len(LENGTH_TAG) + end] 
            return length
      return None

   def get_field(self, msg, tag, pos = 0):
      tag_start = msg[pos:].find(tag)
      if tag_start != -1 :
         end = msg[pos + tag_start + len(tag):].find(SEP)
         if end != -1:
            entries = msg[pos + tag_start + len(tag) + 1: pos + tag_start + len(tag) + end] 
            return entries
      return None

   def get_security(self, msg, pos = 0):
      return self.get_field(msg, SECURITY_TAG, pos)

   def get_bidpx(self, msg, pos = 0):
      return self.get_field(msg, BIDPX_TAG, pos)

   def get_offerpx(self, msg, pos = 0):
      return self.get_field(msg, OFFERPX_TAG, pos)

   def get_bidsize(self, msg, pos = 0):
      return self.get_field(msg, BIDSIZE_TAG, pos)

   def get_offersize(self, msg, pos = 0):
      return self.get_field(msg, OFFERSIZE_TAG, pos)

   def get_mktref(self, msg, pos = 0):
      return self.get_field(msg, MKTREF_TAG, pos)

   def get_next_entry(self, msg, index):
      return msg.find(SECURITY_TAG, index)

   def is_header(self, input):
      return input == HEADER

   def is_footer(self, input):
      return input == FOOTER

   def decode_msg(self, msg):
      points = 0
      entries = []

      index = self.get_next_entry(msg, 0)
      nb_entries = msg.count(SECURITY_TAG)

      for i in range(0, nb_entries):
         security = self.get_security(msg, index)
         bid_px = self.get_bidpx(msg, index)
         offer_px = self.get_offerpx(msg, index)
         bid_size = self.get_bidsize(msg, index)
         offer_size = self.get_offersize(msg, index)
         mkt_ref = self.get_mktref(msg, index)

         if security and bid_px and offer_px and bid_size and offer_size:
            s = Streaming(security, mkt_ref, bid_px, bid_size, offer_px, offer_size)
            entries.append(s)
            #print(f"Found : {security} {bid_px} {bid_size} {offer_px} {offer_size}")

         else:
            points -= 5
            print(f"Missing mandatory field.")

         index = self.get_next_entry(msg, index + len(SECURITY_TAG))
         #order = Order(security, side, price, quantity)
      return entries, points

      

   def process_data(self, data):
      msgs = []
    
      index = 0
      buffer = self.buffer + data.decode('ascii')
      while (index < len(buffer)):
         if (index + len(HEADER) - 1) < len(buffer):
            header = buffer[index:(index + len(HEADER))]
            msg_complete = False
            if self.is_header(str(header)):
               msg_start = index
               index = index + len(HEADER)
               
               if (index < len(buffer)):
                  length = self.get_body_length(buffer[index:])
                  if length:
                     index = index + len(LENGTH_TAG) + 1 + len(length) + 1 
                     if (index + int(length) < len(buffer)):
                        body = buffer[index:(index + int(length))]
                        index = index + len(body)
                     if (index + len(FOOTER) - 1) < len(buffer):
                        footer = buffer[index:(index + len(FOOTER))]
                        if self.is_footer(footer):
   
                           index = index + len(FOOTER)
                           msg_end = index
                           msg_complete = True
   
               if msg_complete:
                  msg = buffer[msg_start:msg_end]
                  self.buffer = ""
                  msgs.append(msg)
               else:
                  self.buffer = buffer[msg_start:]
                  return msgs
            else:
               self.buffer = buffer[index:]
               return msgs
         else:
            self.buffer = buffer[index:]
            return msgs

      return msgs


class Streaming:
   def __init__(self, security, mkt_ref, bid_px, bid_size, offer_px, offer_size):
      self.security = security
      self.mkt_ref = mkt_ref
      self.bid_px = bid_px
      self.bid_size = bid_size
      self.offer_px = offer_px
      self.offer_size = offer_size
  
   def update(self, s):
      points = 0
      if self.bid_px != s.bid_px:
         self.bid_px = s.bid_px
         points += 8
      else:
         points -= 6

      if self.offer_px != s.offer_px:
         self.offer_px = s.offer_px
         points += 8 
      else:
         points -= 6

      if self.bid_size != s.bid_size:
         self.bid_size = s.bid_size
         points += 5 

      if self.offer_size != s.offer_size:
         self.offer_size = s.offer_size
         points += 5

      self.mkt_ref = s.mkt_ref

      return points

   def show(self):
      print(f"[{self.bid_size} {self.bid_px} | {self.offer_px} {self.offer_size}]")

class StreamingHandler:
   def __init__(self):
      self.streaming_data = {}

   def update_book(self, streaming):
      points = 0
      if not streaming.security in self.streaming_data:
         self.streaming_data[streaming.security] = streaming
         points += 10
         #print(f"NEW [{streaming.security}] : "\
         #   f"[{self.streaming_data[streaming.security].bid_size}" \
         #   f" {self.streaming_data[streaming.security].bid_px} |" \
         #   f" {self.streaming_data[streaming.security].offer_px}" \
         #   f" {self.streaming_data[streaming.security].offer_size}]")

      else:
         #print(f"UPDATE [{streaming.security}] : "\
         #   f"[{self.streaming_data[streaming.security].bid_size}" \
         #   f" {self.streaming_data[streaming.security].bid_px} |" \
         #   f" {self.streaming_data[streaming.security].offer_px}" \
         #   f" {self.streaming_data[streaming.security].offer_size}] --> " \
         #   f" [{streaming.bid_size} {streaming.bid_px} | {streaming.offer_px} {streaming.offer_size}]")

         points += self.streaming_data[streaming.security].update(streaming)

      return points


class Server:
   def __init__(self, reference_book):
      self.index = 0
      self.data = list()

      self.securities_mkt_ref = {}
      self.reference_book = reference_book

      self.sock = None
      self.server_address = ('localhost', 31017)

      self.running = False
      self.is_connected = False
      self.period = 0.005

      self.connections = []
      self.sockets = []

   def init(self):
      self.load_data()

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[PROVIDER] Starting server on %s port %s" % self.server_address)
      self.sock.bind(self.server_address)

      self.sock.listen(5)
      self.sockets.append(self.sock)

   def load_data(self):
      self.securities_mkt_ref["BOIS"] = 0
      self.securities_mkt_ref["EAUX"] = 0
      self.securities_mkt_ref["ELEC"] = 0
      self.securities_mkt_ref["CAFE"] = 0
      self.securities_mkt_ref["BRIE"] = 0

      self.data = list((
      list(("BOIS", "100.1", "100", "100.2", "100")),
      list(("EAUX", "100.1", "100", "100.2", "100")),
      list(("ELEC", "100.1", "100", "100.2", "100")),
      list(("CAFE", "100.1", "100", "100.2", "100")),
      list(("BRIE", "100.1", "100", "100.2", "100")),
      list(("BOIS", "100.0", "100", "100.2", "100")),
      list(("BOIS", "100.0", "100", "100.2", "100")),
      list(("EAUX", "100.0", "100", "100.2", "100")),
      list(("EAUX", "100.0", "100", "100.2", "100")),
      list(("ELEC", "100.0", "100", "100.2", "100")),
      list(("ELEC", "100.0", "100", "100.2", "100")),
      list(("CAFE", "100.0", "100", "100.2", "100")),
      list(("CAFE", "100.0", "100", "100.2", "100")),
      list(("BRIE", "100.0", "100", "100.2", "100")),
      list(("BRIE", "100.0", "100", "100.2", "100")),
      list(("BOIS", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("ELEC", "100.2", "100", "100.3", "100")),
      list(("CAFE", "100.2", "100", "100.3", "100")),
      list(("BRIE", "100.2", "100", "100.3", "100")),
      list(("BOIS", "100.0", "100", "100.2", "100")),
      list(("BOIS", "100.0", "100", "100.2", "100")),
      list(("EAUX", "100.0", "100", "100.2", "100")),
      list(("EAUX", "100.0", "100", "100.2", "100")),
      list(("ELEC", "100.0", "100", "100.2", "100")),
      list(("ELEC", "100.0", "100", "100.2", "100")),
      list(("CAFE", "100.0", "100", "100.2", "100")),
      list(("CAFE", "100.0", "100", "100.2", "100")),
      list(("BRIE", "100.0", "100", "100.2", "100")),
      list(("BRIE", "100.0", "100", "100.2", "100")),
      list(("BOIS", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("ELEC", "100.2", "100", "100.3", "100")),
      list(("CAFE", "100.2", "100", "100.3", "100")),
      list(("BRIE", "100.2", "100", "100.3", "100")),
      list(("BOIS", "100.3", "100", "100.5", "100")),
      list(("EAUX", "100.3", "100", "100.5", "100")),
      list(("ELEC", "100.3", "100", "100.5", "100")),
      list(("CAFE", "100.3", "100", "100.5", "100")),
      list(("BRIE", "100.3", "100", "100.5", "100")),
      list(("BOIS", "100.3", "100", "100.5", "100")),
      list(("EAUX", "100.3", "100", "100.5", "100")),
      list(("ELEC", "100.3", "100", "100.5", "100")),
      list(("CAFE", "100.3", "100", "100.5", "100")),
      list(("BOIS", "100.3", "100", "100.5", "100")),
      list(("EAUX", "100.3", "100", "100.5", "100")),
      list(("ELEC", "100.3", "100", "100.5", "100")),
      list(("CAFE", "100.3", "100", "100.5", "100")),
      list(("BRIE", "100.3", "100", "100.5", "100")),
      list(("BRIE", "100.3", "100", "100.5", "100")),
      list(("BOIS", "100.2", "100", "100.4", "100")),
      list(("EAUX", "100.2", "100", "100.4", "100")),
      list(("ELEC", "100.2", "100", "100.4", "100")),
      list(("CAFE", "100.2", "100", "100.4", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("EAUX", "100.1", "100", "100.3", "100")),
      list(("ELEC", "100.1", "100", "100.3", "100")),
      list(("CAFE", "100.1", "100", "100.3", "100")),
      list(("BRIE", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("EAUX", "100.1", "100", "100.3", "100")),
      list(("ELEC", "100.1", "100", "100.3", "100")),
      list(("CAFE", "100.1", "100", "100.3", "100")),
      list(("BRIE", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.1", "100", "100.3", "100")),
      list(("EAUX", "100.1", "100", "100.3", "100")),
      list(("ELEC", "100.1", "100", "100.3", "100")),
      list(("CAFE", "100.1", "100", "100.3", "100")),
      list(("BRIE", "100.1", "100", "100.3", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("ELEC", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BOIS", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.2", "100", "100.4", "100")),
      list(("EAUX", "100.2", "100", "100.4", "100")),
      list(("EAUX", "100.2", "100", "100.4", "100")),
      list(("EAUX", "100.2", "100", "100.4", "100")),
      list(("ELEC", "100.2", "100", "100.4", "100")),
      list(("ELEC", "100.2", "100", "100.4", "100")),
      list(("ELEC", "100.2", "100", "100.4", "100")),
      list(("CAFE", "100.2", "100", "100.4", "100")),
      list(("CAFE", "100.2", "100", "100.4", "100")),
      list(("CAFE", "100.2", "100", "100.4", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.3", "100", "100.5", "100")),
      list(("EAUX", "100.3", "100", "100.5", "100")),
      list(("ELEC", "100.3", "100", "100.5", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("CAFE", "100.3", "100", "100.5", "100")),
      list(("BRIE", "100.3", "100", "100.5", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("ELEC", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("ELEC", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BOIS", "100.5", "100", "100.5", "100")),
      list(("EAUX", "100.5", "100", "100.5", "100")),
      list(("ELEC", "100.5", "100", "100.5", "100")),
      list(("CAFE", "100.5", "100", "100.5", "100")),
      list(("BRIE", "100.5", "100", "100.5", "100")),
      list(("BOIS", "100.5", "100", "100.5", "100")),
      list(("EAUX", "100.5", "100", "100.5", "100")),
      list(("ELEC", "100.5", "100", "100.5", "100")),
      list(("CAFE", "100.5", "100", "100.5", "100")),
      list(("BRIE", "100.5", "100", "100.5", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("ELEC", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.2", "100", "100.4", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("ELEC", "100.5", "100", "100.5", "100")),
      list(("CAFE", "100.5", "100", "100.5", "100")),
      list(("ELEC", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.2", "100", "100.3", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("BRIE", "100.4", "100", "100.5", "100")),
      list(("CAFE", "100.5", "100", "100.5", "100")),
      list(("BRIE", "100.5", "100", "100.5", "100")),
      list(("BRIE", "100.2", "100", "100.4", "100")),
      list(("BOIS", "100.4", "100", "100.5", "100")),
      list(("EAUX", "100.4", "100", "100.5", "100")),
      list(("BOIS", "100.5", "100", "100.5", "100")),
      list(("EAUX", "100.5", "100", "100.5", "100")),
      list(("ELEC", "100.5", "100", "100.5", "100")),
      list(("CAFE", "100.5", "100", "100.5", "100")),
      ))

   def serialize(self, input):

      data = "SECURITY=" + input[0] + "|" \
             "MKTREF=" + f"{self.securities_mkt_ref[input[0]]:03d}" + "|" \
             "BIDPX=" + input[1] + "|" \
             "BIDSIZE=" + input[2] + "|" \
             "OFFERPX=" + input[3] + "|" \
             "OFFERSIZE=" + input[4] + "|"

      length = len(data)
      data = "START=1.1|" + "LENGTH=" + str(length) + "|" + data + "END=SG|"
      return str.encode(data)

   def publish(self, data):
      self.reference_book.setdefault(data[0], {})
      mkt_ref = f'{self.securities_mkt_ref[data[0]]:03d}'
      self.reference_book[data[0]].update({ mkt_ref : [data[1], data[2], data[3], data[4]]})    
      return

   def on_new_connection(self):
      readable, writable, errored = select.select(self.sockets, [], [], self.period)

      try:
         for s in readable : 
            if s is self.sock:
               client_socket, client_address = self.sock.accept()

               self.connections.append(client_socket)
               self.sockets.append(client_socket)

               print("[PROVIDER] Recv connection from", client_address)
            else:
               data = s.recv(1024)
               if data:
                  print(f"Recv data {data}")
               else:
                  print("[PROXY] Closing connection {s}")
                  self.disconnect(s)

      except ConnectionResetError:
          self.disconnect(s)


   def run(self):
      self.on_new_connection()

      if len(self.connections) < 1:
         return

      self.is_connected = True
      if not self.running:
         t = threading.Timer(self.period, self.send_data)
         t.start()
         self.running = True

      if not self.is_connected:
         t.cancel()
         self.running = False

   def send_data(self):
      update = self.data[self.index % len(self.data)]

      self.publish(update)
      data = self.serialize(update)

      self.securities_mkt_ref[update[0]] += 1 
      self.index += 1
      
      self.running = False 
      #print(f"[PROVIDER] Sending to clients : {data}")
      try:
         for s in self.connections:
            s.sendall(data)
      except (BrokenPipeError, ConnectionResetError):
         self.is_connected = False
         print("[PROVIDER] Exception occured. Closing connection ... ")

   def disconnect(self, s):
      print("[PROVIDER] Disconnect client {s}")
      s.close()
      self.sockets.remove(s)
      self.connections.remove(s)  

      self.is_connected = False
      self.running = False
      

   def reset_connection(self):
      self.index = 0
      self.running = False
      self.is_connected = False

   def handle_new_connection(self):
      connection, client_address = self.sock.accept()
      self.is_connected = True

      print("[PROVIDER] Recv connection from", client_address)

      while self.is_connected:
         if not self.running:
            t = threading.Timer(self.period, self.send_data, [connection])
            t.start()
            self.running = True
         if not self.is_connected:
            t.cancel()
            self.running = False

      connection.close()
      print("[PROVIDER] Connection closed!")


class Client:
   def __init__(self):
      self.sock = None
      self.server_address = ('localhost', 30017)
      self.connected = False

      self.decoder = Decoder()
      self.timeout = 0.01

   def start(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("[CONSUMER] Connecting to server %s %s", self.server_address)
      self.sock.connect(self.server_address)
      self.connected = True

   def stop(self):
      self.sock.close()

   def init_connection(self):
      message = b'Hello, kindly request data !'
      print("[CONSUMER] Send message : %s", message)
      self.sock.sendall(message)

   def is_connected(self):
      return self.connected 

   def disconnect(self):
      self.connected = False

   def read_data(self):
      readable, writable, errored = select.select([self.sock], [], [], self.timeout)

      try:
         for s in readable : 
            if s is self.sock:
               return self.sock.recv(128)
      
      except ConnectionResetError:
          self.disconnect(s)


   def process(self):
      data = self.read_data()

      if data:
         return self.process_data(data)

      return 0

class StudentClient(Client):
   def __init__(self, reference_book):
      Client.__init__(self)

      self.streaming_handler = StreamingHandler()
      self.reference_book = reference_book

      self.config_processing_capacity = 10
      self.config_processing_period = 1

      self.processed_msg_count = 0
      self.start_period_time = 0

      self.total_msg_processed = 0

   def can_process_msgs(self):
      if self.processed_msg_count == 0:
         self.start_period_time = datetime.now().timestamp()
      
      if self.processed_msg_count >= self.config_processing_capacity:
         return False
      return True

   def check_window(self):
      ts = datetime.now().timestamp()
      if ts - self.start_period_time > self.config_processing_period:
         self.start_period_time = datetime.now().timestamp()
         self.processed_msg_count = 0

   def check_book_consistency(self, s):
      if not s.security in self.reference_book.keys():
#         print(f"[CONSUMER] -5p : Unknown security")
         return -5

      if not s.mkt_ref in list(self.reference_book[s.security].keys()):
#         print(f"[CONSUMER] -5p : Unknown mktref : [{s.mkt_ref}] in {list(self.reference_book[s.security].keys())}")
         return -20

      points = 0
      if s.bid_px != self.reference_book[s.security][s.mkt_ref][0]:
#         print(f"[CONSUMER] -5p : Wrong bidpx ")
         points -= 10

      if s.bid_size != self.reference_book[s.security][s.mkt_ref][1]:
#         print(f"[CONSUMER] -5p : Wrong bidsize ")
         points -= 10

      if s.offer_px != self.reference_book[s.security][s.mkt_ref][2]:
#        print(f"[CONSUMER] -5p : Wrong offerpx ")
         points -= 10

      if s.offer_size != self.reference_book[s.security][s.mkt_ref][3]:
#        print(f"[CONSUMER] -5p : Wrong offersize ")
         points -= 10

      if s.mkt_ref == list(self.reference_book[s.security].keys())[-1]: 
#         print("[CONSUMER] +10p EXCELLENT ! MOST RECENT MKT REF")
         points += 10

      elif s.mkt_ref in list(self.reference_book[s.security].keys())[-5:]: 
#         print(f"[CONSUMER] +5p COOL ! NOT BAD MKT REF [{s.mkt_ref}] / [{list(self.reference_book[s.security].keys())[-1]}]")
         points += 5

      elif s.mkt_ref in list(self.reference_book[s.security].keys())[-10:]:
#         print(f"[CONSUMER] +1p CAN DO BETTER ! MKTREF [{s.mkt_ref}] / [{list(self.reference_book[s.security].keys())[-1]}]")
         points += 1
 
      else:
         points -= 3

      return points
      

   def process_data(self, data):
      msgs = self.decoder.process_data(data)
      points = 0
      for msg in msgs:
         entries, p = self.decoder.decode_msg(msg)

         points += p
         for e in entries:
            points += self.streaming_handler.update_book(e)
            points += self.check_book_consistency(e)


      self.processed_msg_count += len(msgs)
      self.total_msg_processed += len(msgs)

      #print(f"[CONSUMER] Adding points {points} / new msgs {len(msgs)} / nb_msgs {self.total_msg_processed}")
      return points

class Consumer:
   def __init__(self, reference_book):
      self.student_client = StudentClient(reference_book)

      self.score = 0 

      self.start_time = datetime.now().timestamp()
      self.duration = 10

   def start(self):
      self.student_client.start()
      self.student_client.init_connection()

   def stop(self):
      self.student_client.stop()
  
   def keep_running(self):
      if not self.student_client.is_connected():
         return False 

      ts = datetime.now().timestamp()
      return (ts - self.start_time) <= self.duration

   def run(self):
      if (self.student_client.can_process_msgs()):
         self.score += self.student_client.process()
      else:
         self.student_client.check_window()


class Launcher:
   def __init__(self):
      self.reference_book = {}
      self.provider = Server(self.reference_book)
      self.consumer = None
      self.proxy = None


   def init(self):
      self.provider.init()

#      self.proxy = ChiwaProxy.ChiwaProxy()
      self.proxy =  NoobProxy.NoobProxy()
      self.consumer = Consumer(self.reference_book)
      self.consumer.start()

   def run(self):
      self.provider.run()
      self.proxy.run()
      self.consumer.run()

   def stop(self):
      self.consumer.stop()

   def get_score(self):
      return self.consumer.score

   def get_total_msg_processed(self):
      return self.consumer.student_client.total_msg_processed

   def keep_running(self):
      return self.consumer.keep_running()


launcher = Launcher()
launcher.init()

try:
   while launcher.keep_running():
      launcher.run()

finally:
   print(f"CONGRATS ! FINAL SCORE : {launcher.get_score()} . Total msg processed : {launcher.get_total_msg_processed()}")
   launcher.stop()


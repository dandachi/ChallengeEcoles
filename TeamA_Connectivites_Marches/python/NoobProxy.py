import NoobProxyBase

class NoobProxy(NoobProxyBase.NoobProxyBase):
   def __init__(self):
      NoobProxyBase.NoobProxyBase.__init__(self)
      self.data = None

   def on_data_received(self, data):
      self.data = data
      #print("[PROXY] Receive data from server :%s", data)

   def process_idle(self):
      if self.data:
         self.send_message(self.data)
 

import asyncio
from time import sleep
from datetime import datetime, timedelta 
    
class GrabCarClientV2:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.start_time = datetime.now()
        
    
    def get_reading(self,secondstoget):
        current_time = datetime.now()
        delta = current_time - self.start_time
        message = secondstoget #delta.seconds
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.connect_and_get_data(message,loop))#self.host,self.port, self,message, loop))
        
        return result

    async def connect_and_get_data(self,message,loop):#self,host,port,car,message, loop):
        reader, writer = await asyncio.open_connection(self.host,self.port,loop=loop)

        print(f'Data sent to host: {message}')
        writer.write(str(message).encode())

        data = await reader.readline()
        decoded = data.decode("utf-8")
        #car.readings.append(decoded)
        self.readings = decoded
        #print(f'Data received from host: {decoded}')

        #print('Closing the socket to host...')
        writer.close()

        return decoded



    
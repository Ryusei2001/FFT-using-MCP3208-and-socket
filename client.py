import socket
import numpy as np

class BaseClient:
        def __init__(self, timeout:int=10, buffer:int=1024):
                self.__socket = None
                self.__address = None
                self.__timeout = timeout
                self.__buffer = buffer

        def connect(self, address, family:int, typ:int, proto:int):
                self.__address = address
                self.__socket = socket.socket(family, typ, proto)
                self.__socket.settimeout(self.__timeout)
                self.__socket.connect(self.__address)

        def send(self, message:str="") -> None:
                flag = False
                while True:
#                       if message == "":
#                                message_send = input("> ")
#                       else:
#                               message_send=message
#                               flag = True
#                               self.__socket.send(message_send.encode('utf-8'))
                        message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
                        self.received(message_recv)
                        if flag:
                                break
                try:
                        self.__socket.shutdown(socket.SHUT_RDWR)
                        self.__socket.close()
                except:
                        pass

        def received(self, message:str):
                value = []
                value = message.split(',')
                print("Row:")
                print(message)
                print("List:")
                print(value)
                FFTrow = len(value)
                self.FFT(value, FFTrow)

        def FFT(self, value:list, FFTrow:int):
                if list(bin(FFTrow)).count('1') != 1:
                    pass
                SpectrumAmplitude = [0.0] * FFTrow
                FFT = np.fft.fft(value[0:0+FFTrow])
                for i in range(FFTrow):
                        SpectrumAmplitude[i] = np.sqrt(FFT[i].real * FFT[i].real + FFT[i].imag * FFT[i].imag)

                print("FFT Result")
				#toriaezu
                value_freq = 128

                Freqency = [0.0] * FFTrow
                for j in range(FFTrow):
                        print(SpectrumAmplitude[j])
                        Freqency[j] = (j * value_freq) / FFTrow

class InetClient(BaseClient):
        #def __init__(self, host:str="192.168.1.7", port:int=8080) -> None:
        def __init__(self, host:str="192.168.0.6", port:int=8080) -> None:
                self.server=(host,port)
                super().__init__(timeout=60, buffer=1024)
                super().connect(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)

if __name__=="__main__":
        cli = InetClient()
        cli.send()

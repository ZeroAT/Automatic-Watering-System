import time
import os
import glob
import RPi.GPIO as GPIO
import logging
import threading
import datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from coapthon import defines


from coapthon.resources.resource import Resource
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

p = GPIO.PWM(19, 50)  
GPIO.output(19, True)

p.start(0)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


class ObservableResource(Resource):

    def __init__(self, name="Moisture", coap_server=None):
        super(ObservableResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        self.payload = "Observable Resource"
        self.period = 5
        self.update(True)

    def render_GET(self, request):

        return self

    def render_POST(self, request):
        self.payload = request.payload
        return self

    def update(self, first=False):
        self.value = mcp.read_adc(0)
        self.payload = str(self.value)


        if not self._coap_server.stopped.isSet():

            timer = threading.Timer(self.period, self.update)
            timer.setDaemon(True)
            timer.start()


            if not first and self._coap_server is not None:
                logger.debug("Periodic Update")
                myValue = mcp.read_adc(0)
                print(myValue)
                p = GPIO.PWM(19, 50)
                p.start(0)
                while(myValue>):
                    p.ChangeDutyCycle(70)
                    time.sleep(0.2)
                else:
                    print("The dirt is wet right now...")
                    p.stop() 
                self._coap_server.notify(self)
                self.observe_count += 1
                                
                                
##class Moisture(Resource):
##    def __init__(self, name="Moisture", coap_server=None, obs=True):
##        super(Moisture, self).__init__(name, coap_server, visible=True, observable=obs, allow_children=True)
##
##    def render_GET(self, request):
##        self.value = mcp.read_adc(0)
##
##        self.payload = str(self.value)
##        self._coap_server.notify(self)
##        #while(GPIO.input(26) == True):
##            #p.ChangeDutyCycle(40)
##            #time.sleep(0.2)
##            #self.payload = "The dirt is dry"
##
##        #p.stop()
##        #self.payload = "The dirt is wet"
##        #GPIO.cleanup()
##        
##       
##        return self
##
##    def render_PUT(self, request):
##        self.edit_resource(request)
##        return self
##
##    def render_POST(self, request):
##        res = self.init_resource(request, MultipleEncodingResource())
##        return res
##

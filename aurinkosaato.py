#------------------------------------------------
# Name      : aurinko
# Author    : Ari Kristola
# Created   : 10/10/2014
# Python    : 2.7
# Copyright : (c) Ari Kristola 2014
#------------------------------------------------
# pari pikku juttua
# ennen ohjelman toimintaa pitaa antaa kasky
# sudo /opt/owfs/bin/owfs --i2c=ALL:ALL --allow_other /mnt/1wire/
# jotta lampotila ilmestyy hakemistoon /mnt/1wire
# tassa mukana flask webbiserveri JOU JOU

# Import required libraries
import time
import RPi.GPIO as GPIO
import spidev
import os
import redis

pannu_file = os.path.join("/","mnt","1wire","28.D06B20060000","temperature")
patteri_file = os.path.join("/","mnt","1wire","28.51B420060000","temperature")

r_server = redis.Redis('localhost')

spi = spidev.SpiDev()
spi.open(0,0)
spidac = spidev.SpiDev()
spidac.open(0,1)
spidac.max_speed_hz = (20000000)

GPIO.setwarnings(False)
# use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT) # da-muunnos tarttee


# Define GPIO signals to use
# that are connected to 8 transistors
# Pins 7,11,13,15,19,24,23,16,18,22
# GPIO4,GPIO17,GPIO21,GPIO22,GPIO10,
# GPIO8,GPIO11,GPIO23,GPIO24,GPIO25
RpiGPIO = [31,32,33,36,35,38,37,40]

GPIO.output(29, True) # eka vastus paalle
#GPIO.output(22, False)

# Set all pins as output
#for pin in RpiGPIO:
#  print ("Setup pins")
#  GPIO.setup(pin,GPIO.OUT)

# Define some settings
StepCounter = 0
StepDir = 1
WaitTime = 0.01
teho = 0.0
U = 0.0
I = 0.0
valinta = 4
vertailuteho = -500.0
vertailujannite = 0.0
lampolaskuri = 70
pannuTemp = 0.0
patteriTemp = 0.0
KWHmittari = 0.0
tehosumma = 0.0
pannustringi = "paljon"

# tallennetun jannitteen arvoksi laitetaan 0V
# aluksi mitataan jannitetta jos jannite muuttuu 10V talletetusta arvosta
# mennaan eteenpain ja etsitaan optimikuormitus

# vastussekvenssit
# sekvenssi 1
StepCount1 = 8
Seq1 = []
Seq1 = range(0,StepCount1)
Seq1[0] =[1,1,1,1,1,1,1,1]
Seq1[1] =[0,0,0,0,0,0,0,0]
Seq1[2] =[1,1,1,1,1,1,1,1]
Seq1[3] =[0,0,0,1,1,0,0,0]
Seq1[4] =[1,1,1,1,1,1,1,1]
Seq1[5] =[0,0,1,1,1,1,0,0]
Seq1[6] =[1,1,1,1,1,1,1,1]
Seq1[7] =[0,1,1,1,1,1,1,0]

# oma pannu
StepCount2 = 18
Seq2 = []
Seq2 = range(0,StepCount2)
Seq2[0] =[0,0,0,0,0,0,0,0]  #50.00
Seq2[1] =[0,0,0,1,0,0,0,0]  #25.00
Seq2[2] =[0,0,0,0,0,0,0,1]  #20.76
Seq2[3] =[0,1,0,0,0,0,1,0]  #14.67
Seq2[4] =[0,0,0,0,0,0,1,1]  #13.10
Seq2[5] =[0,0,1,0,1,0,0,1]  #11.34
Seq2[6] =[0,0,0,0,1,0,0,1]  #10.38
Seq2[7] =[0,0,0,0,0,1,1,1]  #9.57
Seq2[8] =[0,0,1,1,1,0,0,1]  #9.24
Seq2[9] =[0,1,1,0,0,0,1,1]  #8.59
Seq2[10] =[0,0,1,0,0,1,1,1] #8.03
Seq2[11] =[1,1,0,1,0,1,1,0] #7.33
Seq2[12] =[0,1,0,1,0,1,1,1] #6.92
Seq2[13] =[0,1,1,1,1,0,1,1] #6.39
Seq2[14] =[1,1,1,0,0,1,1,1] #6.01
Seq2[15] =[1,1,1,1,1,0,1,1] #5.67
Seq2[16] =[1,1,1,0,1,1,1,1] #5.42
Seq2[17] =[1,1,1,1,1,1,1,1] #4.89

# sekvenssi 2
StepCount3 = 8
Seq3 = []
Seq3 = range(0,StepCount3)
Seq3[0] =[1,0,0,0,0,0,0,0]
Seq3[1] =[0,1,0,0,0,0,0,0]
Seq3[2] =[0,0,1,0,0,0,0,1]
Seq3[3] =[0,0,0,1,0,0,1,0]
Seq3[4] =[0,0,0,0,1,1,0,0]
Seq3[5] =[0,0,0,1,0,0,1,0]
Seq3[6] =[0,0,1,0,0,0,0,1]
Seq3[7] =[0,1,0,0,0,0,0,0]

# Choose a sequence to use
Seq = Seq2
StepCount = StepCount2


# read SPI data from MCP3002 chip
def get_adc(channel):
	# Only 2 channels 0 and 1 else return -1
	if ((channel > 1) or (channel < 0)):
		return -1
	r = spi.xfer2([1,(2+channel)<<6,0])
           
	ret = ((r[1]&0x0F) << 8) + (r[2])
	return ret  

def setOutput(channel, val):

        lowByte = val & 0xff;
        highByte = ((val >> 8) & 0xff) | channel << 7 | 0x1 << 5 | 1 << 4;
        spidac.xfer2([highByte, lowByte])

# pollari eli ns. paaluuppi
while True:
  time.sleep(0.995)
  U = get_adc(1)    # in2
  setOutput(1,U)    # O2
  U = U * 0.0814721 # jannite kohilleen
  I = get_adc(0)    # in1
  setOutput(0,I*3)  # O1
  I = (I-5) * 0.047794 # 75mV/100A gain24.444 1100mVmax
  teho = U * I * 1000 # kerrotaan tuhannella niin saadaan vaikuttavampi teho testiin
  lampolaskuri = lampolaskuri + 1
  tehosumma = tehosumma + teho # tehosumma on joulet
#  pannustringi = str(int(tehosumma))
#  r_server.set('pannumittaus', tehosumma)

  if lampolaskuri > 599: # kun 10 minuuttia kulunut, mitataan lampotilat ja paivitetaan KWH-mittari
    file_object=open(pannu_file,'r')  # haetaan pannun lampo
    line=file_object.read()
    pannuTemp=float(line)
    file_object.close()
    file_object=open(patteri_file,'r')  # haetaan patteriveden lampo
    line=file_object.read()
    patteriTemp=float(line)
    file_object.close()
    lampolaskuri = 0
    KWHmittari = KWHmittari + (tehosumma / 3600000)
    r_server.set('KWH', KWHmittari)
    r_server.set('PANNU', pannuTemp)
    tehosumma = 0
    print ("U=%0.1f ")%U,("I=%0.2f ")%I,("P=%0.2fW ")%teho,(" tv=%0.2f ")%pannuTemp,(" KWH=%0.1f ")%KWHmittari,time.strftime("%H:%M:%S:  %d.%m.%Y", time.localtime())
  
  if (vertailujannite > U + 1) or (vertailujannite < U - 1):
        lampolaskuri = 0
        StepCounter = 0
        vertailuteho = 0.0
        vertailujannite = 0.0

        while StepCounter < StepCount:

          for pin in range(0, 8):
            xpin = RpiGPIO[pin]
            if Seq[StepCounter][pin]!=0: #talla saisi nakyviin print (" Enable %i") %xpin
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False) #print (" Disable %i") %xpin

          time.sleep(WaitTime) # tahan valiin tehon mittaus ja laskenta ja suurinta tehoa vastaava StepCounter
          U = get_adc(1)       
          U = U * 0.0814721
          I = get_adc(0)
          teho = U * I
      
          if vertailuteho < teho: # eli jos kombinaation teho on suurempi,
            vertailuteho = teho   # kuin edellisen kombinaation, laitetaan
            valinta = StepCounter # teho ja U talteen verrattavaksi seuraavaan
            vertailujannite = U   # kombinaatioon. jaljelle jaava kombinaatio
                                  # on paras.

          StepCounter = StepCounter + 1 #askellellaaan
         
# tassa ollaan jo ulkona sekvenssista
        if pannuTemp > 90:
          for pin in range(0, 8): # jos pannu kuumana, katkaistaan lammitys
            xpin = RpiGPIO[pin]
            if Seq[0][pin]!=0:
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)
        else:
          for pin in range(0, 8): # tuupataan valittu kombinaatio ulos
            xpin = RpiGPIO[pin]
            if Seq[valinta][pin]!=0:
              GPIO.output(xpin, True)
            else:
              GPIO.output(xpin, False)




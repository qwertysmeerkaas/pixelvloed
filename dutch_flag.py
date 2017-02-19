#!/usr/bin/python
"""This is an udp / binary client

Inspired by the PixelFlut projector on eth0:winter 2016 and
code from https://github.com/defnull/pixelflut/
"""

__version__ = 0.3
__author__ = "Jan Klopper <jan@underdark.nl>"

import random
from vloed import PixelVloedClient, NewMessage, RGBPixel, MAX_PIXELS

def BlueFill(message, width, height):
  """Generates a random number of pixels with a random color"""
  for pixel in xrange(0, random.randint(140, MAX_PIXELS)):
    pixel = RGBPixel(random.randint(0, 1366),
                     random.randint(height*2/3, height),
                     random.randint(0, 0),
                     random.randint(0, 0),
                     random.randint(255, 255))
    try:
      message.append(pixel)
    except IndexError:
      yield ''.join(message)
      message[2:] = [pixel]
  yield ''.join(message)

def RedFill(message, width, height):
  """Generates a random number of pixels with a random color"""
  for pixel in xrange(0, random.randint(140, MAX_PIXELS)):
    pixel = RGBPixel(random.randint(0, 1366),
                     random.randint(0, height/3),
                     random.randint(255, 255),
                     random.randint(0, 0),
                     random.randint(0, 0))
    try:
      message.append(pixel)
    except IndexError:
      yield ''.join(message)
      message[2:] = [pixel]
  yield ''.join(message)

def WhiteFill(message, width, height):
  """Generates a random number of pixels with a random color"""
  for pixel in xrange(0, random.randint(140, MAX_PIXELS)):
    pixel = RGBPixel(random.randint(0, 1366),
                     random.randint(height/3, (height*2/3)),
                     random.randint(255, 255),
                     random.randint(255, 255),
                     random.randint(255, 255))
    try:
      message.append(pixel)
    except IndexError:
      yield ''.join(message)
      message[2:] = [pixel]
  yield ''.join(message)

def RunClient(options):
  """Discover the servers and start sending to the first one"""

  client = PixelVloedClient(True, # start as soon as we find a server
                            options.debug, # show debugging output
                            options.ip, # ip of the server, None for autodetect
                            options.port, # port of the server None for autodetect
                            options.width, # Screen pixels wide, None for autodetect
                            options.height  # Screen pixels height, None for autodetect
                            )
  message = NewMessage() #create a new message that buffers the output etc

  # loop the effect until we cancel by pressing ctrl+c / exit the program
  while True:
    # create a new message and send it every time the buffer is full
    # the width/height are read from the client's config
    for packet in BlueFill(message, client.width, client.height):
      # send the message we just filled with random pixels
      client.SendPacket(packet)
    for packet in RedFill(message, client.width, client.height):
      # send the message we just filled with random pixels
      client.SendPacket(packet)
    for packet in WhiteFill(message, client.width, client.height):
      # send the message we just filled with random pixels
      client.SendPacket(packet)
      
if __name__ == '__main__':
  # if this script is called from the command line, and thus not imported
  # start a client and start sending messages
  import optparse
  parser = optparse.OptionParser()
  parser.add_option('-v', action="store_true", dest="debug", default=False)
  parser.add_option('-i', action="store", dest="ip", default=None)
  parser.add_option('-p', action="store", dest="port", default=None,
                    type="int")
  parser.add_option('-x', action="store", dest="width", default=None,
                    type="int")
  parser.add_option('-y', action="store", dest="height", default=None,
                    type="int")
  options, remainder = parser.parse_args()

  try:
    RunClient(options)
  except KeyboardInterrupt:
    print 'Closing client'

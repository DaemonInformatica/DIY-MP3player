#!/usr/bin/python

from CMP3proc   import CMP3proc
from subprocess import call

import RPIO as GPIO
import sys
import time

pMP3Play = None

def initMP3():
  global pMP3Play

  print("Initializing MP3 object.")
  pMP3Play = CMP3proc()  
  
  print("MP3 object initialized.")

def initGPIO():
  print("initializing GPIO pins...")
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(7, GPIO.IN)
  GPIO.add_interrupt_callback(7,  handle_incvol,   edge='rising')
  GPIO.add_interrupt_callback(8,  handle_stop,     edge='rising')
  GPIO.add_interrupt_callback(11, handle_play,     edge='rising')
  GPIO.add_interrupt_callback(25, handle_pause,    edge='rising')
  GPIO.add_interrupt_callback(9,  handle_decvol,   edge='rising')
  GPIO.add_interrupt_callback(10, handle_next,     edge='rising')

  print("GPIO pins initialized. Waiting for interrupts.")
  GPIO.wait_for_interrupts()


def handle_callback(gpio_id, value):
  print("GPIO pin ID: ", gpio_id)


def handle_stop(gpio_id, value):
  global pMP3Play
  print("main: called stop")
  pMP3Play.stop()


def handle_incvol(gpio_id, value):
  print("handle_incvol")
  global pMP3Play
  pMP3Play.incVolume()


def handle_decvol(gpio_id, value):
  print("handle_decvol")
  global pMP3Play
  pMP3Play.decVolume()


def handle_pause(gpio_id, value):
  global pMP3Play
  print("main: called pause")

  # figure out current state. 
  bIsPlaying = pMP3Play.m_bIsPlaying

  # if current state is 'paused' call cont else call pause
  if(bIsPlaying == True):
    pMP3Play.pause()
  else: 
    pMP3Play.cont()


def handle_exit(gpio_id, value):
  global pMP3lay
  print("main: called exit")  
  pMP3Play.stop()
  sys.exit(0)


def handle_play(gpio_id, value):
  global pMP3lay
  print("main: called play")
  pMP3Play.play()


def handle_list_mp3(gpio_id, value):
  global pMP3Play
  print("GPIO pin id: ", gpio_id)
  print(pMP3Play.getArrMP3())


def handle_next(gpio_id, value):
  global pMP3Play
  pMP3Play.next()


def main():
  print("Starting MP3player.")
  initMP3()
  initGPIO()
  

if __name__ == '__main__':
  main()

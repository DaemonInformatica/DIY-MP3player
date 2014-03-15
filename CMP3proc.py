#!/usr/bin/python

import glob
import alsaaudio
import ConfigParser
from CPlayThread import CPlayThread

class CMP3proc:  
  m_arrMP3     = []
  m_bIsPlaying = False
  m_nPlayIndex = 0
  m_pAlsaDev   = None
  m_pMP3Thread = None
  m_strMP3Dir  = ""
  m_nVolume    = 60

  def __init__(self):
    self.initConfig()
    self.initFileList()
    self.initAlsaDevice()


  def initConfig(self):
    print("Reading configuration file")
    config = ConfigParser.RawConfigParser()
    config.read("/home/mp3player/mp3player/settings.cfg")
    self.m_strMP3Dir = config.get("settings", "mp3dir")


  def initFileList(self):
    print("Initializing mp3 list")
    print("checking directory " + self.m_strMP3Dir)

    self.m_arrMP3 = glob.glob(self.m_strMP3Dir + "/*.mp3")

    print(`len(self.m_arrMP3)` + " mp3's found.")


  def initAlsaDevice(self):
    print("Initializing Alsa device...")

    card            = "default"
    self.m_pAlsaDev = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, card=card)

    self.m_pAlsaDev.setchannels(2)
    self.m_pAlsaDev.setrate(44100)
    self.m_pAlsaDev.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    self.m_pAlsaDev.setperiodsize(160)

    # set mixer settings: 
    m = alsaaudio.Mixer("PCM")
    m.setvolume(self.m_nVolume)

    print("Alsa initialized.")


  def getArrMP3(self):
    return self.m_arrMP3


  def play(self):   
    # if an mp3 is already playing: pause it. 
    if(self.m_pMP3Thread != None and self.m_bIsPlaying == True):
      self.pause()
      return
    elif(self.m_pMP3Thread != None and self.m_bIsPlaying == False):
      self.cont()
      return

    print("starting play for mp3: " + `self.m_nPlayIndex`)

    #validate index on mp3 list. 
    if(self.m_nPlayIndex >= len(self.m_arrMP3)):    
      return false
    
    # start new threaded process for playing an mp3
    filename          = self.m_arrMP3[self.m_nPlayIndex]
    print("CMP3proc::play: filename: " + filename)
    self.m_pMP3Thread = CPlayThread(self.m_pAlsaDev, filename, self)
    
    print("Starting new thread")
    self.m_pMP3Thread.start()
    self.m_bIsPlaying = True
    print("new thread started")


  # def pause(self):
  def pause(self):
    print("Pausing play")
    # if nothing is currently playing: ignore it. 
    if(self.m_pMP3Thread == None):
      return False

    # send 'pause' signal to the current thread. 
    self.m_pMP3Thread.mp3_pause()
    self.m_bIsPlaying = False
    print("Play paused")


  def cont(self):
    print("Continue-ing play")

    #if nothing was playing and now paused: ignore it. 
    if(self.m_pMP3Thread == None):
      return False

    # send continue signal to curent thread. 
    self.m_pMP3Thread.play()
    self.m_bIsPlaying = True
    print("Play continued.")

    
  # def stop(self):
  def stop(self):
    print("Stopping play...")

    # if no thread exists: ignore it. 
    if(self.m_pMP3Thread == None):
      return False

    # send stop signal to the thread and nullify it. 
    self.m_pMP3Thread.stop()
    self.m_pMP3Thread = None

    print("Play stopped.")

  
  # def next(self):
  def next(self):
    print("Skipping mp3")
    if(self.m_nPlayIndex < len(self.m_arrMP3) - 1):
      self.m_nPlayIndex += 1
    else:
      return

    # stop the thread.
    self.stop()

    # update index by one. 

    # call play. 
    self.play()
    print("Mp3 skipped. Playing next mp3")

  # def previous(self):
  def previous(self):
    print("Previous mp3...")
    # stop the thread. 
    self.stop()

    #if current index > 0
    if(self.m_nPlayIndex > 0):
      # update index by -1
      self.m_nPlayIndex -= 1

    # call play
    self.play()
    print("Jumped back mp3.")


  def updateVolume(self):
    m = alsaaudio.Mixer("PCM")
    m.setvolume(self.m_nVolume)
    

  def incVolume(self):
    self.m_nVolume += 10
    if(self.m_nVolume > 100):
      self.m_nVolume = 100
  
    self.updateVolume()


  def decVolume(self):
    self.m_nVolume -= 10

    if(self.m_nVolume < 0):
      self.m_nVolume = 0

    self.updateVolume()


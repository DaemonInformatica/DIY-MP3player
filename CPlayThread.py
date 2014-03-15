#!/usr/bin/python

import mad
import threading

class CPlayThread (threading.Thread):
  # properties
  m_pAlsaDev   = None  # Alsa device
  m_filename   = ""    # filename plus relative path of the mp3 to play
  m_bIsPlaying = True  # whether we're playing or pausing.
  m_bDoRun     = True  # this keeps alive the while loop in the run method. call stop to kill it.
  m_pMad       = None  # pymad object. 
  m_pParent    = None  # parent CMP3Proc object to call when the song's done. 

  def __init__(self, pAlsaDev, filename, pParent):
    print("Initializing new mp3 thread.")
    threading.Thread.__init__(self)

    self.m_pAlsaDev = pAlsaDev
    self.m_filename = filename
    self.m_pParent  = pParent

    self.initMadLib()
    print("Done initializing mp3 thread")


  def initMadLib(self):
    print("initMadLib...")
    self.m_pMad = mad.MadFile(self.m_filename)
    print("pymad lib initialized")


  # def run(self)
  def run(self):
    print("CPlayThread: Starting run")

    while(self.m_bDoRun == True):
      # are we in fact playing? 
      if(self.m_bIsPlaying == True):
        # get next peice of the file. 
        data = self.m_pMad.read()

        # if there's data: stream it to the output. else call next in the parent and kill the loop. 
        if(data):
          self.m_pAlsaDev.write(data)
        else:
          self.m_bDoRun = False
          self.m_pParent.next()

    print("CPlayThread for file " + self.m_filename + " ended")


  # def play(self):
  def play(self):
    self.m_bIsPlaying = True

  # def mp3_pause(self):
  def mp3_pause(self):
    self.m_bIsPlaying = False

  # def stop(self):
  def stop(self):
    self.m_bDoRun = False

import pyautogui as pg
import os
from time import sleep

"""pg.click(x=100, y=200, clicks=1,
          interval=0.2, # Time between clicks
          button="right", # Right mouse button
          duration=0.5) # Time taken to move the mouse to the position 
          """


### Crating Folder in the Desktop
# Open Folder
pg.hotkey("win", "e")

# CREATE FOLDER
## Gonna Download Path
pg.click(1673,26, duration=0.15)

sleep(2)
## Create folder
pg.click(2724,59, duration=0.15, button="right") # New Folder Button

sleep(2)
pg.click(2744,355, duration=0.1) # New Folder Button

sleep(2)
pg.hotkey("enter")
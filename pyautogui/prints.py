import pyautogui


pyautogui.screenshot("Screenshot.png")


# Screenshot Region
pyautogui.screenshot("teste.png", region=(0, #  X axis
                                          0, #  Y axis
                                          300, # Width
                                          400))# Height
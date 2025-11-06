import pyautogui


password = pyautogui.password(text='Enter Passowrd', title='Password Dialog', default='', mask='*')
print(password)
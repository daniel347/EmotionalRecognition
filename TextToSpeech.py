#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 15:46:05 2020

@author: taradiviney
"""

import os
import requests
import time
from xml.etree import ElementTree

try:
    input = raw_input
except NameError:
    pass


class TextToSpeech(object):
    def __init__(self,subscription_key): 
        self.subscription_key = subscription_key #service key id
        self.tts = input("What would you like to convert to speech: ")
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
    def get_token(self):
        fetch_token_url = "https://uksouth.api.cognitive.microsoft.com/sts/v1.0/issuetoken" #endpoint issued
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key}
        response = requests.post(fetch_token_url, headers=headers)
        print(response.text)
        self.access_token = str(response.text)
        print(self.access_token)
        
        
    def save_audio(self):
        base_url = 'https://uksouth.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
        'Authorization': 'Bearer ' + self.access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'HackCambridge-AuralFeedback'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        print(response.text)
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                  "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
              "\nSomething went wrong. Check your subscription key and headers.\n")
    
if __name__ == "__main__":
   subscription_key = "18cc0b753fa74192a6bac800febea621"
   app = TextToSpeech(subscription_key)
   app.get_token()
   app.save_audio()
        
        
    
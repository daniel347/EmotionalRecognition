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
import random
import simpleaudio as sa
import subprocess

device_name = "Dora the Fedora"

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key #service key id
        # self.tts = input("What would you like to convert to speech: ")
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        try:
            with open("tts_token.txt", "r") as f:
                self.access_token = f.read()
                print(self.access_token)
                f.close()
        except Exception as e:
            print(e)

        fetch_token_url = "https://uksouth.api.cognitive.microsoft.com/sts/v1.0/issuetoken" #endpoint issued
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key}
        response = requests.post(fetch_token_url, headers=headers)
        print(response.text)
        self.access_token = str(response.text)

        with open("tts_token.txt", "w") as f:
            f.write(self.access_token)
            f.close()

    def save_audio(self, emotion):
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
        # DONE Write dialogues around this
        voice.text = choose_dialogue(emotion=emotion)
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
                with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                    audio.write(response.content)
                    try:
                        subprocess.run(["sudo", "omxplayer", "-o", "local", "sample-{0}.wav".format(self.timestr)])
                        #time.sleep(5)
                        print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
                    except Exception as e:
                        print (e)
        else:
            print("\nStatus code: " + str(response.status_code) +
              "\nSomething went wrong. Check your subscription key and headers.\n")
        # TODO Handle os.remove on deactivation

if __name__ == "__main__":
    subscription_key = "18cc0b753fa74192a6bac800febea621"
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.save_audio()

def choose_dialogue(emotion):
    dialogues = {
    'start_up': [
        "Hello, I'm " + device_name + ". I'm here to help you while having conversations"
    ],  'sadness': [
        "They’re down and low, maybe you could be the one that puts a smile on their face today!",
        "Tell them they’re not alone and that you’ll hear them out, no questions asked ",
        "Life is cold and gray sometimes, how you can be their warm sunshine today?"

    ], 'happiness':[
            "This is a really positive conversation. Well done!",
            "Your companions are really happy right now!",
            "They seem happy, ask them more about what makes them happy!"

    ], "surprise":[
            "They look surprised, ask them what did they find out?",
            "Ask them what's surprising!",
            "Something surprises them! Find out what it is!"

    ], "fear":[
            "This person is feeling fearful, maybe you could reassure them?",
            "Your companion is scared, please comfort them!",
            "They seem scared! Why don't you try and help them?"

    ], "contempt":[

            "Remind them to breathe, bottling up hate is just going to result in an explosion!",
            "Draw a picture, scream your lungs out, or just talk—which idea are you going to inspire them with today?",
            "Can you help them find the bright spots in their moments of hatred?"

    ], "disgust":[

            "The uphill is always difficult, but you’re about to go downhill soon—how can you remind them of this today?",
            "When life gives you lemons, you make some sweet lemonade— how can you be their lemonade maker today?",
            "The best way to get someone out of a “disgusted” moment is to remind them of all they're doing and how "
            "much they are valued - can you do that for someone today?"
        ],

    "anger":[

        "Anger is never good. Ask them if they'd like a glass of water and hear their concerns!",
        "They seem angry, is there something you can do to help them calm down?",
        "The best remedy to their anger is to listen calmly to their concerns and address them!"

    ],

    "neutral": [

        "There's not much you can do when someone shows no expression. Maintain eye contact!",
        "They are neutral! Listen intently and see if they'd like to discuss their feelings about the matter.",

    ], "hello": ["Hey there, got your back in this conversation, don't worry", "Hiya, don't worry, am here now to help you through this conversation"], "bye":["Well done! You did really well. Keep it up. See you soon!", "That was nicely done, you are getting better at it each day!"]}

    selected_emotion_sentence = random.choice(dialogues[emotion])

    return selected_emotion_sentence

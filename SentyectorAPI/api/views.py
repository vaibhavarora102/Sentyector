import io

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import re
import speech_recognition as sr
from sys import argv
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence


def normalization(file):
    # file = r'C:\Users\Sairish\Downloads\myrecord.wav'
    rawsound = AudioSegment.from_file(file, "wav")
    normalizedsound = effects.normalize(rawsound)
    normalizedsound.export("normalized.wav", format="wav")
    print("normalized recording saved as normalized.wav \n")
def speechToTextModule(lang="en-in"):
    song = AudioSegment.from_wav("normalized.wav")

    # spliting audio into chunks with parameter as silence of 1.2 seconds
    chunks = split_on_silence(song,
                              # must be silent for at least 1.2 seconds
                              min_silence_len=1200,
                              # consider it silent if quieter than -50 dBFS
                              silence_thresh=-50
                              )

    # creating a directory to store the audio chunks.
    try:
        os.mkdir('audio_chunks')
    except(FileExistsError):
        pass

    print("folder created for storing the chunks of audio file \n")

    os.chdir('audio_chunks')

    i = 0
    # processing  each chunk
    for chunk in chunks:
        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration=10)
        audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in the current directory.
        print("saving chunk{0}.wav".format(i))

        # specify the bitrate to be 192 k
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'chunk' + str(i) + '.wav'

        print("Processing chunk " + str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename
        # create a speech recognition object
        r = sr.Recognizer()
        # recognize the chunk
        with sr.AudioFile(file) as source:
            r.pause_threshhold = 1
            r.energy_threshold = 7000
            audio_listened = r.listen(source)
            # below could be used in case above three lines are not giving good results
            # r.adjust_for_ambient_noise(source)
            # audio_listened = r.listen(source)
        try:
            # try converting it to text by specifying the language
            rec = r.recognize_google(audio_listened, language=lang)
            # print recognised input
            return rec
            # catch any errors.
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "no internet connection or access"
        i += 1
    os.chdir('..')

@csrf_exempt
def audiototext(request):
    if (request.method == 'POST'):
        file = request.FILES.get('file')
        normalization(file)
        response = speechToTextModule()
        res = {'text': response}
        return JsonResponse(res, safe=False)


from sklearn.externals import joblib
from string import digits

model = joblib.load(open('model.pkl','rb'))
def remove_digits(s: str) -> str:
    remove_digits = str.maketrans('', '', digits)
    res = s.translate(remove_digits)
    return res

@csrf_exempt
def predemotions(request):
    if (request.method == 'POST'):
        json_data = request.body  # coming data
        stream = io.BytesIO(json_data)  # created io(input/output) stream
        textopredict = JSONParser().parse(stream)  # converted JSON to Python Data

        textopredict=textopredict['textopredict']
        textopredict = remove_digits(textopredict)
        pred = model.predict([textopredict])
        pred = {'prediction': pred[0]}
        return JsonResponse(pred, safe=False)

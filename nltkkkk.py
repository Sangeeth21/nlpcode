import asyncio
from fastapi import FastAPI
from typing import Optional
import firebase_admin
from firebase_admin import credentials, storage
import json
from pdfminer.high_level import extract_text
import os
import re
import nltk
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

nlp = spacy.load('en_core_web_sm') 

app = FastAPI()

cred = credentials.Certificate("./smarthire-285b9-firebase-adminsdk-frtth-fee212ac40.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "smarthire-285b9.appspot.com"
})

bucket = storage.bucket()
blobs = bucket.list_blobs()

for blob in blobs:
    destination_path = f"./files/{blob.name}"
    blob.download_to_filename(destination_path)
    print(f"Document downloaded from Firebase Storage and saved to {destination_path}.")

input_dir = './files'
output_dir='./output_dir'

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    if os.path.isfile(file_path):
        if file_path.lower().endswith(('.png', '.docx')):
            print(f"{filename} is not supported")
        elif file_path.lower().endswith('.pdf'):
            text = extract_text(file_path)

            stop = stopwords.words('english')
            nlp = en_core_web_sm.load()

            

            def extract_mobile_number(resume_text):
                phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)

                if phone:
                    number = ''.join(phone[0])
                    if len(number) > 10:
                        return number
                    else:
                        return number 

            mob=extract_mobile_number(text)

            data = {        
                "Mobile Number": mob,
            }

            output_file = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, output_file)
            with open(output_path, 'w') as f:
                json.dump(data, f)

            print(f"Data written to JSON file {filename}.json successfully in the output directory!")
            
app.get("/")
async def root():
    await asyncio.sleep(5)

    return {"message": "Files downloaded from Firebase Storage, information extracted from PDF files, and saved to JSON files in the output directory."}

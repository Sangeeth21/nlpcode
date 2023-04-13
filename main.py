import asyncio
from fastapi import FastAPI, BackgroundTasks
from typing import Optional
import firebase_admin
from firebase_admin import credentials, storage
from queue import Queue
import json
from pdfminer.high_level import extract_text
import os
import re
import nltk
import requests
import spacy
import en_core_web_sm
from spacy.matcher import Matcher
import re
from nltk.corpus import stopwords
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm') 
import psycopg2




app = FastAPI()

cred = credentials.Certificate("./smarthire-285b9-firebase-adminsdk-frtth-fee212ac40.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "smarthire-285b9.appspot.com"
})
bucket = storage.bucket()


async def download_files():
    queue = Queue()
    blobs = bucket.list_blobs()

    for blob in blobs:
        queue.put(blob)

    while not queue.empty():
        blob = queue.get()
        destination_path = f"./{blob.name}"
        blob.download_to_filename(destination_path)

    return {"message": f"Documents downloaded from Firebase Storage and saved to {destination_path}."}


async def exrt(filename,textinput):
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')



    nlp = en_core_web_sm.load()
    matcher = Matcher(nlp.vocab)
    def extract_name(resume_text):
        nlp_text = nlp(resume_text)
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]#proper noun
        #matcher.add('NAME', None, pattern)
        matcher.add('NAME', [pattern], on_match=None)
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text
    #print('Name:',extract_name(textinput))
    name=extract_name(textinput)



    STOPWORDS = set(stopwords.words('english'))#stopword 
    EDUCATION = [
                'BE','B.E.', 'B.E', 'BS', 'B.S', 
                'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
                'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
                'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII','Diploma in Electronics and Communication','Diploma in Computer Science','Computer science Engineering','Electronics and Electrical Engineering','Electronics and Communication engineering'
            ]


    def extract_education(resume_text):
        nlp_text = nlp(resume_text)
        #nlp_text = [sent.string.strip() for sent in nlp_text.sents]
        nlp_text = [sent.text.strip() for sent in nlp_text.sents]
        edu = {}
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education
    qualif= extract_education(textinput)


    nlp_text = nlp(textinput)
    noun_chunks = nlp_text.noun_chunks
    STOPWORDS = set(stopwords.words('english'))#stopword 
    SKILLS = [
                'Python ',' Python','Python','Java', 'C++', 'C', 'ANDROID STUDIO', 
                'HTML', 'SQL', 'FIREBASE','CSS',
            ]


    def extract_qualification(resume_text):
        nlp_text = nlp(resume_text)
        #nlp_text = [sent.string.strip() for sent in nlp_text.sents]
        nlp_text = [sent.text.strip() for sent in nlp_text.sents]
        edu = {}
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in SKILLS and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education
    #print('Skills: ',extract_qualification(textinput))
    skill= extract_qualification(textinput)


    def extract_mobile_number(resume_text):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)

        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return number
            else:
                return number 

    mob=extract_mobile_number(textinput)


    def extract_email_addresses(string):
        r = re.compile(r'[\w\.-]+@[\w\.-]+')
        return r.findall(string)
    #print('Mail id: ',extract_email_addresses(textinput))
    mail=extract_email_addresses(textinput)

    def extract_linkedin(string):
        linkedin_pattern = r"linkedin\.com\/in\/\w+[0-9-_a-zA-Z]+\/?"
        linkedin_url = re.findall(linkedin_pattern,string)
        return linkedin_url
    lin=extract_linkedin(textinput)



    def extract_github(string):
        github_pattern_1 = r"github\.com\/\w+[0-9-_a-zA-Z]+\/?"
        github_pattern_2 = r"\w+[0-9-_a-zA-Z]\s\(+github\.com\)?"
        github_pattern_3 = r"\w+\s+\(github\.com\)"
    
        if re.search(github_pattern_1, string):
            github_url = re.findall(github_pattern_1, string)
            return github_url
        elif re.search(github_pattern_2, string):
            github_url = re.findall(github_pattern_2, string)
            return github_url
        elif re.search(github_pattern_3, string):
            github_url = re.findall(github_pattern_3, string)
            return github_url
        else:
            return None

    git=extract_github(textinput)
    

    data = {
        "Name": name,
        "Qualification": qualif,
        "Skills":skill,
        "Mobile Number": mob,
        "Mail id":mail,
        "Linkedin":lin,
        "Github":git
    }

    output_dir='./output_dir'
    output_file = os.path.splitext(filename)[0] + ".json"
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        json.dump(data, f)

    print(f"Data written to JSON file {filename}.json successfully in the output directory!")

def pdftotext(filename):
    text = extract_text(filename)
    return text

input_dir = './files'
input_dir1='./jr_engineer'
input_dir2='./senior_engineer'





async def process():
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if os.path.isfile(file_path):
            if file_path.lower().endswith(('.png', '.docx')):
                print(f"{filename} is not supported")
            elif file_path.lower().endswith('.pdf'):
                textinput = pdftotext(file_path)
                await exrt(filename,textinput)

async def process1():
    for filename in os.listdir(input_dir1):
        file_path = os.path.join(input_dir1, filename)
        if os.path.isfile(file_path):
            if file_path.lower().endswith(('.png', '.docx')):
                print(f"{filename} is not supported")
            elif file_path.lower().endswith('.pdf'):
                textinput = pdftotext(file_path)
                await exrt(filename,textinput)

async def process2():
    for filename in os.listdir(input_dir2):
        file_path = os.path.join(input_dir2, filename)
        if os.path.isfile(file_path):
            if file_path.lower().endswith(('.png', '.docx')):
                print(f"{filename} is not supported")
            elif file_path.lower().endswith('.pdf'):
                textinput = pdftotext(file_path)
                await exrt(filename,textinput)







async def matching():
 with open('./HR/hr.json', 'r') as f:
    # Load the contents of the file as a string
    json_string = f.read()

# Parse the JSON string into a dictionary
 hr_dict = json.loads(json_string)


 folder_path = "./output_dir"
 for filename in os.listdir(folder_path):
    score = 0
    if filename.endswith(".json"):
        # Load the JSON data from the file
        filepath = os.path.join(folder_path, filename)
        with open(filepath) as f:
            json_string = f.read()
        candidate_dict = json.loads(json_string)
        for key in hr_dict:
            if key in candidate_dict:
                for element in candidate_dict[key]:
                    if element.upper() in hr_dict[key]:
                        score += 1
        candidate_dict["Score"] = score


    output_dir='./output_dir'
    output_file = os.path.splitext(filename)[0] + ".json"
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        json.dump(candidate_dict, f)




async def gitfetch():
    folder_path = "./output_dir"
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            # Load the JSON data from the file
            filepath = os.path.join(folder_path, filename)
            with open(filepath) as f:
                json_string = f.read()
            git_data = json.loads(json_string)
            if git_data.get("Github"):  # use get() method to avoid NoneType error
                github_url = git_data["Github"][0]
                if "(" in github_url and ")" in github_url:
                    # Extract username from {username} (github.com) format
                    github_username = github_url.split("(")[0].strip()
                else:
                    github_username = github_url.split("/")[-1]
                url = "http://localhost:5000/repos/{}".format(github_username)
                response = requests.get(url)
                if response.status_code == 200:
                    results.append(response.json())
                else:
                    results.append({"message": "Error fetching data from Flask app"})
    return results



async def postgre():
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="sangeeth")

# Open a cursor to execute SQL commands
    cur = conn.cursor()

# Loop through each JSON file in the folder
    folder_path = "./output_dir"
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
        # Load the JSON data from the file
            filepath = os.path.join(folder_path, filename)
            with open(filepath) as f:
                data = json.load(f)
        
        # Extract the relevant key-value pairs
            name = data.get("Name")
            qualifications = data.get("Qualification")
            skills = data.get("Skills")
            mobile_number = data.get("Mobile Number")
            mail_ids = data.get("Mail id")
            github = data.get("Github")
            linkedin = data.get("Linkedin")            
            scores = data.get("Score")

        
        # Check if a record with the same name or mobile number already exists
            cur.execute("SELECT * FROM shire WHERE name=%s OR mobile_number=%s", (name, mobile_number))
            existing_record = cur.fetchone()
            if existing_record:
                print(f"Skipping {filename} as record already exists in the database.")
                continue
        
        # Insert the data into the PostgreSQL table
            cur.execute("INSERT INTO shire (name, qualifications, skills, mobile_number, mail_ids,github,linkedin,scores) VALUES (%s, %s, %s, %s, %s,%s,%s, %s)" , (name, qualifications, skills, mobile_number, mail_ids,github,linkedin,scores))
            print(f"Inserted {filename} into the database.")
        
# Commit the changes to the database
    conn.commit()

# Close the cursor and database connection
    cur.close()
    conn.close()
    print("Data insertion complete!")







@app.get("/")
async def main():
    folders_to_check = ["./senior_engineer", "./jr_engineer","./files"]
    last_files = {folder: set() for folder in folders_to_check}
    while True:
        for folder in folders_to_check:
            await download_files()
            current_files = set(os.listdir(folder))
            new_files = current_files - last_files[folder]
            if new_files:
                await process()
                await process1()
                await process2()
                await matching()
                await gitfetch()
                await postgre()
                last_files[folder] = current_files
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

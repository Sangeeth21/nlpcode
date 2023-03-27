



# import firebase_admin
# from firebase_admin import credentials, storage

# cred = credentials.Certificate("./smarthire-285b9-firebase-adminsdk-frtth-fee212ac40.json")
# firebase_admin.initialize_app(cred, {
#     "storageBucket": "smarthire-285b9.appspot.com"
# })

# bucket = storage.bucket()
# from queue import Queue

# queue = Queue()
# blobs = bucket.list_blobs()

# for blob in blobs:
#     queue.put(blob)

# while not queue.empty():
#     blob = queue.get()
#     destination_path = f"./{blob.name}"
#     blob.download_to_filename(destination_path)

# print(f'Document downloaded from Firebase Storage and saved to {destination_path}.')






# from fastapi import FastAPI
# from firebase_admin import credentials, storage
# from queue import Queue

# app = FastAPI()

# cred = credentials.Certificate("./smarthire-285b9-firebase-adminsdk-frtth-fee212ac40.json")
# firebase_admin.initialize_app(cred, {
#     "storageBucket": "smarthire-285b9.appspot.com"
# })

# bucket = storage.bucket()
# queue = Queue()
# blobs = bucket.list_blobs()

# for blob in blobs:
#     queue.put(blob)

# while not queue.empty():
#     blob = queue.get()
#     destination_path = f"./{blob.name}"
#     blob.download_to_filename(destination_path)

#     print(f"Document downloaded from Firebase Storage and saved to {destination_path}.")


# @app.get("/download_from_firebase")
# async def download_from_firebase():
#     return {"message": "Documents downloaded from Firebase Storage and saved locally."}




import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate("credentials.json")

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'audiorec-f1ad6.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
# for name in bucket.list_blobs():
#     print(name)

blob = bucket.blob('myfile.wav')
# print(type(blob))
blob.download_to_filename('file.wav')
#print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
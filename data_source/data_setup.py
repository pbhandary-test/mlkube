import shutil
import os ,io
import zipfile  
import pathlib
import json 
import sys
from google.cloud import storage
from google.oauth2 import service_account
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.exception import CustomException

def import_json(file_name):
    with open(file_name, "r") as f:
        json_data = json.load(f)
    return json_data


def delete_file(filename):
  """Deletes the file with the given filename."""
  if os.path.exists(filename):
    os.remove(filename)
  else:
    print(f"File '{filename}' does not exist.")


print (os.path.abspath("./environ_secrets.json"))
json_file = import_json( (os.path.abspath("./environ_secrets.json")))

GCP_PROJECT_ID = json_file.get("GCP_PROJECT_ID")
SERVICE_ACCOUNT_FILE = json_file.get("SERVICE_ACCOUNT_FILE")
zip_file_path = json_file.get("zip_file_path")
TARGET_DIRECTORY = json_file.get("TARGET_DIRECTORY")
BUCKET_NAME = json_file.get("BUCKET_NAME")
object_name = json_file.get("object_name")
directory = json_file.get("directory")
archive_file = json_file.get("archive_file")


print(SERVICE_ACCOUNT_FILE)

category_dict = {1:"Normal",
2:"glioma_tumor",
3:"meningioma_tumor",
4:"pituitary_tumor"}


credentials = service_account.Credentials.from_service_account_file(os.path.join("./",SERVICE_ACCOUNT_FILE))


client = storage.Client(
    project=GCP_PROJECT_ID,
    credentials=credentials
)

bucket = client.bucket(BUCKET_NAME)
blob = storage.Blob(object_name, bucket)
object_bytes = blob.download_as_bytes()
archive = io.BytesIO()
archive.write(object_bytes)

with open(object_name, 'wb') as file:
    file.write(archive.getvalue())
    
for _,dir_ in category_dict.items():
    new_dir = TARGET_DIRECTORY + directory + "/" + dir_
    if not os.path.exists(new_dir):
            os.makedirs(new_dir)   
            
def directory_check(directory,filename):
    if f"{category_dict[1]}" in filename:
        return f"{directory}/{category_dict[1]}"
    elif f"{category_dict[2]}" in filename:
        return f"{directory}/{category_dict[2]}"
    elif f"{category_dict[3]}" in filename :
        return f"{directory}/{category_dict[3]}"
    elif f"{category_dict[4]}" in filename :
        return f"{directory}/{category_dict[4]}"


with zipfile.ZipFile(archive_file, "r") as zip_file:
    for member in zip_file.namelist():
        try: 
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
            # get the directory name
            my_dir = directory_check(directory,member)
            source = zip_file.open(member)
            print(os.path.join(my_dir, filename))
            target = open(os.path.join(TARGET_DIRECTORY,my_dir, filename), "wb")

            with source, target:
                shutil.copyfileobj(source, target)
                
        except Exception as e:
            raise CustomException(e,sys)
        

delete_file(archive_file)

import shutil
import os ,io
import zipfile  
import pathlib
from google.cloud import storage
from google.oauth2 import service_account


GCP_PROJECT_ID = GCP_PROJECT_ID
SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE
zip_file_path = SERVICE_ACCOUNT_FILE
TARGET_DIRECTORY = SERVICE_ACCOUNT_FILE
BUCKET_NAME = BUCKET_NAME
object_name = 'archive_1.zip'
directory = "Data"

category_dict = {1:"Normal",
2:"glioma_tumor",
3:"meningioma_tumor",
4:"pituitary_tumor"}


credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

client = storage.Client(
    project=GCP_PROJECT_ID,
    credentials=credentials
)

target_dir = pathlib.Path(TARGET_DIRECTORY)
bucket = client.bucket(BUCKET_NAME)
blob = storage.Blob(object_name, bucket)
object_bytes = blob.download_as_bytes()
archive = io.BytesIO()
archive.write(object_bytes)

with open(object_name, 'wb') as file:
    file.write(archive.getvalue())
    
for _,dir_ in category_dict.items():
    new_dir = directory + "/" + dir_
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


with zipfile.ZipFile("archive_1.zip", "r") as zip_file:
        for member in zip_file.namelist():
            try: 
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue
                # get the directory name
                my_dir = directory_check(directory,member)
                source = zip_file.open(member)
                target = open(os.path.join(my_dir, filename), "wb")

                with source, target:
                    shutil.copyfileobj(source, target)
            except:
                print(filename +" [] "+ member)

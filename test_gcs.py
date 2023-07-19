
import logging
from google.cloud import storage
import json

bucket_name = 'detect_udem'

client = storage.Client()

bucket = client.get_bucket(bucket_name)

gsuri_info = []


for blob in bucket.list_blobs():
    # print( blob.name )
    if (blob.name.endswith('.jpg') or blob.name.endswith('.png') ):
        if ("/Corrosion/"  in blob.name )or ("/no-corrosion/" in blob.name)  :
            displayName= "Corrosion" if "/Corrosion/" in blob.name else "NoCorrosion" 
            gsuri = blob.name.split('/')[0]  
            # print(gsuri)
            if "/train" in blob.name :
                dataItemResourceLabels= "training"
            elif "/test" in blob.name:
                dataItemResourceLabels = "test"
            elif "/validate" in blob.name:
                dataItemResourceLabels = "validation"
            else:
                dataItemResourceLabels= None

            line = {"imageGcsUri": f'gs://{bucket_name}/{blob.name}', 
            "classificationAnnotation": {"displayName": displayName}, 
            "dataItemResourceLabels": {"aiplatform.googleapis.com/ml_use": dataItemResourceLabels}}
            print(line)
            if  dataItemResourceLabels != None:
                gsuri_info.append(line) 
        
# print(gsuri_info)
# Save the gsuri information to a JSON file
output_file = 'gsuri_info.json'
with open(output_file, 'w') as f:
    json.dump(gsuri_info, f, indent=4)



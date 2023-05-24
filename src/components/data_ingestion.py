import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

CSV_NOTEBOOK_PATH =''
TEST_SIZE = 0.25
RANDOM_STATE = 42

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifact','data.csv')
    train_data_path: str = os.path.join('artifact','train.csv')
    test_data_path: str = os.path.join('artifact','test.csv')
    

class DataIngestion:
    def __init__ (self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Data ingestion method initiated")

        try:
            df = pd.read_csv(CSV_NOTEBOOK_PATH) 
            logging.info ('read the dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            #os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)            
            df.to_csv(os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True))
            
            train_set , test_set =train_test_split(df , test_size = TEST_SIZE , random_state = RANDOM_STATE) 
            train_set.to_csv(self.ingestion_config.train_data_path,index=false,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=false,header=True)
            
            logging.info("ingestion completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    obj= DataIngestion()
    train_set , test_set  = obj.initiate_data_ingestion()

#TODO set DataTransformation before train_test split 
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

#TODO set ModelTrainer after train_test split  
    modeltrainer = ModelTrainer()

    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    


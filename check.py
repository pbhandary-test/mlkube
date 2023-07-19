import os
from google.cloud import aiplatform
import atexit
os.fork()
from multiprocessing import Pool
pool = Pool(1)
atexit.register(pool.close)
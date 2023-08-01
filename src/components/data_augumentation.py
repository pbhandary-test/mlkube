import os
import tensorflow as tf


input_types = ["BR", "DA" ,"HF" , "n" ,"RO","SP" ,"VF"]

base_dir = "../data_source/Data/"

input_shape = (150,150,3)

batch_size=32

train_datagen = ImageDataGenerator(
    rescale =1.0 /255.0,
    #other parama
)

val_datagen = ImageDataGenerator(
    rescale =1.0/255.0
)

test_datagen = ImageDataGenerator(
    rescale =1.0/255.0
)

train_generator = train_datagen.flow_from_directory(
    os.path.join(base_dir, "train"),
    target_size = input_shape[:2],
    batch_size = batch_size,
    class_mode = 'categorical',
    shuffle =False,
    classes = input_types
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(base_dir, "train"),
    target_size = input_shape[:2],
    batch_size = batch_size,
    class_mode = 'categorical',
    shuffle =False,
    classes = input_types
)

test_generator = test_datagen.flow_from_directory(
    os.path.join(base_dir, "train"),
    target_size = input_shape[:2],
    batch_size = batch_size,
    class_mode = 'categorical',
    shuffle =False,
    classes = input_types
)


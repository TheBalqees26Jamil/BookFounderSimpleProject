# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
# from tensorflow.keras.models import Model
# from tensorflow.keras.optimizers import Adam
#
#
# IMG_SIZE = 128
# BATCH_SIZE = 8
# EPOCHS = 11
#
# TRAIN_DIR = "dataset/train"
# VAL_DIR = "dataset/val"
#
#
# train_gen = ImageDataGenerator(
#     rescale=1./255,
#     rotation_range=15,
#     zoom_range=0.15,
#     width_shift_range=0.1,
#     height_shift_range=0.1,
#     brightness_range=[0.7, 1.3],
#     horizontal_flip=True
# )
#
# val_gen = ImageDataGenerator(rescale=1./255)
#
# train_data = train_gen.flow_from_directory(
#     TRAIN_DIR,
#     target_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     class_mode="binary",
#     shuffle=True
# )
#
# val_data = val_gen.flow_from_directory(
#     VAL_DIR,
#     target_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     class_mode="binary",
#     shuffle=False
# )
#
#
# base_model = MobileNetV2(
#     weights="imagenet",
#     include_top=False,
#     input_shape=(IMG_SIZE, IMG_SIZE, 3)
# )
#
#
# for layer in base_model.layers:
#     layer.trainable = False
#
#
# x = GlobalAveragePooling2D()(base_model.output)
# x = Dropout(0.4)(x)
# x = Dense(64, activation="relu")(x)
# x = Dropout(0.4)(x)
# output = Dense(1, activation="sigmoid")(x)
#
# model = Model(inputs=base_model.input, outputs=output)
#
#
# model.compile(
#     optimizer=Adam(learning_rate=1e-4),
#     loss="binary_crossentropy",
#     metrics=["accuracy"]
# )
#
# model.summary()
#
#
# history = model.fit(
#     train_data,
#     validation_data=val_data,
#     epochs=EPOCHS
# )
#
#
# train_loss, train_acc = model.evaluate(train_data, verbose=0)
# val_loss, val_acc = model.evaluate(val_data, verbose=0)
#
# print("\n📊 الدقة النهائية:")
# print(f"Training Accuracy : {train_acc * 100:.2f}%")
# print(f"Validation Accuracy: {val_acc * 100:.2f}%")
#
#
# model.save("book_nobook_mobilenetv2_11Ep.h5")

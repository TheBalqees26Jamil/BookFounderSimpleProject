# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import load_model
#
# # حملي نفس الموديل المرتبط بالواجهة
# model = load_model("book_nobook_mobilenetv2_11Ep.h5")
#
# # إعداد test generator
# test_datagen = ImageDataGenerator(rescale=1./255)
#
# test_generator = test_datagen.flow_from_directory(
#     "dataset/test",     # ← عدلي المسار حسب عندك
#     target_size=(128, 128),
#     batch_size=32,
#     class_mode="binary",
#     shuffle=False
# )
#
# # التقييم
# loss, accuracy = model.evaluate(test_generator)
#
# print(f"Test Accuracy: {accuracy * 100:.2f}%")
# print(f"Test Loss: {loss:.4f}")

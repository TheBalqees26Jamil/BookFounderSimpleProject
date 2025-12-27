# BookFounderSimpleProject

📚 Book Detection Project

(Book / NoBook Classification using Deep Learning)

____________________


🔹 Project Overview | 

This project is a Book Detection system that classifies images into two categories:

Book

NoBook

The system uses a Deep Learning model (MobileNetV2) trained on images and integrated with a PyQt6 graphical user interface.
Users can test the model either by loading an image or by using the camera.


______________________

🔹 Technologies Used | 

Python

TensorFlow / Keras

MobileNetV2

OpenCV

PyQt6

NumPy

____________________


🔹 Model Details | 

Model: MobileNetV2

Image Size: 128 × 128

Classes:

Book

NoBook

Accuracy on Test Data: ~90%+

The model shows high accuracy on static images.
Performance may slightly decrease with live camera input due to lighting, motion blur, and camera quality.

____________________

🔹 Application Features | 

Simple and clean graphical interface

Image upload and prediction

Camera capture with multiple-frame averaging

Automatic image preprocessing

Real-time prediction result display

_____________________

🔹 How to Run |

1️⃣ Install requirements:

pip install tensorflow opencv-python pyqt6 numpy

2️⃣ Run the application:

python main.py

___________________

🔹 Project Structure:

```
Bookfounder/
│
├── dataset/
    ├── train/
        ├── Book/
        └── NoBook/ 
    └── val/
       ├── Book/
       └── NoBook/
├── book_nobook_mobilenetv2_11Ep.h5
├── Brown_Natural.mp4
├── Evaluate.py
├── main.py
├── Model.py


```

_______________________

🔹 Notes | 

The model performs best with clear images and good lighting.

Camera-based prediction may vary due to environmental factors.

This behavior is normal in computer vision applications.

________________________

نظرة عامة |


هذا المشروع عبارة عن نظام تصنيف صور يحدد ما إذا كانت الصورة تحتوي على كتاب أو لا تحتوي على كتاب.
تم تدريب موديل تعلم عميق باستخدام MobileNetV2 وربطه بواجهة رسومية باستخدام PyQt6، مع إمكانية الاختبار عن طريق:

تحميل صورة

أو التقاط صورة من الكاميرا
____________________



التقنيات المستخدمة |

Python

TensorFlow / Keras

MobileNetV2

OpenCV

PyQt6

NumPy 
_________________


مميزات التطبيق | 

واجهة سهلة وبسيطة

تصنيف الصور عند التحميل

دعم الكاميرا مع تحسين التنبؤ باستخدام عدة إطارات

معالجة تلقائية للصورة

عرض النتيجة مباشرة داخل الواجهة

_______________________




ملاحظات |


أفضل أداء يكون مع صور واضحة وإضاءة جيدة

نتائج الكاميرا قد تختلف بسبب العوامل البيئية

هذا أمر طبيعي في تطبيقات الرؤية الحاسوبية 

____________________________















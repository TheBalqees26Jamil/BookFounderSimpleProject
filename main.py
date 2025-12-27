import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


model = load_model("book_nobook_mobilenetv2_11Ep.h5")
class_labels = {1: "There is NoBook", 0: "This is a Book"}

class BookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Detection")
        self.setGeometry(200, 100, 500, 800)


        self.result_label = QLabel(self)
        self.result_label.setGeometry(50, 20, 400, 80)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 20px;
        """)


        self.capture_btn = QPushButton("Capture", self)
        self.capture_btn.setGeometry(100, 650, 120, 50)
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """)
        self.capture_btn.clicked.connect(self.capture_image)

        self.load_btn = QPushButton("Load Image", self)
        self.load_btn.setGeometry(280, 650, 120, 50)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """)
        self.load_btn.clicked.connect(self.load_image)


        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 500, 800)
        self.video_label.lower()


        self.cap = cv2.VideoCapture("Brown_Neutral.mp4")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)


    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return
        frame = cv2.resize(frame, (500, 800))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(image)
        self.video_label.setPixmap(pix)


    def preprocess_image(self, image):
        image = cv2.resize(image, (128, 128))
        image = img_to_array(image)
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    def extract_book_roi(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            roi = image[y:y+h, x:x+w]
            return roi
        else:
            return image

    def predict_image(self, image):
        roi = self.extract_book_roi(image)
        processed = self.preprocess_image(roi)
        prediction = model.predict(processed)[0][0]
        print("Confidence:", prediction)
        label = class_labels[int(round(prediction))]
        self.result_label.setText(label)

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.result_label.setText("Failed to open camera")
            return
        predictions = []
        for _ in range(15):
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = self.extract_book_roi(frame_rgb)
            processed = self.preprocess_image(roi)
            pred = model.predict(processed)[0][0]
            predictions.append(pred)
        cap.release()
        cv2.destroyAllWindows()
        if predictions:
            avg_pred = np.mean(predictions)
            print("Average Confidence:", avg_pred)
            label = class_labels[int(round(avg_pred))]
            self.result_label.setText(label)
        else:
            self.result_label.setText("Failed to capture image")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            image = cv2.imread(file_name)
            if image is not None:
                image = cv2.convertScaleAbs(image, alpha=1.2, beta=20)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.predict_image(image)
            else:
                self.result_label.setText("Failed to load image")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec())















# import sys
# import cv2
# import numpy as np
# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
# from PyQt6.QtGui import QPixmap, QImage
# from PyQt6.QtCore import Qt
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array
#
# # تحميل الموديل المحفوظ
# model = load_model("book_nobook_mobilenetv2_11Ep.h5")
#
# # القيم المطلوبة لتحويل النتيجة إلى نص
# class_labels = {1: "This is NoBook", 0: "This is a Book"}
#
#
# class BookApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Book Detection")
#         self.setGeometry(200, 100, 500, 800)
#
#         # QLabel لعرض النتيجة
#         self.result_label = QLabel(self)
#         self.result_label.setGeometry(50, 20, 400, 80)
#         self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.result_label.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: white;
#             background-color: rgba(0, 0, 0, 0.5);
#             border-radius: 20px;
#         """)
#
#         # زر Capture
#         self.capture_btn = QPushButton("Capture", self)
#         self.capture_btn.setGeometry(100, 650, 120, 50)
#         self.capture_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border-radius: 20px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#         """)
#         self.capture_btn.clicked.connect(self.capture_image)
#
#         # زر Load Image
#         self.load_btn = QPushButton("Load Image", self)
#         self.load_btn.setGeometry(280, 650, 120, 50)
#         self.load_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #2196F3;
#                 color: white;
#                 border-radius: 20px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #0b7dda;
#             }
#         """)
#         self.load_btn.clicked.connect(self.load_image)
#
#     def preprocess_image(self, image):
#         image = cv2.resize(image, (128, 128))
#         image = img_to_array(image)
#         image = image / 255.0
#         image = np.expand_dims(image, axis=0)
#         return image
#
#     def extract_book_roi(self, image):
#         """
#         استخراج أكبر جسم محتمل للكتاب من الصورة (ROI)
#         """
#         gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if contours:
#             # أكبر contour
#             c = max(contours, key=cv2.contourArea)
#             x, y, w, h = cv2.boundingRect(c)
#             roi = image[y:y+h, x:x+w]
#             return roi
#         else:
#             return image  # إذا لم يوجد شيء، استخدم الصورة كاملة
#
#     def predict_image(self, image):
#         roi = self.extract_book_roi(image)  # استخدم ROI
#         processed = self.preprocess_image(roi)
#         prediction = model.predict(processed)[0][0]
#
#         print("Confidence:", prediction)
#
#         label = class_labels[int(round(prediction))]
#         self.result_label.setText(label)
#
#     def capture_image(self):
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             self.result_label.setText("Failed to open camera")
#             return
#
#         predictions = []
#         num_frames = 15  # عدد الإطارات للمعدل
#
#         for i in range(num_frames):
#             ret, frame = cap.read()
#             if not ret:
#                 continue
#
#             # تحسين الإضاءة والتباين
#             frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#             roi = self.extract_book_roi(frame_rgb)
#             processed = self.preprocess_image(roi)
#             pred = model.predict(processed)[0][0]
#             predictions.append(pred)
#
#         cap.release()
#         cv2.destroyAllWindows()
#
#         if predictions:
#             avg_pred = np.mean(predictions)
#             print("Average Confidence:", avg_pred)
#             label = class_labels[int(round(avg_pred))]
#             self.result_label.setText(label)
#         else:
#             self.result_label.setText("Failed to capture image")
#
#     def load_image(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
#         if file_name:
#             image = cv2.imread(file_name)
#             if image is not None:
#                 image = cv2.convertScaleAbs(image, alpha=1.2, beta=20)
#                 image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#                 self.predict_image(image)
#             else:
#                 self.result_label.setText("Failed to load image")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = BookApp()
#     window.show()
#     sys.exit(app.exec())
#
#
#
#
#
#
#
#
#
#
#
















# import sys
# import cv2
# import numpy as np
# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
# from PyQt6.QtGui import QPixmap, QImage
# from PyQt6.QtCore import Qt
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import img_to_array
#
# # تحميل الموديل المحفوظ
# model = load_model("book_nobook_mobilenetv2_11Ep.h5")
#
# # القيم المطلوبة لتحويل النتيجة إلى نص
# class_labels = {1: "This is NoBook", 0: "This is a Book"}
#
#
# class BookApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Book Detection")
#         self.setGeometry(200, 100, 500, 800)  # نافذة طولية
#
#         # QLabel لعرض النتيجة
#         self.result_label = QLabel(self)
#         self.result_label.setGeometry(50, 20, 400, 80)
#         self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.result_label.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: white;
#             background-color: rgba(0, 0, 0, 0.5);
#             border-radius: 20px;
#         """)
#
#         # زر Capture
#         self.capture_btn = QPushButton("Capture", self)
#         self.capture_btn.setGeometry(100, 650, 120, 50)
#         self.capture_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border-radius: 20px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#         """)
#         self.capture_btn.clicked.connect(self.capture_image)
#
#         # زر Load Image
#         self.load_btn = QPushButton("Load Image", self)
#         self.load_btn.setGeometry(280, 650, 120, 50)
#         self.load_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #2196F3;
#                 color: white;
#                 border-radius: 20px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #0b7dda;
#             }
#         """)
#         self.load_btn.clicked.connect(self.load_image)
#
#     def preprocess_image(self, image):
#         image = cv2.resize(image, (128, 128))  # نفس حجم التدريب
#         image = img_to_array(image)
#         image = image / 255.0
#         image = np.expand_dims(image, axis=0)
#         return image
#
#     def predict_image(self, image):
#         processed = self.preprocess_image(image)
#         prediction = model.predict(processed)[0][0]
#
#         # طباعة قيمة الثقة
#         print("Confidence:", prediction)
#
#         # تحويل التنبؤ إلى تصنيف
#         label = class_labels[int(round(prediction))]
#         self.result_label.setText(label)
#
#     def capture_image(self):
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             self.result_label.setText("Failed to open camera")
#             return
#
#         predictions = []
#         num_frames = 10  # عدد الإطارات للمعدل
#
#         for i in range(num_frames):
#             ret, frame = cap.read()
#             if not ret:
#                 continue
#             # تحويل BGR → RGB
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             processed = self.preprocess_image(frame_rgb)
#             pred = model.predict(processed)[0][0]
#             predictions.append(pred)
#
#         cap.release()
#         cv2.destroyAllWindows()
#
#         if predictions:
#             avg_pred = np.mean(predictions)
#             print("Average Confidence:", avg_pred)
#             label = class_labels[int(round(avg_pred))]
#             self.result_label.setText(label)
#         else:
#             self.result_label.setText("Failed to capture image")
#
#     def load_image(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
#         if file_name:
#             image = cv2.imread(file_name)
#             if image is not None:
#                 # تحويل BGR إلى RGB
#                 image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#                 self.predict_image(image)
#             else:
#                 self.result_label.setText("Failed to load image")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = BookApp()
#     window.show()
#     sys.exit(app.exec())
#
#
#
#
# # import sys
# # import cv2
# # import numpy as np
# # from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
# # from PyQt6.QtGui import QPixmap, QImage
# # from PyQt6.QtCore import Qt
# # from tensorflow.keras.models import load_model
# # from tensorflow.keras.preprocessing.image import img_to_array
# #
# # # تحميل الموديل المحفوظ
# # model = load_model("book_nobook_mobilenetv2_11Ep.h5")
# #
# # # القيم المطلوبة لتغيير النتيجة إلى نص
# # class_labels = {0: "This is NoBook", 1: "This is a Book"}
# # #
# # class BookApp(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Book Detection")
# #         self.setGeometry(200, 100, 500, 800)  # نافذة طولية
# #
# #         # QLabel لعرض النتيجة
# #         self.result_label = QLabel(self)
# #         self.result_label.setGeometry(50, 20, 400, 80)
# #         self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
# #         self.result_label.setStyleSheet("""
# #             font-size: 24px;
# #             font-weight: bold;
# #             color: white;
# #             background-color: rgba(0, 0, 0, 0.5);
# #             border-radius: 20px;
# #         """)
# #
# #         # زر Capture
# #         self.capture_btn = QPushButton("Capture", self)
# #         self.capture_btn.setGeometry(100, 650, 120, 50)
# #         self.capture_btn.setStyleSheet("""
# #             QPushButton {
# #                 background-color: #4CAF50;
# #                 color: white;
# #                 border-radius: 20px;
# #                 font-size: 16px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #45a049;
# #             }
# #         """)
# #         self.capture_btn.clicked.connect(self.capture_image)
# #
# #         # زر Load Image
# #         self.load_btn = QPushButton("Load Image", self)
# #         self.load_btn.setGeometry(280, 650, 120, 50)
# #         self.load_btn.setStyleSheet("""
# #             QPushButton {
# #                 background-color: #2196F3;
# #                 color: white;
# #                 border-radius: 20px;
# #                 font-size: 16px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #0b7dda;
# #             }
# #         """)
# #         self.load_btn.clicked.connect(self.load_image)
# #
# #     def preprocess_image(self, image):
# #         image = cv2.resize(image, (128, 128))  # نفس حجم التدريب
# #         image = img_to_array(image)
# #         image = image / 255.0
# #         image = np.expand_dims(image, axis=0)
# #         return image
# #
# #     def predict_image(self, image):
# #         processed = self.preprocess_image(image)
# #         prediction = model.predict(processed)[0][0]
# #
# #         # تحويل التنبؤ إلى تصنيف
# #         label = class_labels[int(round(prediction))]
# #         self.result_label.setText(label)
# #
# #     def capture_image(self):
# #         cap = cv2.VideoCapture(0)
# #         ret, frame = cap.read()
# #         if ret:
# #             cap.release()
# #             cv2.destroyAllWindows()
# #             self.predict_image(frame)
# #         else:
# #             self.result_label.setText("Failed to open camera")
# #             cap.release()
# #
# #     def load_image(self):
# #         file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
# #         if file_name:
# #             image = cv2.imread(file_name)
# #             self.predict_image(image)
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = BookApp()
# #     window.show()
# #     sys.exit(app.exec())

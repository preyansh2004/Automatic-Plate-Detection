# 🚘 Automatic Plate Detection (PlateDetect)

An AI-powered Automatic Number Plate Recognition (ANPR) system built using Python and Streamlit. This project allows users to upload video footage, automatically detect vehicles and license plates using YOLO object detection, and extract text using advanced OCR technology.

## ✨ Key Features

* **AI-Powered Detection:** Utilizes advanced deep learning models (YOLOv8) trained on millions of plates for superior recognition accuracy.
* **Text Extraction:** Integrates Optical Character Recognition (OCR) to read and output the alphanumeric characters from detected plates.
* **Interactive UI:** Features a modern, user-friendly web interface built with Streamlit, complete with upload capabilities and processing progress tracking.
* **Visual Output:** Generates and downloads beautifully annotated videos with highlighted detected plates and bounding boxes overlaid in real-time.

## 🛠️ Technologies Used

* **Frontend:** Streamlit (Python web framework), HTML/CSS (Custom styling)
* **Computer Vision:** YOLOv8 (Ultralytics), OpenCV
* **OCR:** EasyOCR / Tesseract
* **Language:** Python 3.x

## 🚀 Setup & Usage

1. Clone the repository:
```bash
git clone https://github.com/preyansh2004/Automatic-Plate-Detection.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```
4. Open the provided localhost URL in your web browser, upload a .mp4 video, and click "Start Detection".

## 📄 License
This project is open-source and available for educational purposes.

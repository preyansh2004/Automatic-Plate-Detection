from ultralytics import YOLO
import cv2
import numpy as np
from sort.sort import Sort
from util import get_car, read_license_plate, write_csv

results = {}
mot_tracker = Sort() # to remember the same car in every frame

# Load models
coco_model = YOLO('yolov8n.pt')    #pre-trained model to detect vehciles like car,bus,truck,motorbike
license_plate_detector = YOLO('best.pt')  # pre-trained model knows what a license plate looks like.

# Load video
cap = cv2.VideoCapture('sample.mp4')

vehicles = [2, 3, 5, 7]

# read frames
frame_nmr = -1
ret = True
print("Starting video processing...")

while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}
        # detect vehicles
        detections = coco_model(frame)[0]          # results = coco_model(frame) returns list of images but we want single image so [0]
        detections_ = []
        for detection in detections.boxes.data.tolist(): #detections.boxes.data returns 2D array so convert to python list
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:      # class id means it tells whether it is a car or not in every frame
                detections_.append([x1, y1, x2, y2, score])

        # track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_)) # it assigns track id where the above class_id just gives that this is car or bus or truck but this creates id for same car

        # detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:
                # crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]  #frame[y1:y2 vertical slice (top to bottom), x1:x2 horizontal slice (left to right), : all color channels (BGR)]

                # process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score}}
    
        if frame_nmr % 50 == 0:
            print(f"Processed frame {frame_nmr}")

        cv2.imshow('PlateDetect Live View', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    else:
        break

# write results
write_csv(results, './test.csv')
print("Done! test.csv created.")
cap.release()
cv2.destroyAllWindows()
import os
from array import array

import cv2
import numpy as np

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(os.path.join(os.getcwd(), 'media', 'models', 'classifier.yml'))
class_names = ['160770107542', '160770107543', '160770107541', '160770107549']


def modify_input_for_multiple_files(property_id, branch, class_str, image):
    dict = {}
    dict['property_id'] = property_id
    dict['branch'] = branch
    dict['class_str'] = class_str
    dict['image'] = image
    return dict


def image_classifier():
    cwd = os.getcwd()
    output_dictionary = []
    for class_name in os.listdir(os.path.join(cwd, 'media', 'images')):
        for div_name in os.listdir(os.path.join(cwd, 'media', 'images', class_name)):
            for picture_name in os.listdir(os.path.join(cwd, 'media', 'images', class_name, div_name)):
                predicted_class = class_names[recognize(class_name, div_name, picture_name)[0]]
                output_dictionary.append({
                    'class_name': class_name,
                    'div_name': div_name,
                    'picture_name': picture_name,
                    'predicted_enroll_no': predicted_class
                })
    return output_dictionary


def recognize(class_name, div_name, picture_name):
    return face_recognizer.predict(
        cv2.imread(
            os.path.join(os.getcwd(), 'media', 'images', class_name, div_name, picture_name),
            cv2.IMREAD_GRAYSCALE
        )
    )

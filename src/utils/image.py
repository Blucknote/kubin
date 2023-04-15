import numpy
import requests
import base64
from gradio.processing_utils import decode_base64_to_image
import base64
from PIL import Image
from io import BytesIO
import cv2

def imagePathToPil(image):
  res = requests.get(image)
  uri = f"data:{res.headers['Content-Type']};base64,{base64.b64encode(res.content).decode('utf-8')}"
  pil_img = decode_base64_to_image(uri)

  return pil_img

def resizePilImg(pil_img, size):
  numpy_image = numpy.array(pil_img)  
  cv_img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

  resized_cv_img = cv2.resize(cv_img, size)
  color_converted_cv = cv2.cvtColor(resized_cv_img, cv2.COLOR_BGR2RGB)
  pil_img = Image.fromarray(color_converted_cv)
  
  return pil_img
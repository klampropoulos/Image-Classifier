from keras.models import model_from_json
from keras.preprocessing import image
import os
from PIL import Image
import numpy as np 
import tensorflow as tf

global graph


class Classifier(object):

	model=None
	graph=tf.get_default_graph()


	def __init__(self):
		self.model=model_from_json(open(os.path.join('model','model.json')).read())
		self.model.load_weights(os.path.join('model','model.h5'))
		
		self.model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])




	def predict(self,filename):
		img=image.load_img(filename,target_size=(64,64))
		
		img=image.img_to_array(img)
		
		img=np.expand_dims(img,axis=0)

		print(img.shape)
		with self.graph.as_default():
			result=self.model.predict(img)

		predicted_label=("Dog" if result == 1 else "Cat" )
		return predicted_label

		

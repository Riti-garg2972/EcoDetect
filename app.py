from flask import Flask, render_template, request
from keras.models import load_model
import tensorflow as tf
import numpy as np
import os
from keras.preprocessing import image

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

dic = {0 : 'compost', 1 : 'glass', 2: 'metal', 3 : 'plastic'}

model1 = load_model('model.h5')
model =load_model("plant.h5")

model.make_predict_function()
model1.make_predict_function()

def predict_label(img_path):
  i = tf.keras.utils.load_img(img_path, target_size=(120,120))
  i = tf.keras.utils.img_to_array(i)/255.0
  i = i.reshape(1, 120,120,3)
  p = model1.predict(i)
  c = np.argmax(p,axis=1)
  if c == 0:
     return "compost"
  elif c ==1:
     return "Glass"
  elif c==2:
     return "Metal"
  else:
     return "plastic"
        

#------------>>pred_cot_dieas<<--start
def pred_cot_dieas(cott_plant):
  test_image = tf.keras.utils.load_img(cott_plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = tf.keras.utils.img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image).round(3) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result) # get the index of max value

  if pred == 0:
    return "Healthy Cotton Plant -  Although the chemical fertilizer has fallen on the leaves of the tree, the leaves are burnt, but there is no need to worry "
  elif pred == 1:
    return "Diseased cotton plant - Attack of Leaf Sucking and Chewing Pests"
  elif pred == 2:
    return 'Healthy Cotton Plant with fresh leaves'
  else:
    return "Healthy Cotton Plant"

#------------>>pred_cot_dieas<<--end

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route("/waste-management", methods = ['GET','POST'])
def waste_management():
	return render_template("waste-management.html")


@app.route("/plant", methods = ['GET','POST'])
def plant():
	return render_template("plant.html")

@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

# Waste Management
@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)
		p = predict_label(img_path)

	return render_template("waste-management.html", prediction = p, img_path = img_path)

# Plant disease detection
@app.route("/predict", methods = ['GET','POST'])
def predict():
  if request.method == 'POST':
    file = request.files['image'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join('static/user', filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred  = pred_cot_dieas(cott_plant=file_path)
    return render_template("plant.html", prediction = pred, img_path = file_path)
     

if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
        
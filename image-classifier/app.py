import os
from classifier import Classifier

from flask import Flask ,request,redirect,url_for,render_template,flash
from flask import send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER='templates/uploads'
ALLOWED_EXTENSIONS =set(['txt','pdf','png','jpg','jpeg','gif'])


app=Flask(__name__)
app.config.from_object(__name__)


app.config['MAX_CONTENT_LENGTH']=16*1024*1024

classifier=Classifier()


def right_type(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def  store_uploaded_image(action):
	#check if the post request hasthe file part
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file=request.files['file']
	#if user does not select file ,browser also 
	#submit a empty part without filename
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)
	if file and right_type(file.filename):
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		return redirect(url_for(action,filename=filename))



@app.route('/',methods=['GET','POST'])
def classifiers():
	if request.method=='POST':
		return store_uploaded_image('classifier_result')
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/classifier_result')
def clf():
	return render_template('classifier_result.html')

@app.route('/classifier_result/<filename>')
def classifier_result(filename):
	filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
	predicted_label=classifier.predict(filepath)
	return render_template('classifier_result.html',filename=filename,
		predicted_label=predicted_label)


def get_image(filename):
	return send_from_directory(app.cofig['UPLOAD_FOLDER'],filename)

def main():

	app.run(debug=True)



if __name__ == '__main__':
	main()
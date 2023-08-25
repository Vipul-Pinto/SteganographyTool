from flask import Flask, render_template, request, redirect
import main, cv2, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
    result = None
    if request.method == 'POST':
        if request.form.get('action') == 'encrypt':
            images = request.files['image']
            image = secure_filename(images.filename)
            images.save("static/"+image)
            im = cv2.imread("static/"+image)
            os.remove("static/"+image)
            plaintext = request.form.get('plaintext')
            keyword = request.form.get('keyword')
            im = main.hide(im, plaintext, keyword)
            cv2.imwrite("static/output.png",im)
            result = ("static/output.png","image")
        else:
            images = request.files['image']
            image = secure_filename(images.filename)
            images.save("static/"+image)
            im = cv2.imread("static/"+image)
            os.remove("static/"+image)
            plaintext = request.form.get('palintext')
            keyword = request.form.get('keyword')
            result = (main.get(im,keyword),"text")
    return render_template('index.html',result = result)

if __name__ == "__main__":
    app.run(debug=True)
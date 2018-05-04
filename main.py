from flask import Flask,render_template, request
app = Flask(__name__)

# Add cloud datastore settings

@app.route('/')
def HelloWorld():
    return render_template("index.html")

# login required
@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/submit-image')
def image_submit():
    return render_template('image-submit.html')

@app.route('/image/<int:image_id>')
def image_detail(image_id):
    return render_template('image-detail.html', image_id=image_id)

@app.route('/image/<int:image_id>/delete')
def image_delete(image_id):
    return render_template('image-delete.html', image_id=image_id)


def shorten(image_full_url):
    pass

def save_to_onedrive():
    pass

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=5000, debug=True)
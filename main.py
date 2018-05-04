from flask import Flask,render_template, request
app = Flask(__name__)

# from sqlalchemy import create_engine
# from sqlalchemy.orm import session
# from database_setup import Base

# engine = create_engine()
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

@app.route('/')
def HelloWorld():
    return render_template("index.html")

@app.route('/profile/')
def profile():
    return 'This is my Profile Page'

@app.route('/submit-image')
def image_submit():
    return 'Form for submitting images'

@app.route('/image/<int:image_id>')
def image_detail(image_id):
    return "This is the page for image with id: " + str(image_id)

@app.route('/image/<int:image_id>/delete')
def image_delete(image_id):
    return "Delete image with id " + str(image_id)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=5000, debug=True)
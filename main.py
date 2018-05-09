import uuid
from flask import (
    Flask, render_template, request, flash, redirect, url_for                
)

# Manage login_sessions
from flask import session as login_session
from flask_oauthlib.client import OAuth

app = Flask(__name__)
import config

# app.config.from_object(config.py)
app.secret_key = 'development'
OAUTH = OAuth(app)
MSGRAPH = OAUTH.remote_app(
    'microsoft', consumer_key=config.CLIENT_ID, consumer_secret=config.CLIENT_SECRET,
    request_token_params={'scope': config.SCOPES},
    base_url=config.RESOURCE + config.API_VERSION + '/',
    request_token_url=None, access_token_method='POST',
    access_token_url=config.AUTHORITY_URL + config.TOKEN_ENDPOINT,
    authorize_url=config.AUTHORITY_URL + config.AUTH_ENDPOINT)

# Add cloud datastore settings
# Setup the data model.
# with app.app_context():
    # from . import model_datastore
    # model = model_datas                                                                                                                   tore
    # model.init_app(app)



# Views
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    """Prompt user to authenticate."""
    login_session['state'] = str(uuid.uuid4())
    return MSGRAPH.authorize(callback=config.REDIRECT_URI, state=login_session['state'])

@app.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""
    if str(login_session['state']) != str(request.args['state']):
        raise Exception('state returned to redirect URL does not match!')
    response = MSGRAPH.authorized_response()
    # Store access_token returned from microsoft
    login_session['access_token'] = response['access_token']
    
    # Get and save User data
    endpoint = 'me'
    graphdata = MSGRAPH.get(endpoint, headers=request_headers()).data
    login_session['username'] = graphdata['givenName'] 
    login_session['email'] = graphdata['userPrincipalName']
    print(graphdata)
    return redirect(url_for('profile'))


@MSGRAPH.tokengetter
def get_token():
    """Called by flask_oauthlib.client to retrieve current access token."""
    return (login_session.get('access_token'), '')


# login required
@app.route('/profile/')
def profile():
    if 'email' not in login_session:
        flash('Please login with your Microsoft Account')
        return redirect(url_for('index'))
    username = login_session['username']
    return render_template('profile.html', username=username)

@app.route('/submit-image')
def image_submit():
    # user_profile = MSGRAPH.get('me', headers=request_headers()).data
    # user_name = user_profile['displayName']

    # upload_response = upload_file(client=MSGRAPH, filename=submitted_pic)
    # if str(upload_response.status).startswith('2'):
    #     # create a sharing link for the uploaded photo
    #     link_url = sharing_link(client=MSGRAPH, item_id=upload_response.data['id'])
    # else:
    #     link_url = ''
    return render_template('image-submit.html')

@app.route('/image/<int:image_id>')
def image_detail(image_id):
    return render_template('image-detail.html', image_id=image_id)

@app.route('/image/<int:image_id>/delete')
def image_delete(image_id):
    return render_template('image-delete.html', image_id=image_id)


def shorten(image_full_url):
    pass

def get_client():
    return datastore.Client(config.PROJECT_ID)

def request_headers(headers=None):
    """Return dictionary of default HTTP headers for Graph API calls.
    Optional argument is other headers to merge/override defaults."""
    default_headers = {'SdkVersion': 'sample-python-flask',
                       'x-client-SKU': 'sample-python-flask',
                       'client-request-id': str(uuid.uuid4()),
                       'return-client-request-id': 'true'}
    if headers:
        default_headers.update(headers)
    return default_headers

def upload_file(*, client, filename, folder=None):
    """Upload a file to OneDrive for Business.

    client  = user-authenticated flask-oauthlib client instance
    filename = local filename; may include a path
    folder = destination subfolder/path in OneDrive for Business
             None (default) = root folder

    File is uploaded and the response object is returned.
    If file already exists, it is overwritten.
    If folder does not exist, it is created.

    API documentation:
    https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/driveitem_put_content
    """
    # fname_only = os.path.basename(filename)

    # # create the Graph endpoint to be used
    # if folder:
    #     # create endpoint for upload to a subfolder
    #     endpoint = f'me/drive/root:/{folder}/{fname_only}:/content'
    # else:
    #     # create endpoint for upload to drive root folder
    #     endpoint = f'me/drive/root/children/{fname_only}/content'

    # content_type, _ = mimetypes.guess_type(fname_only)
    # with open(filename, 'rb') as fhandle:
    #     file_content = fhandle.read()

    # return client.put(endpoint,
    #                   headers=request_headers({'content-type': content_type}),
    #                   data=file_content,
    #                   content_type=content_type)

# def getUserId(email):
#     try:
#         user = session.query(User).filter_by(email=email).one()
#         return user.id
#     except:
#         return None

# def getUserInfo(user_id):
#     user = session.query(User).filter_by(id=user_id).one()
#     return user

# def createUser(login_session):
#     newUser = User(name=login_session['username'], 
#         email=login_session['email'], picture=login_session['picture'])
#     session.add(newUser)
#     session.commit()
#     user = session.query(User).filter_by(email=login_session['email']).one()
#     return user.id

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port=5000, debug=True)
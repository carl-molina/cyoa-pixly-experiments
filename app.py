import os
from dotenv import load_dotenv
from s3_helpers import upload_to_s3, view_photos_from_s3
import boto3

# load environment variables from .env file
load_dotenv()

AWS_ACCESS_KEY = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BUCKET_NAME = os.environ['bucket_name']
REGION_CODE = os.environ['region_code']

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template, flash, redirect
from models import photos_metadata_colname_conversions, Photo, connect_db
import exifread


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)

# attempt at configuring S3 connection, "manage via python" from lecture
s3 = boto3.client(
    's3',
    'us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


@app.route('/', methods=['GET'])
def homepage():
    """Show homepage"""

    # FIXME: moved logic to helpers function file
    photos_urls = view_photos_from_s3()

    return render_template('base.html', photos_urls=photos_urls)


@app.route('/upload', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        file = request.files['photo']
        # after receiving valid photo file from form, we get a 'FileStorage'
        # object w/ methods and properties on it, most importantly, 'filename'.
        if file:
            tags = exifread.process_file(file)

            metadata_tags = {}
            filename = file.filename
            metadata_tags["filename"] = filename

            for key, value in tags.items():
                if key not in metadata_tags and key in photos_metadata_colname_conversions:
                    conversion = photos_metadata_colname_conversions[key]
                    metadata_tags[conversion] = str(value)

            new_photo_in_db = Photo.submit_photo(metadata_tags)
            print('new_photo_in_db: ', new_photo_in_db)

            # puts cursor back to the beginning of the file
            file.seek(0)

            upload_to_s3(file, filename)
            # TODO: ^ this closes file
            flash('File uploaded successfully!')
            return redirect('/')
    return render_template('form.html')
from flask import Flask
from flask import request
from flask import render_template
from utils.tracker import read_torrent_url,read_torrent_file,get_torrent_info
from os import getcwd
app = Flask(__name__)

# settings
UPLOAD_FOLDER = getcwd() + 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/",methods=['GET','POST'])
def hello():
    tracker_info = None
    if request.method == 'POST':
        try:
            uploaded_file = request.files['torrent_file']
            # TODO : change this
            temp_filename = '/tmp/file.torrent'
            uploaded_file.save(temp_filename)
            torrent = read_torrent_file(temp_filename)
            #filename = secure_filename(file_name.filename)
            #torrent = read_torrent_file(filename)
        except:
            try:
                url = request.form['torrent_url']
                torrent = read_torrent_url(url)
            except:
                pass
        torrent_info = get_torrent_info(torrent)
    return render_template('index.html',info = torrent_info)

@app.route("/pg/<view_file>")
def static_page(view_file='about'):
    return render_template(view_file+'.html')

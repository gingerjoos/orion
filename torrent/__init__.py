from flask import Flask
from flask import request
from flask import render_template
from utils.tracker import read_torrent_url,read_torrent_file,get_tracker_info
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def hello():
    tracker_info = None
    if request.method == 'POST':
        try:
            url = request.form['torrent_url']
            torrent = read_torrent_url(url)
        except:
            file_name = request.form['torrent_file']
            torrent = read_torrent_file(file_name)
        tracker_info = get_tracker_info(torrent)
    return render_template('index.html',info = tracker_info)

@app.route("/pg/")
@app.route("/pg/<name>")
def name_print(name='Anirudh'):
    return render_template('name.html',name=name)

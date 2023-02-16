from flask import Flask,request, render_template, session, send_file, url_for, redirect
from pytube import YouTube
from io import BytesIO
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        print(session['link'])
        try:
            url = YouTube(session['link'])
            # url.check_availibility()
        except:
            return render_template('error.html')
        return render_template('download.html', url=url)
    return render_template('index.html')

@app.route("/download", methods = ['GET', 'POST'])
def download():
    if request.method == "POST":
        try:
            buffer = BytesIO()
            url = YouTube(session['link'])
            itag = request.form.get("itag")
            video = url.streams.get_by_itag(itag)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            title = url.title
            title = title.strip()+".mp4"
            return send_file(buffer, as_attachment=True, download_name=title, mimetype="video/mp4")
        except:
            return render_template('error.html')
    return redirect(url_for("home"))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
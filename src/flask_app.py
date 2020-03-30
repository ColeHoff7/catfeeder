from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def home():
    paw_pic = url_for('static', filename='paw_cursor.png')
    pork_pic = url_for('static', filename='porko.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('index.html', paw_pic=paw_pic, pork_pic=pork_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js)

@app.route('/setfeed')
def set_feed():
    paw_pic = url_for('static', filename='paw_cursor.png')
    pork_pic = url_for('static', filename='porko.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('setfeed.html', paw_pic=paw_pic, pork_pic=pork_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js)

@app.route('/feedlog')
def feed_log():
    paw_pic = url_for('static', filename='paw_cursor.png')
    pork_pic = url_for('static', filename='porko.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('feedlog.html', paw_pic=paw_pic, pork_pic=pork_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

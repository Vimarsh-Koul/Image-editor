from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/editor.html")
def editor():
	return render_template('editor.html')

@app.route("/faq.html")
def faq():
	return render_template('faq.html')

@app.route('/editor/<username>')
def profile(username): 
	return '{}\'s profile'.format(escape(username))	


if __name__ == '__main__':
	app.run(debug=True)	
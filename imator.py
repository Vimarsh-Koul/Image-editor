from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def home():
	return "Hello world!"

@app.route("/editor")
def editor():
	return "editor page"

@app.route("/faq")
def faq():
	return "faq page"

@app.route('/editor/<username>')
def profile(username): 
	return '{}\'s profile'.format(escape(username))	


if __name__ == '__main__':
	app.run(debug=True)	

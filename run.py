from my_server import app

if __name__ == '__main__':
	app.run(host='localhost', port=8080, debug=True)
	# app.run(host='0.0.0.0', port=80)
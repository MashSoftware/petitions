from application import app

app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])

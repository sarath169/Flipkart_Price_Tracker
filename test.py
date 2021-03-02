from flask import Flask, jsonify, render_template, request
app = Flask(__name__,template_folder='/home/sarath/Documents/Flipkart_Price_Tracker')

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)

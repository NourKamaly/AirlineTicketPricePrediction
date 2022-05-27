from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict',methods=['GET'])
def predict():
    date=request.args.get('date')
    Airline=request.args.get('Airline')
    departuretime=request.args.get('departuretime')
    stops=request.args.get('stops')
    arrivaltime=request.args.get('arrivaltime')
    type=request.args.get('type')
    source=request.args.get('source')
    destination=request.args.get('destination')
    return str(source)



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')



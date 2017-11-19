from flask import Flask, json, request
import os
import momentumTrader as mt

app = Flask(__name__)

# Post a json to flask server

@app.route('/Tradium/projection', methods=['Post', 'Get'])
def api_root():
    # validate that user sends in a json
    if not request.headers or request.headers['Content-Type'] != 'application/json':
        return json.dumps({'message': 'invalid post'})

    data = json.loads(json.dumps(request.json))

    # data is a map of all the json input
    if 'securities' not in data:
        return json.dumps({'message':'missing securites'})
    if 'start_cash' not in data:
        return json.dumps({'message':'missing start_cash'})
    securities = data["securities"]
    startingCash = data['start_cash']
    trader = mt.MomentumStrategy(startingCash)
    trader.setUniverse(securities)
    try:
        trader.run()
    except Exception as e:
        return json.dumps({'message': 'FAILURE'})

    # making something to return
    return json.dumps({'networth_over_time': trader.getNetworth()})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 1337))
    app.run(debug=True, host='0.0.0.0', port=port)

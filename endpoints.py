from flask import Flask, json, request
import os
import strategies as s

app = Flask(__name__)

# Post a json to flask server

@app.route('/Tradium/projection', methods=['Post', 'Get'])
def api_root():
    # validate that user sends in a json

    data = json.loads(request.data)

    # data is a map of all the json input
    if 'securities' not in data:
        return json.dumps({'message':'missing securites'})
    if 'start_cash' not in data:
        return json.dumps({'message':'missing start_cash'})
    if 'strategy' not in data:
        return json.dumps({'message':'missing strategy'})
    securities = str(data["securities"])
    startingCash = int(data['start_cash'])
    strategy = str(data['strategy'])
    if strategy == 'momentum':
        trader = s.MomentumStrategy(startingCash)
    elif strategy == 'random':
        trader = s.RandomStrategy(startingCash)
    elif strategy == 'passive':
        trader = s.PassiveStrategy(startingCash)
    else:
        return json.dumps({'message':'unimplemented strategy'})
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

from flask import Flask, jsonify, render_template, request

from shuffle_scorers import SCORE_TYPE
from shuffle_simulator import shuffle_decks
from shufflers import SHUFFLE_STRAT

app = Flask(__name__)
app.debug = True

@app.route("/" , methods=['GET', 'POST'])
def shuffle_simulation():
    max_shuffles = [str(i+1) for i in range(6)]
    # max_shuffles.sort(reverse=True)

    return render_template('simulation.html',
        strats=SHUFFLE_STRAT,
        scorers=SCORE_TYPE,
        max_shuffles=max_shuffles,
    )

@app.route('/calculate', methods=['GET'])
def calculate():
    selected_strat = request.args.get('selected_strat', type=str)
    selected_scorer = request.args.get('selected_scorer', type=str)
    selected_max_shuffles = request.args.get('selected_max_shuffles', type=str)
    result = shuffle_decks(
      SHUFFLE_STRAT[selected_strat], 
      SCORE_TYPE[selected_scorer],
      int(selected_max_shuffles)
    )

    return jsonify({'result': result.permutation})

if __name__ == "__main__":
    app.run()
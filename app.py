from flask import Flask, jsonify, render_template, request

from shuffle_scorers import SCORE_TYPE
from shuffle_simulator import shuffle_decks
from shufflers import SHUFFLE_STRAT


app = Flask(__name__)
app.debug = True

@app.route('/calculate', methods=['GET'])
def calculate():
    deck_size = request.args.get('deck_size', type=str)
    selected_strat = request.args.get('selected_strat', type=str)
    selected_scorer = request.args.get('selected_scorer', type=str)
    selected_max_shuffles = request.args.get('selected_max_shuffles', type=str)
    min_num_piles = request.args.get('min_num_piles', type=str)
    max_num_piles = request.args.get('max_num_piles', type=str)

    result = shuffle_decks(
      SHUFFLE_STRAT[selected_strat], 
      SCORE_TYPE[selected_scorer],
      int(selected_max_shuffles),
      int(deck_size),
      int(min_num_piles),
      int(max_num_piles)
    )

    return jsonify({'result': result.permutation})

@app.route("/" , methods=['GET', 'POST'])
def shuffle_simulation():
    max_shuffles = [str(i+1) for i in range(6)]
    min_piles = [str(i+1) for i in range(9)]

    return render_template('simulation.html',
        strats=SHUFFLE_STRAT,
        scorers=SCORE_TYPE,
        max_shuffles=max_shuffles,
        min_piles=min_piles
    )

if __name__ == "__main__":
    app.run()
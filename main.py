from flask import Flask, render_template, request

import museum_tree
import cache_api

app = Flask(__name__, template_folder='templates', static_folder='statics')


def main():
    """
    Main function reads in tree and user can play and test with it in the terminal.
    """
    # Load tree:
    tree = museum_tree.loadTreeFromJSON(museum_tree.TREE_FILE_JSON)

    # Load museum cache:
    museum_file = cache_api.open_cache("museum.json")
    museum_cache = museum_file.get("museums", [])

    # Find museums with tree:
    museum_tree.findMuseums(tree, museum_cache)

def find_musuem_by_answers(answers, number_of_museums):
    museum_file = cache_api.open_cache("museum.json")
    museum_cache = museum_file.get("museums", [])

    tree = museum_tree.loadTreeFromJSON(museum_tree.TREE_FILE_JSON)

    # Find musuems with tree:
    musuem_result = museum_tree.findMuseumByAnswers(answers, tree, museum_cache, number_of_museums)
    return musuem_result


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        print("POST")
        answers = []
        answers.append(request.form.get("e_hemi"))
        answers.append(request.form.get("large"))
        answers.append(request.form.get("high_rating"))
        answers.append(request.form.get("multi_lang"))

        number_of_museums = int(request.form.get("number_of_museums"))
        museums = find_musuem_by_answers(answers, number_of_museums)

        return render_template("museums.html", museums=museums)
    
    return render_template("index.html")


if __name__ == "__main__":
    # main()
    print("starting Flask app", app.name)
    app.run(debug=True)
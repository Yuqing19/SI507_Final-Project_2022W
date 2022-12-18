from museum import Museum
import cache_api
import random
import json

TREE_FILE_JSON = "museum_tree.json"

empty_tree = (
    "Do you want to vist a museum in eastern hemispheres?",
    ("Do you want to visit a large museum?",
        ("Do you want to visit a museum with rating_average greater than 8.0?",
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            ),
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            )
        ),
        ("Do you want to visit a museum with rating_average greater than 8.0?",
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            ),
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            )
        )
    ),

    ("Do you want to visit a large museum?",
        ("Do you want to visit a museum with rating_average greater than 8.0?",
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            ),
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            )
        ),
        ("Do you want to visit a museum with rating_average greater than 8.0?",
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            ),
            ("Do you want to visit a museum supports multi-language?",
                ([], None, None), ([], None, None),
            )
        )
    )
)

def main():
    """
    The main function. It can printout the cached tree
    --------------------
    Parameters:
    None
    --------------------
    Return:
    None
    """
    museum_file = cache_api.open_cache("museum.json")
    museum_cache = museum_file.get("museums", [])

    tree = buildTree(museum_cache, empty_tree)
    saveTreeToJSON(tree, TREE_FILE_JSON)
    tree = loadTreeFromJSON(TREE_FILE_JSON)
    printTree(tree)

def buildTree(museums, tree=None):
    """
    Build a tree.
    --------------------
    Parameters:
    None
    --------------------
    Return:
    tree: a tree
    """
    if tree is None:
        tree = (None, None, None)

    for idx, museum_json in enumerate(museums):
        museum = Museum(museum_json)
        museum_answers = []
        if (-20 < museum.longitude < 160):
            museum_answers.append("Yes")
        else:
            museum_answers.append("No")
        
        if (museum.exhibit_number > 50):
            museum_answers.append("Yes")
        else:
            museum_answers.append("No")
        
        if (museum.rating_average > 8):
            museum_answers.append("Yes")
        else:
            museum_answers.append("No")

        if (museum.languages ==  ["en"]):
            museum_answers.append("Yes")
        else:
            museum_answers.append("No")
        
        museum.list_index = idx
        museum.answers = museum_answers
        addMuseum(tree, museum)
    return tree

def addMuseum(tree, museum, question_number = 0):
    """
    Insert a museum into the tree.
    --------------------
    Parameters:
    tree: a tree
    museum: a museum
    --------------------
    Return:
    tree: an updated tree
    """
    if type(tree[0]) is list:
        tree[0].append(museum.list_index)
        return tree
    
    if museum.answers[question_number] == "Yes":
        addMuseum(tree[1], museum, question_number + 1)
    
    if museum.answers[question_number] == "No":
        addMuseum(tree[2], museum, question_number + 1)


def saveTreeToJSON(tree, tree_file):
    """
    Save the tree to the file treeFile.
    --------------------
    Parameters:
    tree: a tree
    tree_file: a file name
    --------------------
    Return:
    None
    """
    tree_json = convertTreeToJSON(tree)
    with open(tree_file, "w") as outfile:
        json.dump(tree_json, outfile, indent=4)


def convertTreeToJSON(tree):
    """
    Convert the tree to a json object.
    --------------------
    Parameters:
    tree: a tree
    --------------------
    Return:
    tree_json: a json object
    """
    if tree[1] is not None and tree[2] is not None:
        tree_json = {
            "question": tree[0],
            "yes": convertTreeToJSON(tree[1]),
            "no": convertTreeToJSON(tree[2]),
        }
    else:
        tree_json = {"object": tree[0]}
    return tree_json


def convertJSONToTree(tree_json):
    """
    Convert the json object to a tree.
    --------------------
    Parameters:
    tree_json: a json object
    --------------------
    Return:
    tree: a tree
    """
    if "question" in tree_json:
        tree = (
            tree_json["question"],
            convertJSONToTree(tree_json["yes"]),
            convertJSONToTree(tree_json["no"]),
        )
    else:
        tree = (tree_json["object"], None, None)
    return tree


def loadTreeFromJSON(tree_file):
    """
    Load the tree from the file treeFile and return the tree.
    --------------------
    Parameters:
    tree_file: a file name
    --------------------
    Return:
    tree: a tree
    """
    with open(tree_file) as json_file:
        tree_json = json.load(json_file)
    return convertJSONToTree(tree_json)


def findMuseums(tree, museums, random_size = 3):
    """
    Find museum with the tree.
    --------------------
    Parameters:
    tree: a tree
    museums_file_handle: a handle to the museums cache file
    random_size: the number of museums to return
    --------------------
    Return:
    None
    """
    if type(tree[0]) is list:
        print("Here are some museums you may like:")
        for idx in random.sample(tree[0], min(random_size, len(tree[0]))):
            museum = Museum(museums[idx])
            print(museum.name)
        return
    
    answer = input(tree[0] + " (Yes/No): ")
    if answer == "Yes":
        findMuseums(tree[1], museums)
    elif answer == "No":
        findMuseums(tree[2], museums)

def findMuseumByAnswers(answers, tree, museums, number_of_museums):
    """
    Find museum with given tree and questionnaire answers.
    --------------------
    Parameters:
    answers: a list of answers from the questionair
    tree: a tree
    museums_file_handle: a handle to the museums cache file
    number_of_museums: the number of museums to return
    --------------------
    Return:
    None
    """
    result = []
    if type(tree[0]) is list:
        print("Here are some museums you may like:")
        for idx in random.sample(tree[0], min(number_of_museums, len(tree[0]))):
            museum = Museum(museums[idx])
            result.append(museum)
            print(museum.name)
        return result
    
    answer = answers.pop(0)
    if answer == "Yes":
        result = findMuseumByAnswers(answers, tree[1], museums, number_of_museums)
    elif answer == "No":
        result = findMuseumByAnswers(answers, tree[2], museums, number_of_museums)

    return result

def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}{text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")

if __name__ == "__main__":
    main()
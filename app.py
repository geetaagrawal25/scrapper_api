# Api used to ingest to Kylin Data Warehouse

from flask import Flask, make_response, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def return_data():
    truths = pd.read_csv("truths.csv")
    falses = pd.read_csv("falses.csv")
    final = pd.concat([truths, falses])

    final_return = []
    for index, row in final.iterrows():
        final_return.append({"name":row["name"], "text":row["text"], "category":row["category"]})

    return make_response(jsonify(final_return), 200)

if __name__ == "__main__":
    app.run()

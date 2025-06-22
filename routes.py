from flask import render_template
import pandas as pd

def register_routes(app):
    data_abund = pd.read_csv("data/9606_abund.txt", sep="\t")
    data_dom = pd.read_csv("data/9606_gn_dom.txt", sep="\t")
    data_abund = data_abund.rename(columns={"#Taxid": "Taxid"})
    data_dom = data_dom.rename(columns={"#Gn": "Gn"})

    abund = data_abund.head(10)
    dom = data_dom.head(10)

    @app.route("/")
    def index():
        # A1
        # How many protein/copy-number pairs are in the file? (Single numerical value)
        answer_A1_1 = data_abund.shape[0]

        # How many unique copy number values are there in the file? (Single numerical value)
        answer_A1_2 = data_abund.drop_duplicates().shape[0]

        # How many pairs of protein and copy number values are in the file? (Single numerical value)
        answer_A1_3 = data_abund.drop_duplicates().shape[0]




        return render_template("index.html", abund=abund, dom=dom, answer_A1_1=answer_A1_1,
                               answer_A1_2=answer_A1_2, answer_A1_3=answer_A1_3)
from flask import render_template, jsonify
import pandas as pd
import numpy as np

def register_routes(app):
    data_abund = pd.read_csv("data/9606_abund.txt", sep="\t")
    data_dom = pd.read_csv("data/9606_gn_dom.txt", sep="\t")
    data_abund = data_abund.rename(columns={"#Taxid": "Taxid"})
    data_dom = data_dom.rename(columns={"#Gn": "Gn"})

    # A2, A3
    unique_copy_num = data_abund.drop_duplicates().copy()
    unique_copy_num["Mean-copy-number"] = pd.to_numeric(unique_copy_num["Mean-copy-number"], errors="coerce")
    mean_value = unique_copy_num["Mean-copy-number"].mean()
    std_value = unique_copy_num["Mean-copy-number"].std()
    mean_std_for_each_protein = unique_copy_num.groupby("Gn")["Mean-copy-number"].agg(["mean", "std"]).reset_index()
    mean_std_for_each_protein["std"] = mean_std_for_each_protein["std"].fillna(0)


    # B1, B2
    data_dom = data_dom.drop_duplicates()
    proteins_domains = data_dom.merge(mean_std_for_each_protein[["Gn", "mean", "std"]], on="Gn", how="left")
    count_domain = proteins_domains.groupby(["Gn", "Domain", "mean", "std"])["Domain"].size().reset_index(name="count_domain")
    count_domain["domain_average_abundance"] = count_domain["count_domain"] * count_domain["mean"]
    most_prevalent_domain = count_domain.groupby("Domain").agg({
        "domain_average_abundance": "sum",
        "count_domain": "sum"
    }).reset_index().sort_values("domain_average_abundance", ascending=False)

    std_count = (
        count_domain.assign(std_squared=lambda d: d["std"]**2)
        .groupby("Domain")["std_squared"]
        .sum()
        .apply(np.sqrt)
        .reset_index()
        .rename(columns={"std_squared": "domain_abundance_std"})
    )

    domain_summary = count_domain.groupby("Domain").agg({
        "domain_average_abundance": "sum",
        "count_domain": "sum"
    }).reset_index().sort_values("domain_average_abundance", ascending=False)
    avg_abund_each_domain = domain_summary.merge(std_count, on="Domain")
    avg_abund_each_domain["percentile_rank"] = avg_abund_each_domain["domain_average_abundance"].rank(pct=True, ascending=True) * 100

    @app.route("/api/<question_id>")
    def api_dispatch(question_id):
        if question_id == "A1-1":
            return jsonify({"answer": int(data_abund.shape[0])})
        elif question_id == "A1-2":
            return jsonify({"answer": int(data_abund["Mean-copy-number"].nunique())})
        elif question_id == "A1-3":
            return jsonify({"answer": int(data_abund.drop_duplicates().shape[0])})
        elif question_id == "A2-1":
            return jsonify({
                "mean": round(mean_value, 2),
                "std": round(std_value, 2)
            })
        elif question_id == "A2-2":
            answer = mean_std_for_each_protein.sort_values("mean", ascending=False).head(10).to_dict(orient="records")
            # print('A2-2 answer:', answer)
            return jsonify({"table": answer})
        elif question_id == "A3":
            mean_std_for_each_protein["percentile_rank"] = mean_std_for_each_protein["mean"].rank(pct=True,
                                                                                                  ascending=True) * 100
            table = mean_std_for_each_protein.sort_values("mean", ascending=False).head(10).to_dict(orient="records")
            # print('A3 answer:', table)
            return jsonify({"table": table})
        elif question_id == "B1":
            row = most_prevalent_domain.iloc[0]
            domain_name = row["Domain"]
            avg_abundance = round(row["domain_average_abundance"], 2)
            times_seen = int(row["count_domain"])
            return jsonify({
                "domain": domain_name,
                "avg_abundance": avg_abundance,
                "times_seen": times_seen
            })
        elif question_id == "B2":
            table = avg_abund_each_domain.sort_values("domain_average_abundance", ascending=False).head(10)
            table = table[["Domain", "domain_average_abundance", "domain_abundance_std", "count_domain", "percentile_rank"]]
            table = table.round(2).to_dict(orient="records")
            # print('B3 answer:', table)
            return jsonify({"table": table})
        else:
            return jsonify({"error": "Unknown question ID"}), 404

    @app.route("/")
    def index():
        return render_template("index.html")
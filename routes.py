from flask import render_template, jsonify
import pandas as pd
import numpy as np

def register_routes(app):

    """
    Register all Flask routes for the protein abundance and domain analysis app.

    This function:
    - Loads and preprocesses protein abundance and domain data
    - Calculates statistical metrics (mean, std, percentile rank)
    - Defines API endpoints for each question
    - Serves the main index HTML page

    Each API endpoint returns either a single value or a JSON table with top results.
    """

    # Load and preprocess data
    data_abund = pd.read_csv("data/9606_abund.txt", sep="\t")
    data_dom = pd.read_csv("data/9606_gn_dom.txt", sep="\t")
    data_abund = data_abund.rename(columns={"#Taxid": "Taxid"})
    data_dom = data_dom.rename(columns={"#Gn": "Gn"})

    # A2, A3 calculations
    unique_copy_num = data_abund.drop_duplicates().copy()
    unique_copy_num["Mean-copy-number"] = pd.to_numeric(unique_copy_num["Mean-copy-number"], errors="coerce")
    mean_value = unique_copy_num["Mean-copy-number"].mean()
    std_value = unique_copy_num["Mean-copy-number"].std()
    mean_std_for_each_protein = unique_copy_num.groupby("Gn")["Mean-copy-number"].agg(["mean", "std"]).reset_index()
    mean_std_for_each_protein["std"] = mean_std_for_each_protein["std"].fillna(0)

    # B1, B2 calculations
    data_dom = data_dom.drop_duplicates()
    proteins_domains = data_dom.merge(mean_std_for_each_protein[["Gn", "mean", "std"]], on="Gn", how="left")
    count_domain = proteins_domains.groupby(["Gn", "Domain", "mean", "std"])["Domain"].size().reset_index(name="count_domain")

    # Domain summary
    domain_summary = count_domain.groupby("Domain").agg({
        "mean": "mean",
        "count_domain": "sum"
    }).reset_index()

    # Standard deviation propagation for domains
    std_count = (
        count_domain.assign(std_squared=lambda d: d["std"]**2)
        .groupby("Domain")["std_squared"]
        .sum()
        .apply(np.sqrt)
        .reset_index()
        .rename(columns={"std_squared": "domain_abundance_std"})
    )

    # Merge and compute ranks
    avg_abund_each_domain = domain_summary.merge(std_count, on="Domain")
    avg_abund_each_domain["percentile_rank"] = avg_abund_each_domain["mean"].rank(pct=True, ascending=True) * 100

    @app.route("/api/a1-1")
    def a1_1():
        return jsonify({"answer": int(data_abund.shape[0])})

    @app.route("/api/a1-2")
    def a1_2():
        return jsonify({"answer": int(data_abund[["Mean-copy-number", "Gn"]].drop_duplicates().shape[0])})

    @app.route("/api/a1-3")
    def a1_3():
        return jsonify({"answer": int(data_abund.drop_duplicates().shape[0])})

    @app.route("/api/a2-1")
    def a2_1():
        return jsonify({
            "mean": round(mean_value, 2),
            "std": round(std_value, 2)
        })

    @app.route("/api/a2-2")
    def a2_2():
        table = mean_std_for_each_protein.sort_values("mean", ascending=False).head(10).to_dict(orient="records")
        return jsonify({"table": table})

    @app.route("/api/a3")
    def a3():
        mean_std_for_each_protein["percentile_rank"] = round(mean_std_for_each_protein["mean"].rank(
            pct=True, ascending=True) * 100, 3)
        table = mean_std_for_each_protein[["Gn", "percentile_rank"]].sort_values("percentile_rank", ascending=False).head(10).to_dict(orient="records")
        return jsonify({"table": table})

    @app.route("/api/b1")
    def b1():
        row = avg_abund_each_domain.sort_values("mean", ascending=False).iloc[0]
        domain_name = row["Domain"]
        avg_abundance = round(row["mean"], 2)
        times_seen = int(row["count_domain"])
        return jsonify({
            "domain": domain_name,
            "avg_abundance": avg_abundance,
            "times_seen": times_seen
        })

    @app.route("/api/b2")
    def b2():
        table = avg_abund_each_domain.sort_values("mean", ascending=False).head(10)
        table = table[["Domain", "mean", "domain_abundance_std", "count_domain", "percentile_rank"]]
        table = table.rename(columns={"domain_abundance_std": "std"})
        table = table.round(2).to_dict(orient="records")
        return jsonify({"table": table})

    @app.route("/")
    def index():
        return render_template("index.html")
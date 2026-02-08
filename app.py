from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import numpy as np

app = Flask(__name__)

def format_id(num):
    try:
        return f"{int(num):,}".replace(",", ".")
    except:
        return "0"

def format_decimal(num, d=2):
    try:
        return f"{num:.{d}f}".replace(".", ",")
    except:
        return "0,00"

def configure_style():
    return {
        "Rendah": "#86efac",
        "Sedang": "#4ade80",
        "Tinggi": "#16a34a",
        "primary": "#1a5d1a"
    }

@app.route("/")
def dashboard():

    df = pd.read_csv("data/processed/aggregated_per_kabupaten.csv")

    df["petani_per_desa"] = df["total_petani_perempuan"] / df["jumlah_desa"]

    q1 = df["petani_per_desa"].quantile(0.25)
    q3 = df["petani_per_desa"].quantile(0.75)

    df["kategori_kepadatan"] = df["petani_per_desa"].apply(
        lambda x: "Rendah" if x < q1 else "Tinggi" if x > q3 else "Sedang"
    )

    COLOR = configure_style()

    summary = {
        "Total Petani Perempuan": format_id(df["total_petani_perempuan"].sum()),
        "Jumlah Kabupaten/Kota": df.shape[0],
        "Kabupaten Tertinggi": df.loc[df["total_petani_perempuan"].idxmax()]["bps_nama_kabupaten_kota"],
        "Kabupaten Terendah": df.loc[df["total_petani_perempuan"].idxmin()]["bps_nama_kabupaten_kota"],
    }

    top10 = (
        df.sort_values("total_petani_perempuan", ascending=False)
          .head(10)
          .sort_values("total_petani_perempuan")
    )

    max_val = top10["total_petani_perempuan"].max()

    fig_top10 = go.Figure()

    fig_top10.add_bar(
        x=top10["total_petani_perempuan"],
        y=top10["bps_nama_kabupaten_kota"],
        orientation="h",

        marker=dict(
            color=[COLOR[k] for k in top10["kategori_kepadatan"]]
        ),

        text=[format_id(x) for x in top10["total_petani_perempuan"]],
        textposition="inside",
        insidetextanchor="end",
        cliponaxis=False,

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Total Petani: %{x:,}<br>"
            "Kategori: %{customdata}<extra></extra>"
        ),
        customdata=top10["kategori_kepadatan"]
    )

    fig_top10.update_layout(
        height=320,
        showlegend=False,

        xaxis=dict(
            range=[0, max_val * 1.05],
            tickformat=",",
            automargin=True,
            zeroline=False
        ),

        yaxis=dict(
            automargin=True,
            categoryorder="total ascending"
        ),

        margin=dict(
            l=180,
            r=40,
            t=10,
            b=40
        ),

        uniformtext=dict(
            mode="hide",
            minsize=9
        )
    )

    fig_dist = go.Figure()

    fig_dist.add_trace(
        go.Histogram(
            x=df["petani_per_desa"],
            nbinsx=10,
            marker=dict(
                color="#22c55e",
                line=dict(width=0),
            ),
            opacity=0.85,
            hovertemplate=(
                "<b>Kepadatan</b>: %{x:.1f}<br>"
                "<b>Jumlah Kabupaten</b>: %{y}"
                "<extra></extra>"
            )
        )
    )

    mean_val = df["petani_per_desa"].mean()

    fig_dist.add_vline(
        x=q1,
        line_dash="dot",
        line_color="#94a3b8",
        annotation_text="Q1",
        annotation_position="top left",
        annotation_font_size=11
    )

    fig_dist.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#1a5d1a",
        line_width=2,
        annotation_text="Rata-rata",
        annotation_position="top",
        annotation_font_size=11
    )

    fig_dist.add_vline(
        x=q3,
        line_dash="dot",
        line_color="#94a3b8",
        annotation_text="Q3",
        annotation_position="top right",
        annotation_font_size=11
    )

    fig_dist.update_layout(
        height=330,
        bargap=0.15,
        showlegend=False,
        margin=dict(l=60, r=30, t=20, b=50),
        plot_bgcolor="#f1f5f9",
        paper_bgcolor="white",
        xaxis=dict(
    ),
    yaxis=dict(
        title="Jumlah Kabupaten/Kota",
        showgrid=True,
        gridcolor="rgba(0,0,0,0.05)",
        zeroline=False
    )
    )

    table_df = df[[
        "bps_nama_kabupaten_kota",
        "total_petani_perempuan",
        "jumlah_desa",
        "petani_per_desa",
        "kategori_kepadatan"
    ]].copy()

    table_df["total_petani_perempuan"] = table_df["total_petani_perempuan"].apply(format_id)
    table_df["jumlah_desa"] = table_df["jumlah_desa"].apply(format_id)
    table_df["petani_per_desa"] = table_df["petani_per_desa"].apply(format_decimal)

    table_html = table_df.to_html(
        classes="data-table",
        index=False,
        border=0
    )

    return render_template(
        "index.html",
        summary=summary,
        graph_top10=fig_top10.to_html(
            full_html=False,
            config={"responsive": True, "displayModeBar": False}
        ),
        graph_dist=fig_dist.to_html(
            full_html=False,
            config={"responsive": True, "displayModeBar": False}
        ),
        table=table_html
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
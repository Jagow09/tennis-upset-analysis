import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import os

pio.renderers.default = "browser"

OUTPUT_DIR  = "output/"
FIGURES_DIR = "output/figures/"
os.makedirs(FIGURES_DIR, exist_ok=True)

GRAND_SLAM_COLOUR   = "#1a3a5c"
MASTERS_COLOUR      = "#e8703a"
AVERAGE_LINE_COLOUR = "#e63946"

# ── Calculate true overall average ────────────────────────────────────────────
df_all = pd.read_csv("data/clean/atp_clean.csv")
df_all = df_all[df_all["rank_gap"] >= 10].copy()
df_all = df_all[df_all["surface"] != "Carpet"]
OVERALL_AVERAGE = df_all["upset"].mean()
print(f"True overall average upset rate: {OVERALL_AVERAGE:.1%}")

# ── Load analysis outputs ─────────────────────────────────────────────────────
upset_by_level      = pd.read_csv(os.path.join(OUTPUT_DIR, "upset_by_level.csv"))
upset_by_gap        = pd.read_csv(os.path.join(OUTPUT_DIR, "upset_by_gap.csv"))
upset_by_tournament = pd.read_csv(os.path.join(OUTPUT_DIR, "upset_by_tournament.csv"))
upset_by_surface    = pd.read_csv(os.path.join(OUTPUT_DIR, "upset_by_surface_level.csv"))
upset_by_round      = pd.read_csv(os.path.join(OUTPUT_DIR, "upset_by_round.csv"))
coefficients        = pd.read_csv(os.path.join(OUTPUT_DIR, "model_coefficients.csv"))

# ── Figure 1 ──────────────────────────────────────────────────────────────────
colours_level = [
    GRAND_SLAM_COLOUR if t == "Grand Slam" else MASTERS_COLOUR
    for t in upset_by_level["tourney_level_name"]
]

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=upset_by_level["tourney_level_name"],
    y=upset_by_level["upset_rate"],
    marker_color=colours_level,
    text=[f"{r:.1%}" for r in upset_by_level["upset_rate"]],
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Upset Rate: %{y:.1%}<br>Matches: %{customdata}<extra></extra>",
    customdata=upset_by_level["total_matches"]
))
fig1.add_hline(
    y=OVERALL_AVERAGE,
    line_dash="dash",
    line_color=AVERAGE_LINE_COLOUR,
    line_width=2,
    annotation_text=f"Overall average: {OVERALL_AVERAGE:.1%}",
    annotation_position="top right",
    annotation_font_color=AVERAGE_LINE_COLOUR
)
fig1.update_layout(
    title=dict(text="Upsets Are More Common Than You Think", font=dict(size=22)),
    xaxis_title="Tournament Level",
    yaxis_title="Upset Rate",
    yaxis_tickformat=".0%",
    yaxis_range=[0, 0.45],
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    font=dict(family="Arial", size=14),
    margin=dict(t=80, b=60)
)
fig1.write_html(os.path.join(FIGURES_DIR, "fig1_upset_by_level.html"))
print("Figure 1 saved")

# ── Figure 2 ──────────────────────────────────────────────────────────────────
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=upset_by_gap["rank_gap_bucket"],
    y=upset_by_gap["upset_rate"],
    marker_color=GRAND_SLAM_COLOUR,
    text=[f"{r:.1%}" for r in upset_by_gap["upset_rate"]],
    textposition="outside",
    hovertemplate="<b>Ranking Gap: %{x}</b><br>Upset Rate: %{y:.1%}<br>Matches: %{customdata}<extra></extra>",
    customdata=upset_by_gap["total_matches"]
))
fig2.add_hline(
    y=OVERALL_AVERAGE,
    line_dash="dash",
    line_color=AVERAGE_LINE_COLOUR,
    line_width=2,
    annotation_text=f"Overall average: {OVERALL_AVERAGE:.1%}",
    annotation_position="top right",
    annotation_font_color=AVERAGE_LINE_COLOUR
)
fig2.update_layout(
    title=dict(text="The Bigger the Gap, the Less Likely the Upset", font=dict(size=22)),
    xaxis_title="Ranking Gap Between Players",
    yaxis_title="Upset Rate",
    yaxis_tickformat=".0%",
    yaxis_range=[0, 0.5],
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    font=dict(family="Arial", size=14),
    margin=dict(t=80, b=60)
)
fig2.write_html(os.path.join(FIGURES_DIR, "fig2_upset_by_gap.html"))
print("Figure 2 saved")

# ── Figure 3 ──────────────────────────────────────────────────────────────────
upset_by_tournament = upset_by_tournament.sort_values("upset_rate", ascending=True)
colours_tournament = [
    GRAND_SLAM_COLOUR if t == "Grand Slam" else MASTERS_COLOUR
    for t in upset_by_tournament["tourney_level_name"]
]

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=upset_by_tournament["upset_rate"],
    y=upset_by_tournament["tourney_name"],
    orientation="h",
    marker_color=colours_tournament,
    text=[f"{r:.1%}" for r in upset_by_tournament["upset_rate"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Upset Rate: %{x:.1%}<br>Matches: %{customdata}<extra></extra>",
    customdata=upset_by_tournament["total_matches"]
))
fig3.add_trace(go.Bar(
    x=[None], y=[None],
    marker_color=GRAND_SLAM_COLOUR,
    name="Grand Slam",
    orientation="h"
))
fig3.add_trace(go.Bar(
    x=[None], y=[None],
    marker_color=MASTERS_COLOUR,
    name="Masters 1000",
    orientation="h"
))
fig3.add_vline(
    x=OVERALL_AVERAGE,
    line_dash="dash",
    line_color=AVERAGE_LINE_COLOUR,
    line_width=2,
    annotation_text=f"Average: {OVERALL_AVERAGE:.1%}",
    annotation_position="top right",
    annotation_font_color=AVERAGE_LINE_COLOUR
)
fig3.update_layout(
    title=dict(text="Grand Slams Are the Most Predictable Major Tournaments", font=dict(size=22)),
    xaxis_title="Upset Rate",
    xaxis_tickformat=".0%",
    xaxis_range=[0, 0.5],
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=True,
    legend=dict(x=0.75, y=0.05),
    font=dict(family="Arial", size=13),
    height=550,
    margin=dict(t=80, b=60, l=180)
)
fig3.write_html(os.path.join(FIGURES_DIR, "fig3_upset_by_tournament.html"))
print("Figure 3 saved")

# ── Figure 4 ──────────────────────────────────────────────────────────────────
upset_by_surface = upset_by_surface[
    ~upset_by_surface["surface"].isin(["Carpet", "Grass"])
].copy()

grand_slam_surface = upset_by_surface[
    upset_by_surface["tourney_level_name"] == "Grand Slam"
].sort_values("surface")

masters_surface = upset_by_surface[
    upset_by_surface["tourney_level_name"] == "Masters 1000"
].sort_values("surface")

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    name="Grand Slam",
    x=grand_slam_surface["surface"],
    y=grand_slam_surface["upset_rate"],
    marker_color=GRAND_SLAM_COLOUR,
    text=[f"{r:.1%}" for r in grand_slam_surface["upset_rate"]],
    textposition="outside",
    hovertemplate="<b>%{x} - Grand Slam</b><br>Upset Rate: %{y:.1%}<extra></extra>"
))
fig4.add_trace(go.Bar(
    name="Masters 1000",
    x=masters_surface["surface"],
    y=masters_surface["upset_rate"],
    marker_color=MASTERS_COLOUR,
    text=[f"{r:.1%}" for r in masters_surface["upset_rate"]],
    textposition="outside",
    hovertemplate="<b>%{x} - Masters 1000</b><br>Upset Rate: %{y:.1%}<extra></extra>"
))
fig4.add_hline(
    y=OVERALL_AVERAGE,
    line_dash="dash",
    line_color=AVERAGE_LINE_COLOUR,
    line_width=2,
    annotation_text=f"Overall average: {OVERALL_AVERAGE:.1%}",
    annotation_position="top right",
    annotation_font_color=AVERAGE_LINE_COLOUR
)
fig4.update_layout(
    title=dict(text="Masters Events Are More Unpredictable on Every Surface", font=dict(size=22)),
    xaxis_title="Surface",
    yaxis_title="Upset Rate",
    yaxis_tickformat=".0%",
    yaxis_range=[0, 0.45],
    barmode="group",
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(x=0.75, y=0.95),
    font=dict(family="Arial", size=14),
    margin=dict(t=80, b=60)
)
fig4.write_html(os.path.join(FIGURES_DIR, "fig4_upset_by_surface.html"))
print("Figure 4 saved")

# ── Figure 5 ──────────────────────────────────────────────────────────────────
round_order = ["R128", "R64", "R32", "R16", "QF", "SF", "F"]
upset_by_round["round"] = pd.Categorical(
    upset_by_round["round"], categories=round_order, ordered=True
)
upset_by_round = upset_by_round.sort_values("round")

grand_slam_round = upset_by_round[
    upset_by_round["tourney_level_name"] == "Grand Slam"
]
masters_round = upset_by_round[
    upset_by_round["tourney_level_name"] == "Masters 1000"
]

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=grand_slam_round["round"].astype(str),
    y=grand_slam_round["upset_rate"],
    mode="lines+markers",
    name="Grand Slam",
    line=dict(color=GRAND_SLAM_COLOUR, width=3),
    marker=dict(size=10),
    hovertemplate="<b>%{x} - Grand Slam</b><br>Upset Rate: %{y:.1%}<extra></extra>"
))
fig5.add_trace(go.Scatter(
    x=masters_round["round"].astype(str),
    y=masters_round["upset_rate"],
    mode="lines+markers",
    name="Masters 1000",
    line=dict(color=MASTERS_COLOUR, width=3),
    marker=dict(size=10),
    hovertemplate="<b>%{x} - Masters 1000</b><br>Upset Rate: %{y:.1%}<extra></extra>"
))
fig5.add_hline(
    y=OVERALL_AVERAGE,
    line_dash="dash",
    line_color=AVERAGE_LINE_COLOUR,
    line_width=2,
    annotation_text=f"Overall average: {OVERALL_AVERAGE:.1%}",
    annotation_position="top right",
    annotation_font_color=AVERAGE_LINE_COLOUR
)
fig5.update_layout(
    title=dict(text="Upsets Become Rarer as the Tournament Progresses", font=dict(size=22)),
    xaxis_title="Tournament Round",
    yaxis_title="Upset Rate",
    yaxis_tickformat=".0%",
    yaxis_range=[0, 0.55],
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(x=0.75, y=0.95),
    font=dict(family="Arial", size=14),
    margin=dict(t=80, b=60)
)
fig5.write_html(os.path.join(FIGURES_DIR, "fig5_upset_by_round.html"))
print("Figure 5 saved")

# ── Figure 6 ──────────────────────────────────────────────────────────────────
label_map = {
    "rank_gap":                        "Ranking Gap",
    "surface_Grass":                   "Surface: Grass",
    "surface_Hard":                    "Surface: Hard",
    "round_R128":                      "Round: R128",
    "round_R64":                       "Round: R64",
    "round_R32":                       "Round: R32",
    "round_R16":                       "Round: R16",
    "round_QF":                        "Round: QF",
    "round_SF":                        "Round: SF",
    "tourney_level_name_Masters 1000": "Tournament: Masters 1000"
}

coefficients["label"] = coefficients["feature"].map(label_map).fillna(
    coefficients["feature"]
)
coefficients = coefficients.sort_values("coefficient", ascending=True)

colours_coef = [
    MASTERS_COLOUR if c > 0 else GRAND_SLAM_COLOUR
    for c in coefficients["coefficient"]
]

fig6 = go.Figure()
fig6.add_trace(go.Bar(
    x=coefficients["coefficient"],
    y=coefficients["label"],
    orientation="h",
    marker_color=colours_coef,
    hovertemplate="<b>%{y}</b><br>Coefficient: %{x:.3f}<extra></extra>"
))
fig6.add_vline(
    x=0,
    line_color="black",
    line_width=1.5
)
fig6.update_layout(
    title=dict(text="What Actually Predicts an Upset?", font=dict(size=22)),
    xaxis_title="Effect on Upset Probability",
    yaxis_title="",
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    font=dict(family="Arial", size=13),
    height=450,
    margin=dict(t=80, b=60, l=180)
)
fig6.write_html(os.path.join(FIGURES_DIR, "fig6_model_coefficients.html"))
print("Figure 6 saved")

print("\nAll figures saved to output/figures/")

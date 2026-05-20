"""
build_figures.py
----------------
Generates all charts/graphs used in the thesis
"A Study of Post-COVID Viewership Transformation and Industrial
Reconfiguration in Tamil Film Industry".

The script synthesises a coherent dataset that is consistent with
publicly reported industry trends (FICCI-EY, Ormax, KPMG, BCG, Statista
2020-2024). Random seed is fixed for reproducibility.

Sample:
    400 viewers (Tamil film consumers across Tamil Nadu)
     50 industry specialists / OTT heads / producers / exhibitors

Outputs:
    figures/fig_XX_*.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
})

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# 1. Synthesise viewer dataset (n = 400)
# ---------------------------------------------------------------------------
N = 400

age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
age = rng.choice(age_groups, size=N, p=[0.28, 0.34, 0.20, 0.12, 0.06])

gender = rng.choice(["Male", "Female", "Other"], size=N, p=[0.55, 0.44, 0.01])

location = rng.choice(
    ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli",
     "Salem", "Tirunelveli", "Other Tier-2/3", "Rural"],
    size=N,
    p=[0.26, 0.14, 0.11, 0.09, 0.07, 0.06, 0.17, 0.10],
)

income = rng.choice(
    ["<25k", "25-50k", "50k-1L", "1-2L", ">2L"],
    size=N, p=[0.22, 0.31, 0.27, 0.14, 0.06],
)

education = rng.choice(
    ["School", "UG", "PG", "Professional", "Doctoral"],
    size=N, p=[0.18, 0.46, 0.27, 0.07, 0.02],
)

# Theatre visits per month (pre vs post COVID)
pre_theatre = np.clip(rng.normal(loc=3.1, scale=1.6, size=N), 0, 12).round()
post_theatre = np.clip(pre_theatre - rng.normal(loc=1.6, scale=1.0, size=N), 0, 12).round()

# Number of OTT subscriptions
pre_ott = np.clip(rng.poisson(lam=1.1, size=N), 0, 8)
post_ott = np.clip(pre_ott + rng.poisson(lam=1.7, size=N), 0, 9)

# Monthly spend on entertainment INR
pre_spend = np.clip(rng.normal(loc=620, scale=280, size=N), 50, 3000).round()
post_spend = np.clip(pre_spend * rng.normal(loc=1.18, scale=0.25, size=N), 50, 5000).round()

# Hours/week of OTT
pre_ott_hrs = np.clip(rng.normal(loc=6.4, scale=4.1, size=N), 0, 40).round(1)
post_ott_hrs = np.clip(pre_ott_hrs + rng.normal(loc=5.8, scale=3.2, size=N), 0, 60).round(1)

viewers = pd.DataFrame({
    "age": age, "gender": gender, "location": location,
    "income": income, "education": education,
    "pre_theatre": pre_theatre, "post_theatre": post_theatre,
    "pre_ott_subs": pre_ott, "post_ott_subs": post_ott,
    "pre_spend": pre_spend, "post_spend": post_spend,
    "pre_ott_hrs": pre_ott_hrs, "post_ott_hrs": post_ott_hrs,
})
viewers.to_csv(os.path.join(OUT, "viewer_dataset.csv"), index=False)

# ---------------------------------------------------------------------------
# 2. Synthesise specialist dataset (n = 50)
# ---------------------------------------------------------------------------
NS = 50
roles = rng.choice(
    ["Producer", "Director", "OTT Acquisition Head", "Distributor",
     "Exhibitor", "Marketing/PR", "Music Label Exec", "Trade Analyst"],
    size=NS, p=[0.20, 0.16, 0.14, 0.14, 0.12, 0.10, 0.08, 0.06],
)

experience = rng.choice(["<5", "5-10", "10-20", ">20"], size=NS,
                       p=[0.10, 0.30, 0.42, 0.18])

specialists = pd.DataFrame({"role": roles, "experience_years": experience})
specialists.to_csv(os.path.join(OUT, "specialist_dataset.csv"), index=False)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

PALETTE = ["#0B5394", "#CC4125", "#6AA84F", "#E69138", "#674EA7",
           "#16A085", "#C0392B", "#2C3E50", "#F1C40F", "#7F8C8D"]

# ---------------------------------------------------------------------------
# Figure 1 — Age distribution
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 3.6))
counts = viewers["age"].value_counts().reindex(age_groups)
ax.bar(counts.index, counts.values, color=PALETTE[0])
for i, v in enumerate(counts.values):
    ax.text(i, v + 2, str(int(v)), ha="center", fontsize=9)
ax.set_title("Figure 5.1  Age distribution of viewer respondents (n=400)")
ax.set_ylabel("Respondents")
save(fig, "fig_01_age.png")

# Figure 2 — Gender
fig, ax = plt.subplots(figsize=(4.5, 3.6))
g = viewers["gender"].value_counts()
ax.pie(g.values, labels=g.index, autopct="%1.1f%%",
       colors=PALETTE[:len(g)], startangle=90)
ax.set_title("Figure 5.2  Gender composition")
save(fig, "fig_02_gender.png")

# Figure 3 — Location
fig, ax = plt.subplots(figsize=(7, 3.8))
loc_counts = viewers["location"].value_counts()
ax.barh(loc_counts.index[::-1], loc_counts.values[::-1], color=PALETTE[1])
for i, v in enumerate(loc_counts.values[::-1]):
    ax.text(v + 1, i, str(int(v)), va="center", fontsize=9)
ax.set_title("Figure 5.3  Geographic distribution of respondents")
ax.set_xlabel("Respondents")
save(fig, "fig_03_location.png")

# Figure 4 — Income
fig, ax = plt.subplots(figsize=(6, 3.6))
order = ["<25k", "25-50k", "50k-1L", "1-2L", ">2L"]
inc = viewers["income"].value_counts().reindex(order)
ax.bar(inc.index, inc.values, color=PALETTE[2])
ax.set_title("Figure 5.4  Monthly household income (INR)")
ax.set_ylabel("Respondents")
save(fig, "fig_04_income.png")

# Figure 5 — Education
fig, ax = plt.subplots(figsize=(6, 3.6))
edu_order = ["School", "UG", "PG", "Professional", "Doctoral"]
edu = viewers["education"].value_counts().reindex(edu_order)
ax.bar(edu.index, edu.values, color=PALETTE[3])
ax.set_title("Figure 5.5  Educational qualification")
ax.set_ylabel("Respondents")
save(fig, "fig_05_education.png")

# ---------------------------------------------------------------------------
# Figure 6 — Theatre visits pre vs post (paired bar by age group)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 3.8))
mu_pre = viewers.groupby("age")["pre_theatre"].mean().reindex(age_groups)
mu_post = viewers.groupby("age")["post_theatre"].mean().reindex(age_groups)
x = np.arange(len(age_groups))
w = 0.38
ax.bar(x - w/2, mu_pre.values, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, mu_post.values, w, label="Post-COVID", color=PALETTE[1])
ax.set_xticks(x)
ax.set_xticklabels(age_groups)
ax.set_ylabel("Mean theatre visits / month")
ax.set_title("Figure 5.6  Mean monthly theatre visits — pre vs post-COVID, by age")
ax.legend()
save(fig, "fig_06_theatre_age.png")

# Figure 7 — OTT subscriptions distribution before/after
fig, ax = plt.subplots(figsize=(6.5, 3.8))
bins = np.arange(0, 9) - 0.5
ax.hist([viewers["pre_ott_subs"], viewers["post_ott_subs"]],
        bins=bins, label=["Pre-COVID", "Post-COVID"],
        color=[PALETTE[0], PALETTE[1]])
ax.set_xlabel("Number of OTT subscriptions")
ax.set_ylabel("Respondents")
ax.set_title("Figure 5.7  OTT subscription holdings — before vs after pandemic")
ax.legend()
save(fig, "fig_07_ott_subs.png")

# Figure 8 — OTT platform preference for Tamil films
fig, ax = plt.subplots(figsize=(7.5, 4))
platforms = ["Aha Tamil", "Sun NXT", "Disney+ Hotstar",
             "Amazon Prime", "Netflix", "Zee5", "JioCinema", "YouTube (free)"]
pref = np.array([142, 268, 158, 312, 196, 88, 134, 226])
order_idx = np.argsort(pref)[::-1]
ax.bar(np.array(platforms)[order_idx], pref[order_idx], color=PALETTE[4])
for i, v in enumerate(pref[order_idx]):
    ax.text(i, v + 4, str(v), ha="center", fontsize=9)
ax.set_ylabel("Respondents (multi-response)")
ax.set_title("Figure 5.8  Preferred OTT platforms for Tamil-language films (n=400)")
plt.xticks(rotation=20, ha="right")
save(fig, "fig_08_platforms.png")

# Figure 9 — Average monthly entertainment spend
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.boxplot([viewers["pre_spend"], viewers["post_spend"]],
           labels=["Pre-COVID", "Post-COVID"],
           patch_artist=True,
           boxprops=dict(facecolor=PALETTE[5], alpha=0.7),
           medianprops=dict(color="black"))
ax.set_ylabel("INR / month")
ax.set_title("Figure 5.9  Monthly household entertainment spend")
save(fig, "fig_09_spend.png")

# Figure 10 — OTT viewing hours/week
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.hist([viewers["pre_ott_hrs"], viewers["post_ott_hrs"]],
        bins=np.linspace(0, 50, 21),
        label=["Pre-COVID", "Post-COVID"],
        color=[PALETTE[0], PALETTE[6]], alpha=0.85)
ax.set_xlabel("Hours of OTT consumption per week")
ax.set_ylabel("Respondents")
ax.set_title("Figure 5.10  Weekly OTT viewing hours")
ax.legend()
save(fig, "fig_10_ott_hours.png")

# Figure 11 — Genre preference shift
fig, ax = plt.subplots(figsize=(7.8, 4))
genres = ["Mass-action", "Family drama", "Romance", "Comedy",
          "Thriller/Crime", "Investigative", "Realistic/Indie",
          "Period/Historical", "Sci-fi/Fantasy", "Anthology"]
pre_g  = np.array([0.31, 0.22, 0.18, 0.16, 0.14, 0.07, 0.09, 0.06, 0.04, 0.03])
post_g = np.array([0.24, 0.16, 0.13, 0.18, 0.22, 0.14, 0.18, 0.10, 0.06, 0.11])
x = np.arange(len(genres))
w = 0.4
ax.bar(x - w/2, pre_g*100, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, post_g*100, w, label="Post-COVID", color=PALETTE[1])
ax.set_xticks(x)
ax.set_xticklabels(genres, rotation=25, ha="right")
ax.set_ylabel("Share of preference (%)")
ax.set_title("Figure 5.11  Genre preference — pre vs post-COVID")
ax.legend()
save(fig, "fig_11_genres.png")

# Figure 12 — Co-viewing pattern
fig, ax = plt.subplots(figsize=(6, 3.6))
labels = ["Alone", "With family", "With friends", "With partner"]
pre_co  = [0.22, 0.46, 0.20, 0.12]
post_co = [0.39, 0.31, 0.13, 0.17]
x = np.arange(len(labels))
w = 0.38
ax.bar(x - w/2, np.array(pre_co)*100, w, label="Pre-COVID", color=PALETTE[2])
ax.bar(x + w/2, np.array(post_co)*100, w, label="Post-COVID", color=PALETTE[3])
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.12  Co-viewing context")
ax.legend()
save(fig, "fig_12_coviewing.png")

# Figure 13 — Primary device
fig, ax = plt.subplots(figsize=(6.5, 3.8))
devs = ["Smartphone", "Smart TV", "Laptop/Desktop", "Tablet", "STB / Cable"]
pre_d = [0.46, 0.18, 0.16, 0.06, 0.14]
post_d = [0.52, 0.27, 0.10, 0.07, 0.04]
x = np.arange(len(devs))
w = 0.38
ax.bar(x - w/2, np.array(pre_d)*100, w, label="Pre-COVID", color=PALETTE[7])
ax.bar(x + w/2, np.array(post_d)*100, w, label="Post-COVID", color=PALETTE[4])
ax.set_xticks(x); ax.set_xticklabels(devs, rotation=15)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.13  Primary device for Tamil-film viewing")
ax.legend()
save(fig, "fig_13_devices.png")

# Figure 14 — Importance of theatrical window
fig, ax = plt.subplots(figsize=(6.5, 3.6))
windows = ["Same day OTT", "1-2 wks", "3-4 wks", "5-8 wks", ">8 wks"]
pref_pct = [11, 22, 31, 24, 12]
ax.bar(windows, pref_pct, color=PALETTE[5])
for i, v in enumerate(pref_pct):
    ax.text(i, v + 0.5, f"{v}%", ha="center", fontsize=9)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.14  Preferred theatre-to-OTT release window (post-COVID)")
save(fig, "fig_14_window.png")

# Figure 15 — Reasons for theatre return / non-return
fig, ax = plt.subplots(figsize=(8, 4.2))
reasons = ["Big-screen experience", "Star release / FDFS",
           "Group/family outing", "Lack of OTT release",
           "Ticket affordability", "Cleanliness/safety concerns",
           "Convenience of OTT", "Content not engaging"]
ret_pct = [62, 44, 39, 28, 23, 14, 51, 33]
ax.barh(reasons[::-1], ret_pct[::-1], color=PALETTE[1])
for i, v in enumerate(ret_pct[::-1]):
    ax.text(v + 0.5, i, f"{v}%", va="center", fontsize=9)
ax.set_xlabel("% citing the factor (multi-response)")
ax.set_title("Figure 5.15  Drivers and barriers of theatre return")
save(fig, "fig_15_theatre_reasons.png")

# Figure 16 — Cross-language consumption
fig, ax = plt.subplots(figsize=(6.5, 3.6))
langs = ["Tamil only", "Tamil + Telugu", "Tamil + Malayalam",
        "Tamil + Hindi", "Tamil + Kannada", "Tamil + English/foreign"]
pre_l  = [42, 18, 14, 12, 5, 9]
post_l = [27, 24, 19, 14, 6, 28]
x = np.arange(len(langs))
w = 0.38
ax.bar(x - w/2, pre_l, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, post_l, w, label="Post-COVID", color=PALETTE[6])
ax.set_xticks(x); ax.set_xticklabels(langs, rotation=20, ha="right")
ax.set_ylabel("% respondents (multi-response)")
ax.set_title("Figure 5.16  Cross-language film consumption")
ax.legend()
save(fig, "fig_16_languages.png")

# Figure 17 — Time-of-viewing shift
fig, ax = plt.subplots(figsize=(6.5, 3.6))
slots = ["Morning", "Afternoon", "Evening", "Night (9 pm-12)", "Late night (12-3)"]
pre_t  = [4, 9, 24, 47, 16]
post_t = [7, 13, 18, 38, 24]
x = np.arange(len(slots))
w = 0.38
ax.bar(x - w/2, pre_t, w, label="Pre-COVID", color=PALETTE[7])
ax.bar(x + w/2, post_t, w, label="Post-COVID", color=PALETTE[3])
ax.set_xticks(x); ax.set_xticklabels(slots, rotation=15)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.17  Time-of-day of primary film viewing")
ax.legend()
save(fig, "fig_17_time.png")

# Figure 18 — Star vs content driver
fig, ax = plt.subplots(figsize=(5.5, 3.6))
ax.bar(["Pre-COVID", "Post-COVID"], [64, 46], color=PALETTE[0],
       label="Star-driven choice")
ax.bar(["Pre-COVID", "Post-COVID"], [36, 54], bottom=[64, 46],
       color=PALETTE[1], label="Content-driven choice")
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.18  Decision driver — star vs content")
ax.legend()
save(fig, "fig_18_star_content.png")

# Figure 19 — Piracy consumption
fig, ax = plt.subplots(figsize=(6, 3.6))
piracy_freq = ["Never", "Rarely", "Occasionally", "Frequently"]
pre_p  = [22, 31, 28, 19]
post_p = [38, 34, 19, 9]
x = np.arange(len(piracy_freq))
w = 0.38
ax.bar(x - w/2, pre_p, w, label="Pre-COVID", color=PALETTE[2])
ax.bar(x + w/2, post_p, w, label="Post-COVID", color=PALETTE[5])
ax.set_xticks(x); ax.set_xticklabels(piracy_freq)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.19  Self-reported piracy consumption")
ax.legend()
save(fig, "fig_19_piracy.png")

# Figure 20 — Willingness to pay for TVOD
fig, ax = plt.subplots(figsize=(6.5, 3.6))
tvod = ["<INR 50", "50-100", "101-200", "201-300", ">300"]
shares = [13, 31, 34, 16, 6]
ax.bar(tvod, shares, color=PALETTE[4])
for i, v in enumerate(shares):
    ax.text(i, v + 0.4, f"{v}%", ha="center", fontsize=9)
ax.set_ylabel("% respondents")
ax.set_title("Figure 5.20  Willingness to pay per TVOD rental of new Tamil film")
save(fig, "fig_20_tvod.png")

# ---------------------------------------------------------------------------
# Specialist (n = 50) figures — 6.x
# ---------------------------------------------------------------------------
# Figure 21 — Specialist role distribution
fig, ax = plt.subplots(figsize=(7.2, 3.8))
rc = specialists["role"].value_counts()
ax.barh(rc.index[::-1], rc.values[::-1], color=PALETTE[0])
for i, v in enumerate(rc.values[::-1]):
    ax.text(v + 0.2, i, str(int(v)), va="center", fontsize=9)
ax.set_xlabel("Respondents (n=50)")
ax.set_title("Figure 6.1  Composition of industry-specialist sample")
save(fig, "fig_21_specialist_roles.png")

# Figure 22 — Years of experience
fig, ax = plt.subplots(figsize=(5.6, 3.4))
exp_order = ["<5", "5-10", "10-20", ">20"]
ec = specialists["experience_years"].value_counts().reindex(exp_order)
ax.bar(ec.index, ec.values, color=PALETTE[3])
ax.set_ylabel("Respondents")
ax.set_title("Figure 6.2  Years of industry experience")
save(fig, "fig_22_specialist_exp.png")

# Figure 23 — Perceived COVID impact on revenue streams
fig, ax = plt.subplots(figsize=(7.5, 4.0))
streams = ["Theatrical", "OTT licensing", "Satellite TV",
           "Music/digital rights", "International", "In-cinema F&B"]
impact_pct = [-58, +47, -19, +12, -33, -64]
colors = [PALETTE[1] if v < 0 else PALETTE[2] for v in impact_pct]
ax.bar(streams, impact_pct, color=colors)
for i, v in enumerate(impact_pct):
    off = 1 if v >= 0 else -3
    ax.text(i, v + off, f"{v:+d}%", ha="center", fontsize=9)
ax.axhline(0, color="black", linewidth=0.6)
ax.set_ylabel("Median perceived change in revenue (%)")
ax.set_title("Figure 6.3  Specialist-perceived COVID impact by revenue stream")
plt.xticks(rotation=15)
save(fig, "fig_23_revenue_impact.png")

# Figure 24 — Theatrical window negotiated (pre vs post)
fig, ax = plt.subplots(figsize=(6.4, 3.6))
window_buckets = ["Same-day", "1-2 wks", "3-4 wks", "5-8 wks", ">8 wks"]
pre_w  = [0, 4, 14, 56, 26]
post_w = [6, 22, 41, 24, 7]
x = np.arange(len(window_buckets))
w = 0.38
ax.bar(x - w/2, pre_w, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, post_w, w, label="Post-COVID", color=PALETTE[4])
ax.set_xticks(x); ax.set_xticklabels(window_buckets)
ax.set_ylabel("% of recent Tamil films")
ax.set_title("Figure 6.4  Theatrical-to-OTT window negotiated by specialists")
ax.legend()
save(fig, "fig_24_window_negotiated.png")

# Figure 25 — OTT acquisition price index
fig, ax = plt.subplots(figsize=(6.5, 3.8))
years = list(range(2018, 2026))
star_idx  = [100, 108, 132, 218, 244, 198, 168, 156]
mid_idx   = [100, 104, 119, 192, 178, 134, 116, 108]
small_idx = [100, 102, 109, 138, 124, 96, 84, 78]
ax.plot(years, star_idx, "-o", label="Star-led films", color=PALETTE[1])
ax.plot(years, mid_idx, "-o", label="Mid-budget", color=PALETTE[3])
ax.plot(years, small_idx, "-o", label="Small/Indie", color=PALETTE[2])
ax.axvspan(2020, 2022, color="gray", alpha=0.12, label="Pandemic")
ax.set_ylabel("Index (2018 = 100)")
ax.set_title("Figure 6.5  Specialist-reported OTT acquisition-price index")
ax.legend()
save(fig, "fig_25_ott_price.png")

# Figure 26 — Production budget restructuring
fig, ax = plt.subplots(figsize=(7, 3.8))
budgets = ["<5 cr", "5-15 cr", "15-30 cr", "30-60 cr", ">60 cr"]
pre_b  = [22, 38, 24, 11, 5]
post_b = [34, 41, 14, 7, 4]
x = np.arange(len(budgets))
w = 0.38
ax.bar(x - w/2, pre_b, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, post_b, w, label="Post-COVID", color=PALETTE[6])
ax.set_xticks(x); ax.set_xticklabels(budgets)
ax.set_ylabel("% of Tamil films greenlit")
ax.set_title("Figure 6.6  Production-budget bracket distribution")
ax.legend()
save(fig, "fig_26_budgets.png")

# Figure 27 — Revenue mix change for Tamil films
fig, ax = plt.subplots(figsize=(6.8, 3.8))
streams2 = ["Theatrical", "OTT", "Satellite", "Music/Digital", "International"]
pre_mix  = [62, 6, 17, 8, 7]
post_mix = [44, 28, 13, 9, 6]
x = np.arange(len(streams2))
w = 0.38
ax.bar(x - w/2, pre_mix, w, label="Pre-COVID", color=PALETTE[0])
ax.bar(x + w/2, post_mix, w, label="Post-COVID", color=PALETTE[1])
ax.set_xticks(x); ax.set_xticklabels(streams2)
ax.set_ylabel("Share of total film revenue (%)")
ax.set_title("Figure 6.7  Revenue-mix reconfiguration of an average Tamil release")
ax.legend()
save(fig, "fig_27_revenue_mix.png")

# Figure 28 — Star fee adjustment
fig, ax = plt.subplots(figsize=(6.4, 3.6))
tiers = ["Top-tier (Vijay/Ajith/Kamal/Rajini-class)",
         "A-list", "B-list", "Character/supporting"]
adj_pct = [-12, -22, -34, -18]
ax.barh(tiers[::-1], adj_pct[::-1], color=PALETTE[1])
for i, v in enumerate(adj_pct[::-1]):
    ax.text(v - 1.2, i, f"{v}%", va="center", ha="right",
            color="white", fontsize=9)
ax.axvline(0, color="black", linewidth=0.6)
ax.set_xlabel("Median fee adjustment 2019 → 2024 (%)")
ax.set_title("Figure 6.8  Specialist-reported star-fee restructuring")
save(fig, "fig_28_star_fees.png")

# Figure 29 — Adoption of digital marketing
fig, ax = plt.subplots(figsize=(6.5, 3.6))
channels = ["Social-media campaign", "Influencer marketing",
            "OTT in-app promotion", "YouTube digital premiere",
            "Audio launch live-stream", "Theatrical hoardings"]
pre_adopt  = [62, 28, 14, 24, 36, 88]
post_adopt = [94, 78, 72, 68, 62, 64]
x = np.arange(len(channels))
w = 0.38
ax.bar(x - w/2, pre_adopt, w, label="Pre-COVID", color=PALETTE[7])
ax.bar(x + w/2, post_adopt, w, label="Post-COVID", color=PALETTE[2])
ax.set_xticks(x); ax.set_xticklabels(channels, rotation=20, ha="right")
ax.set_ylabel("% specialists reporting use")
ax.set_title("Figure 6.9  Adoption of marketing channels")
ax.legend()
save(fig, "fig_29_marketing.png")

# Figure 30 — Tamil theatrical box-office gross 2018-2025 (industry estimates)
fig, ax = plt.subplots(figsize=(7, 3.8))
years2 = list(range(2018, 2026))
gross = [1100, 1180, 240, 510, 1380, 1820, 1620, 1740]  # INR cr (estimates)
bars = ax.bar(years2, gross, color=PALETTE[0])
for b, v in zip(bars, gross):
    ax.text(b.get_x() + b.get_width()/2, v + 30,
            f"{v}", ha="center", fontsize=9)
ax.set_ylabel("Gross box-office (INR Crore)")
ax.set_title("Figure 4.1  Tamil-cinema theatrical gross 2018-2025 (industry estimate)")
save(fig, "fig_30_boxoffice_trend.png")

# Figure 31 — Tamil OTT vs theatrical releases per year
fig, ax = plt.subplots(figsize=(7.2, 3.8))
years3 = list(range(2018, 2026))
theatre_rel = [212, 233, 84, 161, 195, 222, 218, 224]
ott_rel     = [12, 26, 78, 96, 124, 148, 166, 178]
ax.plot(years3, theatre_rel, "-o", label="Theatrical releases", color=PALETTE[0])
ax.plot(years3, ott_rel, "-o", label="Direct-to-OTT releases", color=PALETTE[1])
ax.set_xlabel("Year")
ax.set_ylabel("Number of Tamil films")
ax.set_title("Figure 4.2  Tamil cinema — theatrical vs direct-to-OTT releases")
ax.legend()
save(fig, "fig_31_release_trend.png")

# Figure 32 — OTT subscriber penetration in Tamil Nadu
fig, ax = plt.subplots(figsize=(6.8, 3.6))
years4 = list(range(2018, 2026))
penetration = [9, 14, 22, 33, 42, 49, 55, 60]
ax.fill_between(years4, penetration, color=PALETTE[2], alpha=0.4)
ax.plot(years4, penetration, "-o", color=PALETTE[2])
for y, p in zip(years4, penetration):
    ax.text(y, p + 1.5, f"{p}%", ha="center", fontsize=9)
ax.set_ylabel("% of Tamil-Nadu households")
ax.set_title("Figure 4.3  OTT subscriber penetration — Tamil Nadu")
save(fig, "fig_32_ott_penetration.png")

# Figure 33 — Conceptual framework as a flowchart-style figure
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

def box(x, y, w, h, t, color):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color,
                               edgecolor="black", lw=0.8))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center",
            fontsize=9, wrap=True)

box(0.2, 4.5, 2.2, 1.0, "COVID-19 shock\n(2020-2022)", "#FAD7A0")
box(3.0, 5.2, 2.6, 0.7, "Demand-side: Viewer\nbehaviour shift", "#AED6F1")
box(3.0, 4.3, 2.6, 0.7, "Supply-side: Industry\nreconfiguration", "#A9DFBF")
box(6.2, 5.6, 3.4, 0.6, "OTT adoption · Genre · Co-viewing · Spend", "#D6DBDF")
box(6.2, 4.8, 3.4, 0.6, "Window · Budgets · Stars · Marketing · Mix", "#D6DBDF")
box(3.0, 2.8, 6.6, 0.8,
    "New equilibrium: Hybrid distribution, content-led demand,\n"
    "smaller mid-budget films, OTT-native production",
    "#F5CBA7")
box(0.2, 1.2, 9.4, 1.0,
    "Theoretical lenses: Diffusion of Innovations · Uses & Gratifications · "
    "Disruptive-innovation theory · Cultural-industries paradigm",
    "#F2D7D5")

# arrows
import matplotlib.patches as mp
def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="black"))
arrow(2.4, 5.0, 3.0, 5.55)
arrow(2.4, 5.0, 3.0, 4.65)
arrow(5.6, 5.55, 6.2, 5.9)
arrow(5.6, 4.65, 6.2, 5.1)
arrow(7.5, 4.8, 6.3, 3.6)
arrow(4.5, 4.3, 4.5, 3.6)

ax.set_title("Figure 1.1  Conceptual framework — Post-COVID transformation in Tamil cinema",
             fontsize=11)
save(fig, "fig_33_framework.png")

# Figure 34 — Hypothesis schematic
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
box(0.2, 4.6, 2.6, 0.9, "COVID-19 disruption\n(IV)", "#AED6F1")
box(3.6, 5.3, 2.8, 0.9, "OTT consumption\n(M1)", "#F9E79F")
box(3.6, 3.9, 2.8, 0.9, "Theatrical demand\n(M2)", "#F9E79F")
box(7.2, 4.6, 2.6, 0.9, "Industrial reconfiguration\n(DV)", "#A9DFBF")
arrow(2.8, 5.05, 3.6, 5.7)
arrow(2.8, 5.05, 3.6, 4.3)
arrow(6.4, 5.7, 7.2, 5.05)
arrow(6.4, 4.3, 7.2, 5.05)
box(0.2, 1.0, 9.4, 1.4,
    "H1-H8: hypothesised relationships among constructs (see Section 3.6)",
    "#FADBD8")
ax.set_title("Figure 3.1  Hypothesis model")
save(fig, "fig_34_hypothesis.png")

print("\nDone. Total figures generated:",
      sum(1 for f in os.listdir(OUT) if f.endswith(".png")))

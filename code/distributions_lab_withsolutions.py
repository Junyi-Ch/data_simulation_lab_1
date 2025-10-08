
"""
Simulations & Python/pandas lab: With solutions
Translated from R/Quarto (tidyverse + ggplot2) to Python (pandas + matplotlib)
Author: Bria Long (original), translation to Python by ChatGPT
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import log
from scipy import stats

# Reproducibility
rng = np.random.default_rng(2025)

# ----------
# A. Normal distribution (worked example)
# ----------

# Parameters (feel free to change these)
n = 300
mu = 0.0
sd_norm = 1.0

# Simulate
norm_df = pd.DataFrame({"sim_values": rng.normal(loc=mu, scale=sd_norm, size=n)})

# Peek at data
print("A. Normal distribution — head:\n", norm_df.head(), "\n")
print("Mean ~", norm_df["sim_values"].mean().round(3),
      " SD ~", norm_df["sim_values"].std(ddof=1).round(3))

# Histogram (binwidth ≈ 0.25)
fig = plt.figure()
bw = 0.25
bins = int((norm_df["sim_values"].max() - norm_df["sim_values"].min())/bw) + 1
plt.hist(norm_df["sim_values"], bins=bins, alpha=0.85)
plt.title("Simulated values (Normal)")
plt.xlabel("Value")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("/mnt/data/fig_A_normal_hist.png")
plt.close(fig)

# ----------
# B. Binomial data (accuracy)
# ----------

# B1 — Bernoulli accuracy: n=200, p=0.92
acc_df = pd.DataFrame({"acc": rng.binomial(n=1, p=0.92, size=200)})
acc_df_summary = pd.DataFrame({"prop_correct":[acc_df["acc"].mean()], "n":[acc_df["acc"].size]})
print("\nB1. Overall accuracy summary:\n", acc_df_summary, "\n")

# Plot overall proportion with a point + 95% CI (Wilson)
p_hat = acc_df["acc"].mean()
n_obs = acc_df["acc"].size
ci_low, ci_high = stats.binomtest(acc_df["acc"].sum(), n=n_obs).proportion_ci(method="wilson")
fig = plt.figure()
plt.scatter([0], [p_hat])
plt.vlines(0, ci_low, ci_high)
plt.ylim(0, 1)
plt.xticks([0], ["Overall"])
plt.ylabel("Proportion correct")
plt.title("Bernoulli accuracy with 95% CI (Wilson)")
plt.tight_layout()
plt.savefig("/mnt/data/fig_B1_accuracy_ci.png")
plt.close(fig)

# B2 — Two conditions (Easy vs Hard) with different ps
# Example: Easy p=0.95, Hard p=0.75, with equal trials (n=200 each)
cond = np.repeat(["Easy", "Hard"], repeats=200)
p_map = {"Easy": 0.95, "Hard": 0.75}
acc = np.array([rng.binomial(n=1, p=p_map[c]) for c in cond])
acc_by_cb = pd.DataFrame({"cond": cond, "acc": acc})

# Summaries by condition
acc_by_cb_summary = (
    acc_by_cb.groupby("cond", as_index=False)
    .agg(prop_correct=("acc", "mean"), n=("acc", "size"))
)
# Wide
acc_wide = acc_by_cb_summary.pivot(index=None, columns="cond", values="prop_correct")

print("B2. Accuracy by condition:\n", acc_by_cb_summary, "\n")
overall_prop = acc_df["acc"].mean()
easy_prop = acc_by_cb_summary.loc[acc_by_cb_summary["cond"]=="Easy", "prop_correct"].item()
hard_prop = acc_by_cb_summary.loc[acc_by_cb_summary["cond"]=="Hard", "prop_correct"].item()
print(f'Inline prompt: "Overall accuracy = {overall_prop:.3f}. Easy = {easy_prop:.3f}, Hard = {hard_prop:.3f}."')

# ----------
# C. Reaction times (RT): shifted lognormal
# ----------

def r_shifted_lognorm(n, t0, meanlog, sdlog, rng):
    """Return t0 + LogNormal(meanlog, sdlog). meanlog/sdlog are on log scale."""
    return t0 + rng.lognormal(mean=meanlog, sigma=sdlog, size=n)

# C1 — Single distribution
rt = r_shifted_lognorm(500, t0=300, meanlog=log(250), sdlog=log(20), rng=rng)
rt_df = pd.DataFrame({"rt": rt})
rt_df["log_rt"] = np.log(rt_df["rt"])

# Summaries
summ = rt_df["rt"].agg(["mean", "median", "std", "min", "max"]).to_frame().T
print("\nC1. RT summary (ms):\n", summ.round(2), "\n")

# Histograms: rt and log_rt
fig = plt.figure()
plt.hist(rt_df["rt"], bins=30, alpha=0.85)
plt.title("Shifted lognormal RTs")
plt.xlabel("RT (ms)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("/mnt/data/fig_C1_rt_hist.png")
plt.close(fig)

fig = plt.figure()
plt.hist(rt_df["log_rt"], bins=30, alpha=0.85)
plt.title("Logged RTs")
plt.xlabel("log(RT)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("/mnt/data/fig_C1_logrt_hist.png")
plt.close(fig)

# C2 — Multi-participant, two-condition experiment (Valid vs Invalid)
# Let's mimic a cueing experiment with a participant baseline variation.
n_participants = 40
trials_per_cond = 150  # per condition per participant
conditions = ["valid", "invalid"]

rows = []
for pid in range(1, n_participants + 1):
    # participant baseline shift
    t0_base = 300 + rng.normal(0, 30)  # vary baseline a bit
    for cond in conditions:
        # allow invalid to be slightly slower
        if cond == "valid":
            meanlog, sdlog, t0 = log(250), log(20), t0_base
        else:
            meanlog, sdlog, t0 = log(260), log(20), t0_base + 20
        rts = r_shifted_lognorm(trials_per_cond, t0=t0, meanlog=meanlog, sdlog=sdlog, rng=rng)
        rows.append(pd.DataFrame({
            "participant": pid,
            "condition": cond,
            "rt": rts
        }))

df_experiment = pd.concat(rows, ignore_index=True)

# Summarize by participant and condition
df_experiment_summary = (
    df_experiment.groupby(["participant", "condition"], as_index=False)
    .agg(mean_rt=("rt", "mean"))
)

# CI over participants for each condition (t-based CI for the mean of participant means)
def mean_ci_95(x):
    x = np.asarray(x)
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(len(x))
    ci = stats.t.interval(0.95, df=len(x)-1, loc=m, scale=se)
    return m, ci

means_valid = df_experiment_summary.query("condition=='valid'")["mean_rt"]
means_invalid = df_experiment_summary.query("condition=='invalid'")["mean_rt"]
m_v, ci_v = mean_ci_95(means_valid)
m_i, ci_i = mean_ci_95(means_invalid)
print("C2. Participant-mean RTs (ms):")
print(f"  valid:   mean={m_v:.1f}, 95% CI=({ci_v[0]:.1f}, {ci_v[1]:.1f})")
print(f"  invalid: mean={m_i:.1f}, 95% CI=({ci_i[0]:.1f}, {ci_i[1]:.1f})\n")

# Plot participant means and overall mean with 95% CI
fig = plt.figure()
# jitter x for participants
x_map = {"valid": 0, "invalid": 1}
x_vals = df_experiment_summary["condition"].map(x_map).values + (rng.random(len(df_experiment_summary)) - 0.5) * 0.04
plt.scatter(x_vals, df_experiment_summary["mean_rt"], alpha=0.6)
# connect each participant's two points
for pid, sub in df_experiment_summary.groupby("participant"):
    xs = sub["condition"].map(x_map).values
    ys = sub["mean_rt"].values
    plt.plot(xs, ys, color="grey", alpha=0.1)

# overall means and CIs
plt.scatter([0,1], [m_v, m_i], s=50)
plt.vlines([0,1], [ci_v[0], ci_i[0]], [ci_v[1], ci_i[1]])
plt.xticks([0,1], ["valid", "invalid"])
plt.xlabel("Condition")
plt.ylabel("Average RT (ms)")
plt.title("RT by Simulated Cueing Condition")
plt.tight_layout()
plt.savefig("/mnt/data/fig_C2_rt_condition.png")
plt.close(fig)

# Save some convenient CSVs for inspection if needed
norm_df.to_csv("/mnt/data/A_normal_df.csv", index=False)
acc_df.to_csv("/mnt/data/B1_acc_df.csv", index=False)
acc_by_cb.to_csv("/mnt/data/B2_acc_by_cb.csv", index=False)
df_experiment_summary.to_csv("/mnt/data/C2_rt_summary_by_participant.csv", index=False)

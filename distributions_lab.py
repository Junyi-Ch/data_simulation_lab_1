"""
Simulations & Python/pandas lab
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

# TODO: Calculate some basic summaries of this dataframe and print them out
# Hint: Use norm_df["sim_values"].agg() with functions like "mean", "std", "count"
# What happens if you increase the "n"? How do these summaries change?

# Exercise: change mu and sd_norm to two other combos (e.g., 10 & 2; 10 & 5).
# Write one sentence with an inline mean (e.g., f"Mean = {norm_df['sim_values'].mean():.2f}").

# Bonus: Compute another kind of summary statistic on the dataset
# Bonus: Simulate another distribution and also plot it on the same histogram (you can make it a different color)

# ----------
# B. Binomial data (accuracy)
# ----------

# B1 — Bernoulli accuracy: n=200, p=0.92
# TODO: create a simulated dataframe using rng.binomial
# Hint: Use pd.DataFrame() and rng.binomial(n=1, p=0.92, size=200)
# Expected: acc_df should have one column called 'acc' with 200 values of 0 or 1

# TODO: summarise and count
# Hint: Use acc_df["acc"].agg() to calculate proportion correct and n
# Expected: Create acc_df_summary with columns prop_correct and n

print("\nB1. Overall accuracy summary:\n", acc_df_summary, "\n")

# TODO: Plot overall proportion with a point + 95% CI (Wilson)
# Hint: Use stats.binomtest() for confidence intervals
# Use plt.scatter() for the point and plt.vlines() for error bars

# B2 — Two conditions (Easy vs Hard) with different ps
# TODO: Simulate two conditions with different probabilities
# Hint: Use np.repeat() to create condition labels
# Use different probabilities for Easy vs Hard conditions (e.g., Easy p=0.95, Hard p=0.75)

# TODO: Summaries by condition
# Hint: Use groupby() and agg() to calculate prop_correct and n by condition

# TODO: Create wide format
# Hint: Use pivot() to make conditions into separate columns

print("B2. Accuracy by condition:\n", acc_by_cb_summary, "\n")

# TODO: Calculate inline statistics
# Hint: Extract overall_prop, easy_prop, hard_prop from your summaries
# Print: f'Inline prompt: "Overall accuracy = {overall_prop:.3f}. Easy = {easy_prop:.3f}, Hard = {hard_prop:.3f}."'

# ----------
# C. Reaction times (RT): shifted lognormal
# ----------

def r_shifted_lognorm(n, t0, meanlog, sdlog, rng):
    """Return t0 + LogNormal(meanlog, sdlog). meanlog/sdlog are on log scale."""
    return t0 + rng.lognormal(mean=meanlog, sigma=sdlog, size=n)

# C1 — Single distribution
# TODO: Simulate RTs and their logged RTs
# Hint: Use the r_shifted_lognorm() function with the specified parameters
# Create a DataFrame with rt and log_rt columns
# Expected: rt_df should have columns 'rt' (reaction times) and 'log_rt' (log of reaction times)

# TODO: Calculate summaries
# Hint: Use rt_df["rt"].agg() with functions like "mean", "median", "std", "min", "max"

print("\nC1. RT summary (ms):\n", summ.round(2), "\n")

# TODO: Create histograms for rt and log_rt
# Hint: Use plt.hist() for both distributions
# Use different bins and titles for each plot

# C2 — Multi-participant, two-condition experiment (Valid vs Invalid)
# TODO: Simulate multiple participants with different conditions
# Hint: Use a nested loop over participants and conditions
# Each participant should have different baseline shifts
# Use pd.concat() to combine all participant data

# TODO: Summarize by participant and condition
# Hint: Use groupby(["participant", "condition"]) and agg()

# TODO: Calculate confidence intervals over participants
# Hint: Use stats.t.interval() for 95% CIs
# Calculate means and CIs for each condition separately

print("C2. Participant-mean RTs (ms):")
print(f"  valid:   mean={m_v:.1f}, 95% CI=({ci_v[0]:.1f}, {ci_v[1]:.1f})")
print(f"  invalid: mean={m_i:.1f}, 95% CI=({ci_i[0]:.1f}, {ci_i[1]:.1f})\n")

# TODO: Plot participant means and overall mean with 95% CI
# Hint: Use plt.scatter() for individual points
# Use plt.plot() to connect each participant's two points
# Use plt.vlines() for confidence intervals
# Add jitter to x-coordinates to avoid overlapping points

# Save some convenient CSVs for inspection if needed
norm_df.to_csv("/mnt/data/A_normal_df.csv", index=False)
acc_df.to_csv("/mnt/data/B1_acc_df.csv", index=False)
acc_by_cb.to_csv("/mnt/data/B2_acc_by_cb.csv", index=False)
df_experiment_summary.to_csv("/mnt/data/C2_rt_summary_by_participant.csv", index=False)
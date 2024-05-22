#%%
import wandb
import pandas as pd
from matplotlib import pyplot as plt
api = wandb.Api()


# %% Markov LLM final accuracy (6k iterations)
res = []
for run in api.runs("markov-PQ", {"config.memory": 1}):
    try:
        res.append((run.id, run.config.get("p", None), run.config.get("q", None), run.summary["val/acc"]))
    except:
        pass

df = pd.DataFrame(res, columns=["id", "p", "q", "val/acc"])
piv = df.pivot_table(index="p", columns="q", values="val/acc")
fig, ax = plt.subplots(figsize=(10, 10))
v = ax.matshow(piv, vmin=0, vmax=1)
ax.set_xticks(range(len(piv.columns)), piv.columns)
ax.set_yticks(range(len(piv.index)), piv.index)
ax.xaxis.set_ticks_position("bottom")
ax.set(xlabel="Q", ylabel="P")
ax.set_title("Markov LLM final accuracy (6k iterations, masked memory)")
fig.colorbar(v, ax=ax, label="Final accuracy")
for i in range(len(piv.index)):
    for j in range(len(piv.columns)):
        ax.text(j, i, f"{piv.iloc[i, j]:.3f}", ha="center", va="center", color="w")
fig.savefig("markov-pq-memory.png", dpi=300)

'''# %% PowerSGD varying rank (very high power)
res = []
for run in api.runs("federated-codes", {"group": "psgdstudy"}):
    try:
        res.append((run.id, run.config.get("powersgd_rank", None), run.config["learning_rate"], run.summary["best_accuracy"], run.summary["_step"]))
    except:
        pass

df = pd.DataFrame(res, columns=["id", "powersgd_rank", "learning_rate", "best_accuracy", "step"])
piv = df.pivot_table(index="powersgd_rank", columns="learning_rate", values="best_accuracy")
fig, ax = plt.subplots(figsize=(8, 6))
v = ax.matshow(piv, vmin=0.6, vmax=0.85)
ax.set_xticks(range(len(piv.columns)), piv.columns)
ax.set_yticks(range(len(piv.index)), piv.index.astype(int))
ax.xaxis.set_ticks_position("bottom")
ax.set(xlabel="Learning rate", ylabel="PowerSGD Rank")
ax.set_title("Effect of PowerSGD rank (100 epochs, Cifar-10, ResNet-18)")
fig.colorbar(v, ax=ax, label="Final accuracy (exponential moving average)")
for i in range(len(piv.index)):
    for j in range(len(piv.columns)):
        ax.text(j, i, f"{100*piv.iloc[i, j]:.0f}%", ha="center", va="center", color="w")
fig.savefig("powersgd_rankstudy.png", dpi=300)
# %%'''

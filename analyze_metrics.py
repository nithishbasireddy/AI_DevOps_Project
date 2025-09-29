import pandas as pd
import os
if not os.path.exists("metrics.csv"):
    print("No metrics.csv found. Run pytest first.")
    exit(1)
df = pd.read_csv("metrics.csv")
agg = df.groupby('run_id', sort=False).agg({'TP':'sum','FP':'sum','FN':'sum'}).reset_index()
def compute(row):
    tp, fp, fn = row['TP'], row['FP'], row['FN']
    prec = tp/(tp+fp) if (tp+fp)>0 else 0.0
    rec = tp/(tp+fn) if (tp+fn)>0 else 0.0
    f1 = (2*prec*rec/(prec+rec)) if (prec+rec)>0 else 0.0
    return pd.Series({"precision":prec,"recall":rec,"f1":f1})
metrics = agg.join(agg.apply(compute, axis=1))
metrics.to_csv("metrics_aggregated.csv", index=False)
print(metrics)

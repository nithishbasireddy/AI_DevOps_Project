import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid", rc={"figure.figsize":(10,6)})

df = pd.read_csv("metrics_aggregated.csv")
x = df['run_id'].astype(str)
plt.plot(x, df['precision'], marker='o', label='Precision')
plt.plot(x, df['recall'], marker='o', label='Recall')
plt.plot(x, df['f1'], marker='o', label='F1')
plt.title("Model performance across runs/epochs")
plt.xlabel("run_id")
plt.ylabel("score")
plt.ylim(0,1.05)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("performance_over_time.png")
print("Saved performance_over_time.png")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
data={"hour":[8,9,10,11,12,13,14,15,16,17,18,19],
	"vehicles":[90,120,70,50,60,65,75,85,110,140,160,100],
	"speed":[25,15,35,45,40,38,32,28,18,12,8,22]}
df=pd.DataFrame(data)
def classify_traffic(speed):
	if speed<15:
		return "HIGH"
	elif speed <30:
		return "MODERATE"
	else:
		return "LOW"
df["Congestion"]=df["speed"].apply(classify_traffic)
print("\nSMARTTRAFFIC-SAMPLE ANALYSIS")
print(df.to_string(index=False))
print("\nAverage speed:",df["speed"].mean(),"km/h")
print("Highest vehicle count:",df["vehicles"].max())
plt.figure(figsize=(9,5))
plt.plot(df["hour"],df["vehicles"],marker="o",label="Vehicles")
plt.xlabel("Hour of day")
plt.ylabel("Vehicle count")
plt.title("Sample Traffic Pattern by Hour")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("traffic_pattern.png")
plt.show()

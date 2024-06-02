using isolation forest

iso_forest = IsolationForest(contamination=0.02, random_state=42)
iso_forest.fit(df[['cost']])
df['Anomaly'] = iso_forest.predict(df[['cost']])
df['Anomaly'] = df['Anomaly'].map({1: 0, -1: 1})

make nodes in rectangle, and allow a red dot to travel one node to another taking small steps on the path using arrow keys, keep a counter of current cost, and chcekc with isolation forest if current position shows anomaly, if anomaly, pop up a message

from,to,cost
721,445,0.79
542,480,2.575
770,702,0.9259999999999999
32,266,0.596
34,56,0.628

this is how data looks like

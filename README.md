# anomaly

anomaly detection on pems dataset which contains three columns "to, from and cost"

to and from contain node ID, nodes closer in number are closer in distance, ex: 252 is close to 251

classify anomaly on basis:

1. if a pair of to and from node are close, thier cost should be low, if its too high as compared to other nodes in data with close distance then it is anomaly

2. if the distance between to and from is too high, then high cost is okay, and no anomaly here

if a pair of "to" "from" and "cost" are anomaly or not
from,to,cost
721,445,0.79
542,480,2.575
770,702,0.9259999999999999 3
2,266,0.596
34,56,0.628
251,297,0.725
this is a subset of dataset

721,445,0.79 this is little far away from each other yet cost is low, so its not anomaly 542,480,2.575 this is comparatively closer to each other yet cost too high

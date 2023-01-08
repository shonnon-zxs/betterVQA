import torch
import torch.nn as nn
"""
targets=torch.zeros(3,5)
index = torch.LongTensor([[3],[2],[5]])
targets.scatter_(1,index-1,0.5)
print(targets.size(),index.size())
print(targets)
"""


label = torch.Tensor([1, 0.6, 0])
pred = torch.Tensor([3, 2, 1])
pred_sig = torch.sigmoid(pred)
# BCELoss must be used together with sigmoid
loss = nn.BCELoss()
print(loss(pred_sig, label))
# BCEWithLogitsLoss
loss = nn.BCEWithLogitsLoss()
print(loss(pred, label))
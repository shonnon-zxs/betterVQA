# CVPR2020 Counterfactual Samples Synthesizing for Robust VQA
This repo contains code for our paper ["Counterfactual Samples Synthesizing for Robust Visual Question Answering"](https://arxiv.org/pdf/2003.06576.pdf)
This repo contains code modified from [here](https://github.com/chrisc36/bottom-up-attention-vqa),many thanks!

### Prerequisites

Make sure you are on a machine with a NVIDIA GPU and Python 2.7 with about 100 GB disk space. <br>
h5py==2.10.0 <br>
pytorch==1.1.0 <br>
Click==7.0 <br>
numpy==1.16.5 <br>
tqdm==4.35.0 <br>

### Data Setup
You can use
```
nohup bash tools/download.sh > myout.file 2>&1 &
bash tools/download.sh
```
to download the data <br>
and the rest of the data and trained model can be obtained from [BaiduYun](https://pan.baidu.com/s/1oHdwYDSJXC1mlmvu8cQhKw)(passwd:3jot) or [MEGADrive](https://mega.nz/folder/0JBzGBZD#YGgonKMnwqmeSZmoV7hjMg)
unzip feature1.zip and feature2.zip and merge them into data/rcnn_feature/ <br>
use
```
bash tools/process.sh 
```
to process the data <br>

### Training
Run
```
CUDA_VISIBLE_DEVICES=0 nohup python main.py --dataset cpv2 --mode q_v_debias --debias learned_mixin --topq 1 --topv -1 --qvp 5 --output [mutan-css-vq-lmh-cpv2-] --seed 0 > myout.file 2>&1 &
CUDA_VISIBLE_DEVICES=0 nohup python main.py --dataset cpv2 --mode updn --debias none --output [t] --seed 0 > myout.file 2>&1 &

find /home/xuesongzhang/CSS-VQA-master/feature1/ -name "*.jpg" -exec cp {} /home/xuesongzhang/CSS-VQA-master/data/rcnn_feature/ \; 
```
to train a model

### Testing
Run
```
CUDA_VISIBLE_DEVICES=0 python eval.py --dataset cpv2 --debias none --model_state /home/xuesongzhang/CSS-VQA-master/logs/[argmax]/model.pth
```
to eval a model



## Citation

If you find this code useful, please cite the following paper:

  ```
@inproceedings{chen2020counterfactual,
  title={Counterfactual Samples Synthesizing for Robust Visual Question Answering},
  author={Chen, Long and Yan, Xin and Xiao, Jun and Zhang, Hanwang and Pu, Shiliang and Zhuang, Yueting},
  booktitle={CVPR},
  year={2020}
}
  ```
"""
总体来说包括以下几部分
1，抑制自信度的代码，
2，保存输出预测的自信度
3，计算每个bin的自信度，精确率等，然后数据保存在excel表格中进行画图并计算eof和ece

（eof和ece的计算可通过excel表格计算，后面也有写）
例如在表格的sheet2中， EOF = [（conf0-acc0）* conf0 * weight0 + …… + （conf9-acc9）* conf9 * weight9 ] / 219928(总样本数)
ECE = [|conf0-acc0| * weight0 + …… + |conf9-acc9| * weight9 ] / 219928(总样本数) 注意是绝对值

"""



#############################################训练过自信代码#####################################################

# 只需要加上这一个损失函数，但是需要调整权重（0.1到 4之间），其他基于CSS和SSL实现

# L_tacs 用的这个，抑制gt的自信度
def compute_self_loss(logits_neg, labels):
    prediction_ans_k, top_ans_ind = torch.topk(F.softmax(a, dim=-1), k=1, dim=-1, sorted=False)
    neg_top_k = torch.gather(F.softmax(logits_neg, dim=-1), 1, top_ans_ind).sum(1)

    qice_loss = neg_top_k.mean()
    return qice_loss

# L_conf 抑制最大值
def compute_loss(logits_neg, labels):
    prediction_ans_k, top_ans_ind = torch.topk(F.softmax(a, dim=-1), k=1, dim=-1, sorted=False)
    prediction_max, pred_ans_ind = torch.topk(F.softmax(logits_neg, dim=-1), k=1, dim=-1, sorted=False)
    neg_top_k = torch.gather(F.softmax(logits_neg, dim=-1), 1, top_ans_ind).sum(1)
    pre_ans_k = prediction_max.squeeze(1)
    # neg_top_k = neg_top_k.squeeze(1)
    qice_loss = neg_top_k.mean()
    pre_ans_k = pre_ans_k.tolist()
    neg_top_k = neg_top_k.tolist()
    return qice_loss ,pre_ans_k ,neg_top_k

loss = loss + compute_self_loss(logits, labels)











########################################## 输出保存预测结结果 ########################################################

""" 
首先分别输出模型的最大预测值（pred_max）和ground truth上的预测值（pred_right）保存为json格式，如下
{
    "pred_max": [
        0.16141875088214874, 
        0.9999594688415527, 
        0.5323234796524048, 
        1.0, 
        0.3643921911716461, 
        0.6707115769386292, 
        0.23669420182704926, 
        0.18947939574718475, 
        ……
        0.5415464639663696, 
        0.9999452829360962, 
        0.9999783039093018, 
        0.9988911747932434
    ], 
    "pred_right": [
        0.05331508070230484, 
        0.9999594688415527, 
        0.024799373000860214, 
        1.0, 
        ……
        0.8805205225944519, 
        0.25417470932006836, 
        0.13009017705917358, 
        0.9999783039093018, 
        0.9988911747932434
    ]
}
"""
# 输出最大预测值和gt位置的自信度，输出结果保存的是验证的时候的，输出保存为json格式下面注释掉了
def evaluate(model, dataloader, qid2type,epoch):
    score = 0
    upper_bound = 0
    score_yesno = 0
    score_number = 0
    score_other = 0
    total_yesno = 0
    total_number = 0
    total_other = 0
    total_loss_rubi = 0
    total_loss_bce = 0
    pred_right_list = []
    pred_max_list = []
    ans = {}

    for v, q, a, b, _,_,qids in tqdm(dataloader, ncols=100, total=len(dataloader), desc="eval"):
        v = Variable(v, requires_grad=False).cuda()
        q = Variable(q, requires_grad=False).cuda()
        a = Variable(a, requires_grad=False).cuda()
        # pred,loss_rubi,_ = model(v, q, a, None,None)
        pred, loss_rubi, _ = model(v, q, a, None, None)
        loss_bce = instance_bce_with_logits(pred.cpu(), a.cpu())
        total_loss_bce += loss_bce.item() * q.size(0)
        total_loss_rubi += loss_rubi.item() * q.size(0)
        # batch_score = compute_score_with_logits(pred, a.cuda()).cpu().numpy().sum(1)
        # batch_score = compute_score_with_logits(pred, a.cuda())
        # batch_score = batch_score.cpu().numpy().sum(1)
        batch_score = compute_score_with_logits(pred, a.cuda()).cpu().numpy().sum(1)
        # pred_right_list = pred_right_list + pred_right
        # pred_max_list = pred_max_list + pre_max
        score += batch_score.sum()
        upper_bound += (a.max(1)[0]).sum()
        qids = qids.detach().cpu().int().numpy()
        for j in range(len(qids)):
            qid = qids[j]
            typ = qid2type[str(qid)]
            if typ == 'yes/no':
                score_yesno += batch_score[j]
                total_yesno += 1
            elif typ == 'other':
                score_other += batch_score[j]
                total_other += 1
            elif typ == 'number':
                score_number += batch_score[j]
                total_number += 1
            else:
                print('Hahahahahahahahahahaha')

    # ans['pred_max'] = pred_max_list
    # ans['pred_right'] = pred_right_list
    # json_str = json.dumps(ans, indent=4)  # import torch
    # with open('rubi_test_yuanshi_answer-{}.json'.format(epoch), 'w') as json_file:  # import numpy
    #     json_file.write(json_str)
    score = score / len(dataloader.dataset)
    upper_bound = upper_bound / len(dataloader.dataset)
    total_loss_rubi = total_loss_rubi / len(dataloader.dataset)
    total_loss_bce = total_loss_bce / len(dataloader.dataset)
    score_yesno /= total_yesno
    score_other /= total_other
    score_number /= total_number

    results = dict(
        score=score,
        upper_bound=upper_bound,
        score_yesno=score_yesno,
        score_other=score_other,
        score_number=score_number,
        total_loss_rubi=total_loss_rubi,
        total_loss_bce=total_loss_bce
    )
    return results








#############################################画图计数相关代码#####################################################
import math
import numpy as np
import json

# "H:\Desktop\wang\ObjectCount\pi\\updn\\answer_test.json"
# "H:\Desktop\wang\ObjectCount\Count_howmany\\updn_test_conf314_answer.json"
# H:\Desktop\wang\ObjectCount\Count_howmany\\rubi_test_yuanshi_answer-49.json
# H:\Desktop\wang\ObjectCount\Count_howmany\\rubi_test_conf314_answer.json

# "H:\Desktop\wang\ObjectCount\pi\\updn\SLL_test_yuanshi_answer-20.json"
# "H:\Desktop\wang\ObjectCount\pi\\updn\answer-test-regat_yuanshi.json"



"""
只需要获得每个bin的acc和权重（即每个bin的样本数/总数），
然后conf其实不需要计算，即使计算其大小也可以四舍五入为 0.05，0.15，，，0.95
输出结果放入excel表格中进行画图，计算eof
例如在表格的sheet2中， EOF = [（conf0-acc0）* conf0 * weight0 + …… + （conf9-acc9）* conf9 * weight9 ] / 219928(总样本数)
ECE = [|conf0-acc0| * weight0 + …… + |conf9-acc9| * weight9 ] / 219928(总样本数) 注意是绝对值
"""

"""
读取文件获得pred_max和pred_right
"""
with open('/home/xuesongzhang/CSS-VQA-master/logs/[argmax]/max_gt.json', 'r') as f:
    same_sample = json.load(f)
# print(len(same_sample))
pred = same_sample['pred_max']
print(len(pred))
# pred_ans_ind = same_sample['pred_ansindex']
pred_ans_ind = same_sample['pred_right']
# pred_ans_ind = same_sample['ans_indx_pred']

"""
初始化
"""
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0

conf0 = 0
conf1 = 0
conf2 = 0
conf3 = 0
conf4 = 0
conf5 = 0
conf6 = 0
conf7 = 0
conf8 = 0
conf9 = 0

len0 = 0
len1 = 0
len2 = 0
len3 = 0
len4 = 0
len5 = 0
len6 = 0
len7 = 0
len8 = 0
len9 = 0

a0 = 0
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a55 = 0
a6 = 0

for i in range(len(pred)):
    # 计算精确率，注意这个精确率和VQA中的精确率有区别
    # 计算每个bin预测正确的个数
    if pred[i] < 0.1 and pred[i] == pred_ans_ind[i]:
        count0 += 1
    elif 0.1 <= pred[i] < 0.2 and pred[i] == pred_ans_ind[i]:
        count1 += 1
    elif 0.2 <= pred[i] < 0.3 and pred[i] == pred_ans_ind[i]:
        count2 += 1
    elif 0.3 <= pred[i] < 0.4 and pred[i] == pred_ans_ind[i]:
        count3 += 1
    elif 0.4 <= pred[i] < 0.5 and pred[i] == pred_ans_ind[i]:
        count4 += 1
    elif 0.5 <= pred[i] < 0.6 and pred[i] == pred_ans_ind[i]:
        count5 += 1
    elif 0.6 <= pred[i] < 0.7 and pred[i] == pred_ans_ind[i]:
        count6 += 1
    elif 0.7 <= pred[i] < 0.8 and pred[i] == pred_ans_ind[i]:
        count7 += 1
    elif 0.8 <= pred[i] < 0.9 and pred[i] == pred_ans_ind[i]:
        count8 += 1
    elif 0.9 <= pred[i] < 1.0 and pred[i] == pred_ans_ind[i]:
        count9 += 1

    # 计算每个bin的自信度conf及样本个数len
    if pred[i] < 0.1:
        conf0 = conf0 + pred[i]
        len0 += 1
    elif 0.1 <= pred[i] < 0.2:
        conf1 = conf1 + pred[i]
        len1 += 1
    elif 0.2 <= pred[i] < 0.3:
        conf2 = conf2 + pred[i]
        len2 += 1
    elif 0.3 <= pred[i] < 0.4:
        conf3 = conf3 + pred[i]
        len3 += 1
    elif 0.4 <= pred[i] < 0.5:
        conf4 = conf4 + pred[i]
        len4 += 1
    elif 0.5 <= pred[i] < 0.6:
        conf5 = conf5 + pred[i]
        len5 += 1
    elif 0.6 <= pred[i] < 0.7:
        conf6 = conf6 + pred[i]
        len6 += 1
    elif 0.7 <= pred[i] < 0.8:
        conf7 = conf7 + pred[i]
        len7 += 1
    elif 0.8 <= pred[i] < 0.9:
        conf8 = conf8 + pred[i]
        len8 += 1
    elif pred[i] >= 0.9:
        conf9 = conf9 + pred[i]
        len9 += 1

# 打印每个自信度bin的个数
all_len = len0 + len1 + len2 + len3 + len4 + len5 + len6 + len7 + len8 + len9
print('len:')
print(all_len)
print(len0)
print(len1)
print(len2)
print(len3)
print(len4)
print(len5)
print(len6)
print(len7)
print(len8)
print(len9)

# 打印每个区间的自信度
print('conf')
print(conf0 / len0)
print(conf1 / len1)
print(conf2 / len2)
print(conf3 / len3)
print(conf4 / len4)
print(conf5 / len5)
print(conf6 / len6)
print(conf7 / len7)
print(conf8 / len8)
print(conf9 / len9)

# 打印预测正确的样本的个数
print('acc:')
all_count = count0 + count1 + count2 + count3 + count4 + count5 + count6 + count7 + count8 + count9
# 打印每个bin的精确率
print(float(count0) / float(len0))
print(float(count1) / float(len1))
print(float(count2) / float(len2))
print(float(count3) / float(len3))
print(float(count4) / float(len4))
print(float(count5) / float(len5))
print(float(count6) / float(len6))
print(float(count7) / float(len7))
print(float(count8) / float(len8))
print(float(count9) / float(len9))

# 打印总体精确率，即acc_all
print('acc_all:')
print(float(all_count) / all_len)

############################################################输出结果记录################################################
"""
219928
219928
7498
20276
18739
16894
14843
15465
13559
13523
15118
84013
0.04961323019471859
0.0980469520615506
0.17343508191472332
0.22617497336332426
0.2955601967257293
0.3710313611380537
0.4139685817538167
0.44945648154995194
0.47274771795211007
0.27444562151095664

conf

219928
219928
7967
25208
27503
29965
24111
30865
40457
21081
8307
4464
0.04844985565457512
0.11464614408124404
0.2028505981165691
0.27618888703487404
0.4329973870847331
0.6256277336789243
0.825543169290852
0.8352070584886865
0.8146141808113639
0.8866487455197133


"""

"""
rubi
219928
219928
741
6512
11877
13756
14513
15301
13930
13607
15967
113724
0.043184885290148446
0.0753992628992629
0.11417024501136651
0.16349229427159057
0.21546199958657755
0.2769100058819685
0.30488155061019384
0.33886969941941647
0.36769587273752113
0.2847156273082199

rubi_after
219928
219928
7150
24180
27260
24673
20073
24716
40818
27375
10465
13218
0.05608391608391609
0.12018196856906534
0.20220102714600147
0.2985449681838447
0.4311762068450157
0.6043858229486972
0.7994512224998775
0.8195068493150685
0.7908265647396082
0.915796640944167

regat
2907
14159
17153
17198
16643
16223
13978
13403
14987
93277
0.03543171654626763
0.07429903241754361
0.13338774558386288
0.17205489010350042
0.21186084239620262
0.2786167786475991
0.30440692516812135
0.335745728568231
0.38079669046506975
0.24467982460842436
0.23522698337637774

lmh
20465
39269
31212
24946
21713
19331
17978
17696
16329
10989
0.10730515514292695
0.209605541266648
0.3349032423426887
0.4748657099334563
0.6032791415281168
0.7052402876209197
0.793469796417844
0.8580470162748643
0.9051380978626983
0.9458549458549459
0.5187197628314721


ssl
7132
19228
18417
17807
16391
19035
17245
18941
25212
60520
0.051598429613011774
0.09423757021011026
0.16517348102296792
0.232155893749649
0.30004270636324815
0.4075124770160231
0.4854740504494056
0.5811731165197191
0.6884816753926701
0.8124421678783873
0.4907878942199265

"""
""" # 计算ece这块不要看
for i in range(len(pred)):
    math.fabs(pred[i] - pred_ans_ind[i]) # 浮点绝对值

    if pred[i] < 0.2:
        a0 = a0 + math.fabs(pred[i] - pred_ans_ind[i])
        len0 += 1
    elif 0.2 <= pred[i] < 0.4:
        a1 = a1 + math.fabs(pred[i] - pred_ans_ind[i])
        len1 += 1
    elif 0.4 <= pred[i] < 0.6:
        a2 = a2 + math.fabs(pred[i] - pred_ans_ind[i])
        len2 += 1
    elif 0.6 <= pred[i] < 0.8:
        a3 = a3 + math.fabs(pred[i] - pred_ans_ind[i])
        len3 += 1
    elif 0.8 <= pred[i] < 0.9:
        a4 = a4 + math.fabs(pred[i] - pred_ans_ind[i])
        len4 += 1
    elif 0.9 <= pred[i] < 0.95:
        a5 = a5 + math.fabs(pred[i] - pred_ans_ind[i])
        len5 += 1
    elif 0.95 <= pred[i] < 0.98:
        a55 = a55 + math.fabs(pred[i] - pred_ans_ind[i])
        len6 += 1
    elif pred[i] >= 0.98:
        a6 = a6 + math.fabs(pred[i] - pred_ans_ind[i])
        len7 += 1

ece = (a1 / len1 + a2 / len2 + a3 / len3 + a4 / len4 + a5 / len5 + a55 / len6 + a6 / len7) / 7
print(ece)
"""
![image](https://user-images.githubusercontent.com/68311986/236407426-0b836874-9bad-4a06-89e7-2767bebe2d24.png)


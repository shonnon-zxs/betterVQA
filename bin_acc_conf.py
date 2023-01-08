# import matplotlib.pyplot as plt

import math
import numpy as np
import json


# "H:\Desktop\wang\ObjectCount\pi\\updn\\answer_test.json"
# "H:\Desktop\wang\ObjectCount\Count_howmany\\updn_test_conf314_answer.json"
# H:\Desktop\wang\ObjectCount\Count_howmany\\rubi_test_yuanshi_answer-49.json
# H:\Desktop\wang\ObjectCount\Count_howmany\\rubi_test_conf314_answer.json

# "H:\Desktop\wang\ObjectCount\pi\\updn\SLL_test_yuanshi_answer-20.json"
# "H:\Desktop\wang\ObjectCount\pi\\updn\answer-test-regat_yuanshi.json"

with open('/home/xuesongzhang/CSS-VQA-master/logs/[argmax]/max_gt.json', 'r') as f:
    same_sample = json.load(f)
# print(len(same_sample))
pred = same_sample['pred_max']
print(len(pred))
# pred_ans_ind = same_sample['pred_ansindex']
pred_ans_ind = same_sample['pred_right']
# pred_ans_ind = same_sample['ans_indx_pred']
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
"""
for i in range(len(pred)):
    math.fabs(pred[i] - pred_ans_ind[i])

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


for i in range(len(pred)):
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

"""

"""


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

print('acc:')

all_count = count0 + count1 + count2 + count3 + count4 + count5 + count6 + count7 + count8 + count9

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


print('acc_all:')
print(float(all_count) / all_len)

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

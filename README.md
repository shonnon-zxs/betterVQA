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


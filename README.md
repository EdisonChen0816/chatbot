# 手把手教您搭建对话系统

## 1，git clone

## 2，下载w2v.model.vectors.npy,放在 /model/w2v 目录下
####链接：https://pan.baidu.com/s/1C1qB2b6HyzOpj3eqDehhEQ  提取码：5b6y 

## 3，配置语料，本demo项目中，有三种语料，
###意图语料 /data/intent
### faq标准问语料 /data/faq
### 闲聊语料 /data/chat

## 4，pip3 install requirements.txt -r

## 5，启动服务
#### python server.py

## 6，接口说明：
### 先识别意图，如果未识别到意图，再识别faq，如果未识别到faq，最后识别闲聊
### 请求方式，http+post 
### http://127.0.0.1:51666/chatbot
### 输入： 
{
    "text": "上海天气怎么样"
}
### 返回意图：
{
  "err_no": 0,
  "intent": "Weather",
  "slot": {
    "City": "上海"
  },
  "status": 200
}

### 输入：
{
    "text": "五险一金怎么缴"
}
### 返回faq：
{
  "err_no": 0,
  "faq": "按照最低标准缴",
  "status": 200
}

### 输入：
{
    "text": "留个电话呗"
}
### 返回闲聊：
{
  "chat": "接电话靠缘分，就来这找我把",
  "err_no": 0,
  "status": 200
}

## 7，注意事项
### 本服务只能部署在linux或者mac上，windows尚不支持，因为 annoy 无法在windows运行。

## 8，语料生成工具
### /src/grammar/genbygram.py
### 模板 *.cfg
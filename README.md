# 对话系统平台

## 1，git clone
下载w2v.model.vectors.npy，放在 model/w2v 目录下

链接：https://pan.baidu.com/s/1C1qB2b6HyzOpj3eqDehhEQ 提取码：5b6y

## 2，配置语料，有三种语料，
意图语料 /data/intent

faq标准问语料 /data/faq

闲聊语料 /data/chat

## 3，pip3 install -r requirements.txt

## 4，启动服务
python server.py

## 5，接口说明：
先识别意图，如果未识别到意图，再识别faq，如果未识别到faq，最后识别闲聊
请求方式，http+post 

http://127.0.0.1:58888/chatbot

输入： 
{
    "user": "1",
    "text": "上海天气怎么样"
}
返回意图：
{
  "err_no": 0,
  "intent": "Weather",
  "slot": {
    "City": "上海"
  },
  "status": 200
}

输入：
{
    "text": "五险一金怎么缴"
}
返回faq：
{
  "err_no": 0,
  "faq": "按照最低标准缴",
  "status": 200
}

输入：
{
    "text": "留个电话呗"
}
返回闲聊：
{
  "chat": "接电话靠缘分，就来这找我把",
  "err_no": 0,
  "status": 200
}

## 6，注意事项
本服务只能部署在linux或者mac上，windows尚不支持，因为 annoy 无法在windows运行。

## 7，语料生成工具
/src/grammar/genbygram.py

模板：*.cfg


## 8, todo
1，对话管理功能

2，多轮对话

3，用配置文件管理对话信息

4，改进文本相似度算法
# Cisco-Packet-Tracer-Chinese

# 摆烂中，要是有新版本出来提交一下 Issues 看到会更新新的机翻汉化

* 现已推出 Cisco Packet Tracer 8.1.1 版本完整汉化文件(由于懒出天际用 jio 糊了个 python 自动汉化, 全程谷歌翻译)

* 翻译文件基于 Cisco Packet Tracer 7.3(因为太懒，加上现在搞 HUAWEI 去了, 7.3 的汉化停了)

* ~~由于是从 0 开始汉化，如有翻译不对的地方，还麻烦各位指正一下。~~

* 当前汉化已完成 ~~5%~~ 100%机翻


## # 如何使用
下载 Chinese.ptl

将文件需要放到:
Windows:
```
C:\Program Files\Cisco Packet Tracer 7.3\languages\
```
MacOS:
```
/Applications/Cisco Packet Tracer 7.3/Cisco Packet Tracer 7.3.app/Contents/LANGUAGES
```

在放置文件后还需要进入软件下将 Languages 栏设为 Chinese.ptl (感谢 [gorgeousdays](https://github.com/gorgeousdays) 提醒)
```
Options\Preferences\Interface 
```


## # 加入汉化队伍

### ## 获取汉化文件
#### 方法一（需要了解一下 git 的使用）：
把项目 clone 到本地
```
git clone https://github.com/EmotionalAmo/Cisco-Packet-Tracer-Chinese.git
```

#### 方法二：

点击下面的链接下载文件

https://github.com/EmotionalAmo/Cisco-Packet-Tracer-Chinese/archive/master.zip


### ## 汉化&打包
#### 汉化：
使用 packet tracer 安装时自带的 Qt Linguist 打开
```
Chinese.ts
```

#### 打包：
在选项栏的 file 里找到 release as...
导出文件时选择 ALL files 格式并把文件后缀改成 ptl
现在，你就可以把导出的 *.ptl 放到 languages 文件夹下检查自己汉化的成果了


### ## 文件上传
#### 方法一（需要了解一下 git 的使用）：
使用 git 上传前请先用邮件通知我

#### 方法二（邮件）：
通过邮件发送给我
标题格式 你的昵称-CPT汉化
# 
#### 贡献者：等待你们加入

PyReportMyIP
============
This is a program that automatically updates the IP addresses to server.  

## Features
* Automatic reconnect
* Self-upgrade

## Install
step 1. 安裝必要的第三方套件 requests  
```
pip install requests
```
step 2. 安裝 report-myip.py  
```
cp report-myip.py ~/bin
```
step 3. 開機自動啟動 report-myip.py  
將下列 user 與 server_ip 替換, 插入到 /etc/rc.local 裡的 exit 0 之前  
```
/home/{user}/bin/report-myip.py {server_ip} &
```

## How to Use
start report-myip.py (client)  
```
report-myip.py [server_ip]
```

start myip-server.py (server)  
```
myip-server.py [ip]
```

## 如何線上更新 report-myip.py
step 1. 放置新版的 report-myip.py 在 startSimpleHTTPServer.sh 同個目錄下  
step 2. 啟動 startSimpleHTTPServer.sh 腳本  
step 3. 修改 myip-server.py 裡的 clientLeastVersion 版號 (版號一定要更新, 否則版號一樣是不會自動更新的)  
step 4. 啟動 myip-server.py  
不久後, 舊版 report-myip.py 就會檢查到有新版本可以更新, 就會自動下載更新了！  

## System Requirement
Python  

## Develop Environment
Python 2.7.x  

## License
PyReportMyIP is published under the MIT license.  
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
step 2. 安裝 reportMyIP.py  
```
cp reportMyIP.py ~/bin
```
step 3. 開機自動啟動 reportMyIP.py  
將下列 user 與 server_ip 替換, 插入到 /etc/rc.local 裡的 exit 0 之前  
```
/home/{user}/bin/reportMyIP.py {server_ip} &
```

## How to Use
start reportMyIP.py (client)  
```
reportMyIP.py [server_ip]
```

start devceIPServer.py (server)  
```
devceIPServer.py [ip]
```

## 如何線上更新 reportMyIP.py
step 1. 放置新版的 reportMyIP.py 在 startSimpleHTTPServer.sh 同個目錄下  
step 2. 啟動 startSimpleHTTPServer.sh 腳本  
step 3. 修改 devceIPServer.py 裡的 clientLeastVersion 版號 (版號一定要更新, 否則版號一樣是不會自動更新的)  
step 4. 啟動 devceIPServer.py  
不久後, 舊版 reportMyIP.py 就會檢查到有新版本可以更新, 就會自動下載更新了！  

## System Requirement
Python  

## Develop Environment
Python 2.7.x  

## License
PyReportMyIP is published under the MIT license.  
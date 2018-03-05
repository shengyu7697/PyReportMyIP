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

## System Requirement
Python  

## Develop Environment
Python 2.7.x  

## License
PyReportMyIP is published under the MIT license.  
#!/bin/bash
# 注意：平台对端口和防火墙设置有约定，端口需要大于10000
# 防火墙更改目录：/etc/firewalld/zones/public.xml
# 防火墙重启命令：systemctl reload firewalld
# 占用端口号：10013
uvicorn agent_server:app --host localhost --port 10013 --reload > agent_server.log &

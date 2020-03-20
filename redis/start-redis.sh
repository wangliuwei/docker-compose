#!/bin/sh


start(){
	redis-server /etc/redis/redis.conf &
	redis-server /etc/redis/6380.conf &
	redis-server /etc/redis/6381.conf &
	redis-server /etc/redis/6382.conf &
	redis-server /etc/redis/6383.conf &
	redis-server /etc/redis/6384.conf &
}

case "$1" in
    start)
        start
        ;;
esac
* nerdctl findings

```bash
neil@OFFICEPC1:~/nerd$ nerdctl run -d --name nginx -p 8010:80 nginx:alpine
8e834c8fa608c92eda87ff35879956c0a9c2f4fa7bd787f89b32b1a9cd58db8a
neil@OFFICEPC1:~/nerd$ nerdctl ps
CONTAINER ID    IMAGE                             COMMAND                   CREATED          STATUS    PORTS                   NAMES
8e834c8fa608    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    6 seconds ago    Up        0.0.0.0:8010->80/tcp    nginx
neil@OFFICEPC1:~/nerd$ nerdctl ps -q
8e834c8fa608
neil@OFFICEPC1:~/nerd$ 
```

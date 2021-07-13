# 多用dockerfile，可以依据CMD不同分别执行不同的功能

FROM python:slim-buster

COPY requirement.txt .

RUN python3 -m pip install   -i https://pypi.tuna.tsinghua.edu.cn/simple   -r requirement.txt

WORKDIR /app

COPY . .

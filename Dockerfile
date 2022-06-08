FROM FROM --platform=linux/x86_64 python:3.7.13-buster

COPY deep_pv /deep_pv
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

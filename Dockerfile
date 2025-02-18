FROM python:3.7

RUN mkdir /app \
    && python3 -m pip install \
    Flask==2.2.5  \
    requests \
    toml==0.10.2 \
    SQLAlchemy==2.0.19 \
    -i  https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

ADD ./sdk /app/sdk
ADD ./notice.py /app/notice.py
ADD ./notice.toml /app/notice.toml

EXPOSE 5000
ENTRYPOINT ["python3","/app/notice.py"]

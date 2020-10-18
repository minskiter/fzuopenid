FROM ubuntu:18.04 as BASE
WORKDIR /proj
COPY . .
# 换源
RUN chmod +x ./changesource.sh && ./changesource.sh
# 安装依赖
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y python3 python3-pip nodejs tesseract-ocr
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 80
ENV LC_ALL C.UTF-8
ENV AppToken "SOSD"
ENTRYPOINT [ "python3","app.py" ]
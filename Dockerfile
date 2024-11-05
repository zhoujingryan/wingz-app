FROM dockerpull.org/python:3.10-bullseye

RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin

COPY ./requirements.txt /app/wingz-app/requirements.txt
RUN pip install -r /app/wingz-app/requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /app/wingz-app
WORKDIR /app/wingz-app

ENV DJANGO_SETTINGS_MODULE=wingz.settings.deploy
RUN python manage.py migrate
ENTRYPOINT ["gunicorn", "-c", "etc/gunicorn.conf.py", "wingz.wsgi:application"]

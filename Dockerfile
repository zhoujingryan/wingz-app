FROM dockerpull.org/python:3.10-bullseye
RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y binutils libproj-dev gdal-bin


COPY ./ /app/wingz-app
WORKDIR /app/wingz-app

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

RUN if echo "$DJANGO_SETTINGS_MODULE" | grep -q "develop"; then \
      pip install -r /app/wingz-app/requirements-dev.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple; \
    else \
      pip install -r /app/wingz-app/requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple; \
    fi

RUN python manage.py migrate
ENTRYPOINT ["gunicorn", "-c", "etc/gunicorn.conf.py", "wingz.wsgi:application"]

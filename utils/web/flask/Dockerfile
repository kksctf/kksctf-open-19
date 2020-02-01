FROM python:3
RUN pip install flask
RUN pip install Flask-WTF
RUN pip install psycopg2
RUN pip install uwsgi

RUN groupadd -r ctf && useradd -r -g ctf ctf

ENTRYPOINT [ "/usr/bin/python3", "/main.py" ]

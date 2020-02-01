FROM flask:latest

ADD --chown=root:ctf ./deploy /code
RUN chmod -R u=rX,g=rX,o-rwX /code

ENTRYPOINT [ "/usr/bin/python3", "/code/run.py" ]

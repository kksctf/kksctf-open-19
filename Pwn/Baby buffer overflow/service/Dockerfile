FROM pwn_container_x32:latest

RUN apt-get install strace

ADD ./src/build /home/ctf/task

RUN chown root:ctf /home/ctf/task/* && chmod 550 /home/ctf/task/*

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

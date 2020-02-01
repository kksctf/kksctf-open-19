# FROM pwn_container_x32:latest
FROM pwn_container_x32:latest

ADD ./src/build /home/ctf/task

RUN chown -R root:ctf /home/ctf/task/ && chmod -R 550 /home/ctf/task/

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

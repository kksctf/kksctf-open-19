# FROM pwn_container_x32:latest
FROM pwn_container:latest

ADD ./src/build /home/ctf/task
ADD ./redir.sh /home/ctf/redir.sh

RUN chown -R root:ctf /home/ctf/ && chmod -R 550 /home/ctf/

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

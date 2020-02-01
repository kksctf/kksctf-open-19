FROM pwn_container:latest

ADD ./task/ /home/ctf/task

RUN chown root:ctf /home/ctf/task/chall && chmod 550 /home/ctf/task/chall

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

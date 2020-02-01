# FROM pwn_container_x32:latest
FROM pwn_container_x32:latest

ADD ./src/build /home/ctf/task
ADD ./src/build/glibc2.27x86 /opt/glibc2.27x86

RUN chown -R root:root /opt/glibc2.27x86 && chmod -R 555 /opt/glibc2.27x86
RUN chown -R root:ctf /home/ctf/task/ && chmod -R 550 /home/ctf/task/

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

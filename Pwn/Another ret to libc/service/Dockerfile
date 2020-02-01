# FROM pwn_container_x32:latest
FROM pwn_container_x32:latest

# RUN apt-get install -y python python-pip python-dev git libssl-dev libffi-dev build-essential
# RUN pip install pwntools

ADD ./src/build /home/ctf/task
ADD ctf.xinetd /etc/xinetd.d/ctf
# ADD ./redir.sh /home/ctf/redir.sh

RUN chown -R root:ctf /home/ctf/task/ && chmod -R 550 /home/ctf/task/

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

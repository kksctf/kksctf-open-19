# FROM pwn_container_x32:latest
FROM pwn_container:latest

RUN apt-get install -y python3

ADD ./src/sort.py /home/ctf/task/chall
ADD ./src/emergency_instructions.txt /home/ctf/task/emergency_instructions.txt

RUN chown -R root:ctf /home/ctf/task/ && chmod -R 550 /home/ctf/task/

RUN service xinetd stop
CMD ["/usr/sbin/xinetd", "-dontfork"]

FROM phusion/baseimage:master-amd64
ENV DEBIAN_FRONTEND noninteractive

RUN dpkg --add-architecture i386 && \
    apt-get -y update && \
    apt install -y \
    libc6:i386 \
    g++-multilib \
    strace \
    ltrace \
    file --fix-missing

RUN apt-get install -y xinetd

RUN groupadd -r ctf && useradd -r -g ctf ctf
ADD ctf.xinetd /etc/xinetd.d/ctf
ADD ./files/ /home/ctf/

RUN chmod 440 /home/ctf/*
RUN chown -R root:ctf /home/ctf
RUN chmod 550 /home/ctf/redir.sh

RUN service xinetd restart
CMD ["/usr/sbin/xinetd", "-dontfork"]

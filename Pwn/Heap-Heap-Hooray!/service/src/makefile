libc_version=2.27x86
all: ; gcc -z execstack -no-pie -Wl,-z,norelro -m32 -mpreferred-stack-boundary=2 -o df ./double_free.c
run: df;LD_PRELOAD="/opt/glibc${libc_version}/lib/libc.so.6 /opt/glibc${libc_version}/lib/libpthread.so.0 /opt/glibc${libc_version}/lib/ld-linux.so.2" ./df


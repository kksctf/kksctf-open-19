#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win(int param){
    FILE* f = fopen("flag.txt", "r");
    if(!f) {
        printf("flag not found\n");
        return;
    }
    char buf[29];
    fgets(buf, 29, f);
    if(param != 0xcafebabe){
        printf("Almost there :)\n");
        exit(0);
    }
    printf("Here it comes: %s\n", buf);
}

void read_wrapper(char* dest){
    gets(dest);
    int i;
    for(i=0; i < strlen(dest); i++)
        if(dest[i] >= 'A' && dest[i] <= 'Z')
            dest[i] += 32;
}

int main(int argc, char** argv){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    printf("We have prepared a buffer overflow for you\n");
    printf("Can you get use of it?\n");
    
    char buf[252];        
	printf("Enter your name: ");
    read_wrapper(buf);
    printf("Hello, %s!\n", buf);
    return 0;
}


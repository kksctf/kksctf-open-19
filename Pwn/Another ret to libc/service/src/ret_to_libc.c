#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

uint8_t Gamma[] = "13731337";
uint8_t priveleged[] = {0x50,0x57,0x5a,0x5a, 0x5f, 0x52, 0x57, 0x5a, 0x00};

typedef struct user{
    uint8_t user_name[256];
    uint32_t age;
    uint8_t id[9];
    void (*change_name)(struct user*);
    void (*print_info)(struct user*);
}user;

void print_user_info(user* usr){
    int i ;
    printf("Information about user #");
    for(i=0;i<8; printf("%02x",usr->id[i++]));
    printf(":\nname: %s\n", usr->user_name);
    printf("age: %d\n", usr->age);
    if(!strcmp(priveleged, usr->id)){
        FILE* f = fopen("TOTALY_NOTHING_INTERESTING_HERE.txt", "r");
        char buf[32];
        fgets(buf, 32, f);
        printf("%s\n", buf);        
    }
}

void change_user_name(user* usr){
    printf("Enter new name: ");
    uint8_t tmp[256];
    fgets(tmp, 256, stdin);
    if(!strcmp(tmp, usr->user_name)){
        printf("New name can not match with the old one!\n");
    }else{
        sprintf(usr->user_name, tmp);
        usr->user_name[256] = 0;
        printf("Your name has been seccessfully changed!\n");
    }
}

user* create_user(){
    int i;
    user* usr = (user*)calloc(1, sizeof(user));
    printf("Enter your name: ");
    fgets(usr->user_name, 256, stdin);
    printf("Enter your age: ");
    fgets((uint8_t*)&usr->age, 4, stdin);
    if((usr->age = atoi((uint8_t*)&usr->age))<=0){
        printf("Invalid age!\n");
        exit(-1);
    }
    snprintf(usr->id, 9, usr->user_name);
    for(i=0; i<8; i++)
        usr->id[i] ^= Gamma[i];
    usr->print_info = print_user_info;
    usr->change_name = change_user_name;
    return usr;
}

int main(){
    int tmp;
    
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    user* usr = create_user();
    int flag;
    while(1){
        while(getc(stdin)!='\n');
        printf("\nMenu:\n");
        printf("1) Get information\n");
        printf("2) Change name\n");
        printf("3) Quit\n");
        printf("> ");
        tmp = getc(stdin);
        getc(stdin);
        switch(tmp){
            case '1':{
                usr->print_info(usr);
                break;
            }case '2':{
                usr->change_name(usr);
                break;
            }case '3':{
                exit(0);
            }
        }
    }
    return 0;
}


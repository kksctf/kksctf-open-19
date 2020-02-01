#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

char* chunks[32];

int allocate_chunk(uint32_t*);
void list_chunks_content(uint32_t*);
int delete_chunk(uint32_t*);

int main(int argc, char** argv){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    char tmp;
    uint32_t map=0;
    while(1){
        printf("\n___MENU___\n");
        printf("1) allocate chunk\n");
        printf("2) list chunks\n");
        printf("3) free chunk\n");
        printf("4) quit\n>");
        scanf("%c", &tmp);
        switch(tmp){
            case '1':
                allocate_chunk(&map);
                break;
            case '2':
                list_chunks_content(&map);
                break;
            case '3':
                delete_chunk(&map);
                break;
            case '4':
                exit(0);
            default:
                printf("invalid choice!\n");
        }
        while(getc(stdin) != '\n');
    }
    return 0;
}

int allocate_chunk(uint32_t* map){
    int tmp, size;
    printf("Enter chunk ID: ");
    scanf("%d", &tmp);
    if(tmp<0 || tmp>=32){
        printf("ID must be in range from 0 to 31\n");
        return -1;
    }
    if(*map & (1<<tmp)){
        printf("Chunk with %d ID is already allocated\n", tmp);
        return -1;
    }
    printf("Enter chunk size: ");
    scanf("%d", &size);
    if(size <=0 || size>0x80){
        printf("size must be in range from 1 to 128\n");
        return -1;
    }
    *map |= 1<<tmp;
    chunks[tmp] = (char*)malloc(size);
    printf("Your message: ");
    while(getc(stdin) != '\n');
    fgets(chunks[tmp], size, stdin);
    printf("Done!\n");
    return 0;
}

void list_chunks_content(uint32_t* map){
    int i;
    for(i=0; i<32; i++){
        if(*map & (1<<i))
            printf(chunks[i]);
    }
        
}

int delete_chunk(uint32_t* map){
    int tmp;
    printf("Enter chunk ID: ");
    scanf("%d", &tmp);
    if(tmp<0 | tmp>=32){
        printf("ID must be in range from 0 to 31\n");
        return -1;
    }
    if(!(*map & (1<<tmp))){
        printf("Chunk with %d ID is not allocated\n", tmp);
        return -1;
    }
    *map ^= 1<<tmp;
    free(chunks[tmp]);
    printf("Done!\n");
    return 0;
}

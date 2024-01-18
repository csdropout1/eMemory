//
//  my_malloc-driver.c
//  Lab1: Malloc
//  This file is for testing your code only
//  You will not turn it in
//

#include "my_malloc.h"
#include "stdio.h"

int main(int argc, const char * argv[])
{
    printf("THIS IS THE BEGINNING OF THE END\n");
    FreeListNode t = free_list_begin();
    int *jiyun = my_malloc(16);
    t = free_list_begin();
    printf("1 %d\n", t->size);
    int *jiyun2 = my_malloc(1000);
    t = free_list_begin();
    printf("2 %d\n", t->size);
    int *jiyun3 = my_malloc(8000);
    t = free_list_begin();
    printf("3 %d\n", t->size);

    my_free(jiyun);
    t = free_list_begin();
    printf("4 %d\n", t->size);

    my_free(jiyun2);
    t = free_list_begin();
    printf("5 %d\n", t->size);

    my_free(jiyun3);
    t = free_list_begin();
    printf("6 %d\n", t->size);

    // int ** jiyun4 = my_malloc(16);
    // jiyun4[0] = my_malloc(4*sizeof(int));
    // jiyun4[1] = my_malloc(4*sizeof(int));
    // jiyun4[2] = my_malloc(4*sizeof(int));
    // jiyun4[3] = my_malloc(4*sizeof(int));

    // jiyun4[3][0] = 5;
    // jiyun4[0][3] = 8;
    int *jiyunIQ = my_malloc(16);
    int *jiyun5 = my_malloc(1000);
    int *jiyun6 = my_malloc(7152);
    int *jiyun7 = my_malloc(8000);
    
    t = free_list_begin();
    printf("Free? %d\n", t->size); 
    
}

// gcc -g my_malloc.c jiyu.c -o test
// ./test    

/*
b' \x[99 chars]192\n\nFirst node at: 0x0\nSize of free chunk:[137 chars]\n\n' 
b' \x[99 chars]192\nNext node at: 0x4720\nSize of free chunk:[229 chars]\n\n'
 : Large Allocation Test Failed -- Large chunks (>= 8192 bytes) are not allocated correctly.
*/
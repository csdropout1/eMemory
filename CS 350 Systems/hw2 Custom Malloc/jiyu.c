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
    // jiyun[9999] = 15;
    // // int *jiyun2 = my_malloc(16);

    my_free(jiyun);
    int *jiyun2 = my_malloc(16);
    int *jiyun3 = my_malloc(16);
    // my_free(jiyun2);

    // t = free_list_begin();
    // printf("Free? %d\n", jiyun[9999]); 
    // printf("Free? %d\n", t->flink->size); 
    // printf("Free? %d\n", t->flink->size); 
    
    // coalesce_free_list();
    t = free_list_begin();
    printf("Free? %d\n", t->size);

    // printf("THIS IS THE BEGINNING OF THE END\n");
    // FreeListNode t = free_list_begin();
    // int *jiyun = my_malloc(16);
    // t = free_list_begin();
    // printf("1 %d\n", t->size);
    // int *jiyun2 = my_malloc(1000);
    // t = free_list_begin();
    // printf("2 %d\n", t->size);
    // int *jiyun3 = my_malloc(8000);
    // t = free_list_begin();
    // printf("3 %d\n", t->size);

    // my_free(jiyun);
    // t = free_list_begin();
    // printf("4 %d\n", t->size);

    // my_free(jiyun2);
    // t = free_list_begin();
    // printf("5 %d\n", t->size);

    // my_free(jiyun3);
    // t = free_list_begin();
    // printf("6 %d\n", t->size);

    // // int ** jiyun4 = my_malloc(16);
    // // jiyun4[0] = my_malloc(4*sizeof(int));
    // // jiyun4[1] = my_malloc(4*sizeof(int));
    // // jiyun4[2] = my_malloc(4*sizeof(int));
    // // jiyun4[3] = my_malloc(4*sizeof(int));

    // // jiyun4[3][0] = 5;
    // // jiyun4[0][3] = 8;
    // // int *jiyunIQ = my_malloc(16);
    // // int *jiyun5 = my_malloc(1000);
    // // int *jiyun6 = my_malloc(7152);
    // // int *jiyun7 = my_malloc(8000);
    
    // coalesce_free_list();
    // t = free_list_begin();
    // printf("Free? %d\n", t->size); 
}

// gcc -g my_malloc.c jiyu.c -o test
// ./test    
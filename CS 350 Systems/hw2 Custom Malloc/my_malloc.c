/* THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR . MICROL CHEN */
//tche284 - MICROL CHEN

//
//  my_malloc.c
//  Lab1: Malloc
//

#include "my_malloc.h"
#include <unistd.h>
#define MAGIC 76798669

MyErrorNo my_errno=MYNOERROR;
FreeListNode* head = NULL; //One permitted global variable for head of link list

void *my_malloc(uint32_t size){ //returns allocated memory based on size
    void *ptr = NULL;
    uint32_t end = 0;
    uint32_t padding = 0;
    FreeListNode h;
    char *sbrk_errors = 0;
    h = free_list_begin();
    padding = (size%CHUNKHEADERSIZE != 0)*(CHUNKHEADERSIZE-(size%CHUNKHEADERSIZE)); // complement for mod CHUNKHEADERSIZE given size
    if (head !=NULL){ // Do we have free memory?
        FreeListNode current = free_list_begin();
        FreeListNode prev = NULL;
        while (current->size < size+CHUNKHEADERSIZE+padding && current->flink != NULL) {//trasnverse until we find a fit or end
            prev = current;
            current = current->flink;
        }
        if (current->size >= size+CHUNKHEADERSIZE+padding) { //reduce the size from first fit and set up variables to perform malloc
            if (prev == NULL) { //first node case
                ptr = h;
                end = h->size;
                head = (FreeListNode*)h->flink;
            } else {
                ptr = current;
                end = current->size;
                prev->flink = current->flink; 
            }
        } else {//passes into new memory allocation if no free memory avaliable fits.
            end = size+CHUNKHEADERSIZE+padding;
            end = ((end >8192)*(end))+ ((end <= 8192)*8192); //branchless set 8192 to sbrk if small allocation and just big enough size for large allocation
            ptr = sbrk(0);
            sbrk(end);
            if (sbrk_errors == (char*)-1) {
                my_errno = MYENOMEM;
                return NULL;
            }
        }

    } else { //allocates new memory from sbrk
        end = size+CHUNKHEADERSIZE+padding;
        end = ((end >8192)*(end))+ ((end <= 8192)*8192); //branchless set 8192 to sbrk if small allocation and just big enough size for large allocation

        ptr = sbrk(0);
        sbrk(end);
        if (sbrk_errors == (char*)-1) {
            my_errno = MYENOMEM;
            return NULL;
        }
    } 
    *((int*)ptr) = CHUNKHEADERSIZE + size + padding; //setting size
    ptr += 4;
    *((int*)ptr) = MAGIC;
    ptr += 4;
    if (end - (CHUNKHEADERSIZE + size + padding) < 16) {
        *((int*)(ptr-CHUNKHEADERSIZE)) = end; //dont split sbrk memory if remaining is too small, re-adjust size
        return ptr;
    
    } else { //set up the freelist node for the remaining memory
        ptr += (size + padding); 
        h = free_list_begin();
        FreeListNode new;
        new = (FreeListNode)ptr;
        new->size = end - (CHUNKHEADERSIZE + size + padding); //remaining size
        new->flink = NULL;
        ptr -= (size + padding); //reset the ptr to what we want to give the user
        if (h == NULL) {
            head = (FreeListNode*)new;
        } else { //insert node into list
            FreeListNode prev = NULL;
            while (h < new && h->flink != NULL) {
                prev = h;
                h = h->flink;
            }
            if (h > new) {
                if (prev == NULL) {
                    new->flink = free_list_begin();
                    head = (FreeListNode*)new;
                } else {
                    new->flink = h;
                    prev->flink = new;
                }
            } else {
                h->flink = new;
            }
        }
        return ptr;
    }
}
      
void my_free(void *ptr){ // frees memory based on address
    uint32_t size = 0;
    if (ptr == NULL)
        my_errno=MYBADFREEPTR;

    FreeListNode h;
    h = free_list_begin();
    ptr -= 4; //ptr at magic
    if (*((int*)ptr) == MAGIC) {
        ptr -= 4; //ptr at size
        size = *((uint32_t*)ptr);
        // set up new node
        FreeListNode new;
        new = (FreeListNode)ptr;
        new->size = size; 
        new->flink = NULL;
        if (h == NULL) {
            head = (FreeListNode*)new;
        } else { //insert node
            FreeListNode prev = NULL;
            while (h < new && h->flink != NULL){ //transveral to proper place
                prev = h;
                h = h->flink;
            }
            if (h > new) {
                if (prev == NULL) {
                    new->flink = free_list_begin();
                    head = (FreeListNode*)new;
                } else {
                    new->flink = h;
                    prev->flink = new;
                }
            } else {
                h->flink = new;
            }
        }

    } else {
        my_errno=MYBADFREEPTR;
    }
}

FreeListNode free_list_begin(){ //simply returns the node of the head using the global address for head
    return (FreeListNode)head;
}

void coalesce_free_list(){
    FreeListNode h;
    h = free_list_begin();
    
    while(h->flink != NULL) { //transverse the linklist until the end
        if ((void*)h+h->size == h->flink) {//check if two chunks are adjacent using stored size and address *coalesce if so
            h->size += h->flink->size;
            h->flink = h->flink->flink;
        } else {
            h = h->flink;
        }
    }
}


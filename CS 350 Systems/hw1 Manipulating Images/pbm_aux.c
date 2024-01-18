/* THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR . MICROL CHEN */
//tche284 - MICROL CHEN

#include "pbm.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

PPMImage * new_ppmimage( unsigned int w, unsigned int h, unsigned int m )
{//creates a ppm struct and return its address
    PPMImage *ppm = (PPMImage*)malloc(sizeof(PPMImage));
    ppm->height = h;
    ppm->width = w;
    ppm->max = m;
    for (int i = 0; i < 3; i++){
        ppm->pixmap[i] = (unsigned int**)malloc(h*sizeof(unsigned int*));
        for (int j = 0; j < h; j++) {
            ppm->pixmap[i][j] = (unsigned int*)malloc(w*sizeof(unsigned int));
        }
    }
    return ppm;
}

PBMImage * new_pbmimage( unsigned int w, unsigned int h )
{//creates a pbm struct and return its address
    PBMImage *pbm = (PBMImage*)malloc(sizeof(PPMImage));
    pbm->height = h;
    pbm->width = w;
    pbm->pixmap = (unsigned int**)malloc(h*sizeof(unsigned int*));
    for (int i = 0; i < h; i++)
        pbm->pixmap[i] = (unsigned int*)malloc(w*sizeof(unsigned int));

    return pbm;
}

PGMImage * new_pgmimage( unsigned int w, unsigned int h, unsigned int m )
{//creates a pgm struct and return its address
    PGMImage *pgm = (PGMImage*)malloc(sizeof(PGMImage));
    pgm->height = h;
    pgm->width = w;
    pgm->max = m;
    pgm->pixmap = (unsigned int**)malloc(h*sizeof(unsigned int*));
    for (int i = 0; i < h; i++)
        pgm->pixmap[i] = (unsigned int*)malloc(w*sizeof(unsigned int));
    
    return pgm;
}

void del_ppmimage( PPMImage * p )
{//frees all the malloc calls in inverse order for ppm
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < p->height; j++) {
            free(p->pixmap[i][j]);
        }
        free(p->pixmap[i]);
    }
    free(p);
}

void del_pgmimage( PGMImage * p )
{//frees all the malloc calls in inverse order for pgm
    for (int i = 0; i < p->height; i++) {
        free(p->pixmap[i]);
    }
    free(p->pixmap);
    free(p);
}

void del_pbmimage( PBMImage * p )
{//frees all the malloc calls in inverse order for pbm
    for (int i = 0; i < p->height; i++) {
        free(p->pixmap[i]);
    }
    free(p->pixmap);
    free(p);
}


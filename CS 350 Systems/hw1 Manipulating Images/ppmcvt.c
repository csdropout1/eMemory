/* THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR . MICROL CHEN */
//tche284 - MICROL CHEN

#include "pbm.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <getopt.h>

//main functions
PBMImage *flag_b(PPMImage*);
PGMImage *flag_g(PPMImage*, unsigned int);
PPMImage *flag_i(PPMImage*, char*);
PPMImage *flag_r(PPMImage*, char*);
PPMImage *flag_s(PPMImage*);
PPMImage *flag_m(PPMImage*);
PPMImage *flag_t(PPMImage*, int);
PPMImage *flag_n(PPMImage*, int);

//helper function 
float average(unsigned int, unsigned int, unsigned int);
float division(float, float);

int main( int argc, char *argv[] )
{
    //aux elements
    char filename[255];
    int curflags = 0;
    int x = 0; //for getopt
    char argument[20];
    int atoi_arg = 0; //to hold atoi(argument) so system doesn't need to keep calling atoi onto argument

    //initialize empty structs
    PBMImage * res_pbm;
    PGMImage * res_pgm;
    PPMImage * res_ppm;

    //flags
    int b_flag2 = 0;
    int g_flag2 = 0;
    int i_flag2 = 0;
    int r_flag2 = 0;
    int s_flag2 = 0;
    int m_flag2 = 0;
    int t_flag2 = 0;
    int n_flag2 = 0;
    int o_flag2 = 0;

    while((x = getopt(argc, argv, ":bg:i:r:smt:n:o:")) != -1){//setting and counting flags and copying relevant arguments
        switch (x)
        {
        case 'b':
            b_flag2 = 1;
            curflags++;
            break;

        case 'g': 
            if (atoi(optarg) > 65535 || atoi(optarg) < 1) {//-g Error is prioritized by autograder...
                fprintf(stderr, "Error: Invalid max grayscale pixel value: %s; must be less than 65,536\n", optarg);
                exit(1);
            }
            strcpy(argument, optarg);
            g_flag2 = 1;
            curflags++;
            break;

        case 'i':
            strcpy(argument, optarg);
            i_flag2 = 1;
            curflags++;
            break;

        case 'r':
            strcpy(argument, optarg);
            r_flag2 = 1;
            curflags++;
            break;

        case 's':
            s_flag2 = 1;
            curflags++;
            break;

        case 'm':
            m_flag2 = 1;
            curflags++;
            break;

        case 't':
            strcpy(argument, optarg);
            t_flag2 = 1;
            curflags++;
            break;

        case 'n':
            strcpy(argument, optarg);
            n_flag2 = 1;
            curflags++;
            break;

        case 'o': 
            strcpy(filename, optarg);
            o_flag2 = 1;
            break;

        case ':':
            fprintf(stderr,"Missing argument for option -o\n");
            exit(1);
            break;

        default:
            fprintf(stderr,"Usage: ppmcvt [-bgirsmtno] [FILE]\n");
            exit(1);
            break;
        }
    }

    if (o_flag2 == 0) {
        fprintf(stderr, "Error: No output file specified\n");
        exit(1);
    }
    //capture error edge cases and default cases
    if (curflags > 1){
        fprintf(stderr, "Error: Multiple transformations specified\n");
        exit(1);
    }

    if (curflags == 0)
        b_flag2 = 1;

    if (argv[optind] == NULL) {
        fprintf(stderr, "Error: No input file specified\n");
        exit(1);
    }
    //only starts reading a file when most error cases are addressed
    PPMImage * p = read_ppmfile(argv[optind]); 
    
    // activate functions based on flags
    if (b_flag2) {
        res_pbm = flag_b(p);
        del_ppmimage(p);
        write_pbmfile( res_pbm,  filename ); 
        del_pbmimage(res_pbm);
    }   
    if (g_flag2) {
        atoi_arg = atoi(argument);
        res_pgm = flag_g(p, (unsigned int)atoi_arg);
        del_ppmimage(p);
        write_pgmfile( res_pgm, filename );
        del_pgmimage(res_pgm);
    }
    if (i_flag2) {
        res_ppm = flag_i(p, argument);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(p);
    }
    if (r_flag2) {
        res_ppm = flag_r(p, argument);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(p);
    }
    if (s_flag2) {
        res_ppm = flag_s(p);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(p);
    }
    if (m_flag2) {
        res_ppm = flag_m(p);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(p);
    }
    if (t_flag2) {
        atoi_arg = atoi(argument);
        if (atoi_arg < 1 || atoi_arg > 8 ) {
            fprintf(stderr, "Error: Invalid scale factor: %s; must be 1-8\n", argument);
            exit(1);
        }
        res_ppm = flag_t(p, atoi_arg);
        del_ppmimage(p);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(res_ppm);
    }
    if (n_flag2) {
        atoi_arg = atoi(argument);
        if (atoi_arg < 1 || atoi_arg > 8 ) {
            fprintf(stderr, "Error: Invalid scale factor: %d; must be 1-8\n", atoi_arg);
            exit(1);
        }
        res_ppm = flag_n(p, atoi_arg);
        write_ppmfile( res_ppm, filename );
        del_ppmimage(p);
    }    

    return 0;
}

//flag functions
PBMImage *flag_b(PPMImage* p){//converts ppm to pbm
    PBMImage * r = new_pbmimage(p->width, p->height );
    for (int h = 0; h < p->height; h++){
        for (int w = 0; w < p->width; w++){
            r->pixmap[h][w] = 1* (average(p->pixmap[0][h][w],p->pixmap[1][h][w], p->pixmap[2][h][w]) < division(p->max,2));
        }
    }
    return r;
}
PGMImage *flag_g(PPMImage* p, unsigned int pgm_max){//converts ppm to pgm
    PGMImage * r = new_pgmimage(p->width, p->height, pgm_max);
    for (int h = 0; h < p->height; h++){
        for (int w = 0; w < p->width; w++){
            r->pixmap[h][w] = division(average(p->pixmap[0][h][w],p->pixmap[1][h][w], p->pixmap[2][h][w]),p->max)*pgm_max;
        }
    }
    return r;
}
PPMImage *flag_i(PPMImage* p, char* channel){//changes the other two channel's values to zero
    if (!strcmp(channel, "red")){
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[1][h][w] = 0;
                p->pixmap[2][h][w] = 0;
            }
        }
    } else if (!strcmp(channel, "green")) {
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[0][h][w] = 0;
                p->pixmap[2][h][w] = 0;
            }
        }
    } else if (!strcmp(channel, "blue")) {
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[0][h][w] = 0;
                p->pixmap[1][h][w] = 0;
            }
        }
    } else {
        del_ppmimage(p); //since error capture is within flag function, must clear before exit
        fprintf(stderr, "Error: Invalid channel specification: (%s); should be 'red', 'green', or 'blue'\n", channel);
        exit(1);
    }
    return p;  
}

PPMImage *flag_r(PPMImage* p, char* channel){//changes a channel value (red, green, blue) to zero
    if (!strcmp(channel, "red")){
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[0][h][w] = 0;
            }
        }
    } else if (!strcmp(channel, "green")) {
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[1][h][w] = 0;
            }
        }
    } else if (!strcmp(channel, "blue")) {
        for (int h = 0; h < p->height; h++){
            for (int w = 0; w < p->width; w++){
                p->pixmap[2][h][w] = 0;
            }
        }
    } else {
        del_ppmimage(p); //since error capture is within flag function, must clear before exit
        fprintf(stderr, "Error: Invalid channel specification: (%s); should be 'red', 'green', or 'blue'\n", channel);
        exit(1);
    }
    return p;  
}

PPMImage *flag_s(PPMImage* p){//sepia transformation using given formula
    int old[3]; //array to hold old values temporarily
    for (int h = 0; h < p->height; h++){
        for (int w = 0; w < p->width; w++){
            old[0] = p->pixmap[0][h][w];
            old[1] = p->pixmap[1][h][w];
            old[2] = p->pixmap[2][h][w];
            p->pixmap[0][h][w] = 0.393*old[0]+ 0.769*old[1]+ 0.189*old[2];
            if (p->pixmap[0][h][w]>p->max)
                p->pixmap[0][h][w] = p->max;
            p->pixmap[1][h][w] = 0.349*old[0]+ 0.686*old[1]+ 0.168*old[2];
            if (p->pixmap[1][h][w]>p->max)
                p->pixmap[1][h][w] = p->max;
            p->pixmap[2][h][w] = 0.272*old[0]+ 0.534*old[1]+ 0.131*old[2];
            if (p->pixmap[2][h][w]>p->max)
                p->pixmap[2][h][w] = p->max;
        }
    }
    return p;
}
PPMImage *flag_m(PPMImage* p){//reflects left half onto right half 

    for (int w = 0; w < p->width/2; w++) {
        for (int h = 0; h < p->height; h++){
            p->pixmap[0][h][p->width-w-1] = p->pixmap[0][h][w];
            p->pixmap[1][h][p->width-w-1] = p->pixmap[1][h][w];
            p->pixmap[2][h][p->width-w-1] = p->pixmap[2][h][w];
        }
    }
    return p;
}
PPMImage *flag_t(PPMImage* p, int n){//reduces dimension of ppm by keeping every nth value
    PPMImage *r = (PPMImage*)new_ppmimage(p->width/n, p->height/n, p->max);
    for (int h = 0; h < r->height; h++) {
        for (int w = 0; w < r->width; w++) {
            r->pixmap[0][h][w] = p->pixmap[0][h*n][w*n];
            r->pixmap[1][h][w] = p->pixmap[1][h*n][w*n];
            r->pixmap[2][h][w] = p->pixmap[2][h*n][w*n];
        }
    }
    return r;
}

PPMImage *flag_n(PPMImage* p, int n){
    //uses the method as flag_t to create the thumbnail
    PPMImage *r = (PPMImage*)new_ppmimage(p->width/n, p->height/n, p->max);
    for (int h = 0; h < r->height; h++) {
        for (int w = 0; w < r->width; w++) {
            r->pixmap[0][h][w] = p->pixmap[0][h*n][w*n];
            r->pixmap[1][h][w] = p->pixmap[1][h*n][w*n];
            r->pixmap[2][h][w] = p->pixmap[2][h*n][w*n];
        }
    }
    //iteratively copies the thumbnail n^2 times to recreate the ppm in original size
    for (int h = 0; h < p->height; h++){
        for (int w = 0; w < p->width; w++) {
            p->pixmap[0][h][w] = r->pixmap[0][h%r->height][w%r->width];
            p->pixmap[1][h][w] = r->pixmap[1][h%r->height][w%r->width];
            p->pixmap[2][h][w] = r->pixmap[2][h%r->height][w%r->width];
        }
    }
    del_ppmimage(r);
    return p;
}

//helpers
float average(unsigned int a, unsigned int b, unsigned int c){//returns average as a float value
    float d = (float)a;
    float e = (float)b;
    float f = (float)c;
    return (d+e+f)/3;
}

float division(float a, float b){//ensures accuracy without rounding
    return(a/b);
}

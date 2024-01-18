#include "pbm.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <getopt.h>

PBMImage *flag_b(PPMImage*);
PGMImage *flag_g(PPMImage*, int);
PPMImage *flag_i(PPMImage*, char*);
PPMImage *flag_r(PPMImage*, char*);
PPMImage *flag_s(PPMImage*);
PPMImage *flag_m(PPMImage*);
PPMImage *flag_t(PPMImage*, int);
PPMImage *flag_n(PPMImage*, int);

int main( int argc, char *argv[] )
{
    char filename[255];
    char gray[10];
    char isolate[10];
    char remove[10];
    char thumbnail[10];
    char n_thumbnail[10];
    int x = 0;
    PPMImage * p = read_ppmfile(argv[argc - 1]);
    
    while((x = getopt(argc, argv, "bg:i:r:smt:n:o:")) != -1){
        switch (x)
        {
        case 'b':
            printf("b has been read!\n");
            break;
        case 'g':
            printf("g has been read!\n");
            strcpy(gray, optarg);
            printf("%s\n", gray);
            break;
        case 'i':
            printf("i has been read!\n");
            strcpy(isolate, optarg);
            printf("%s\n", isolate);
            break;
        case 'r':
            printf("r has been read!\n");
            strcpy(remove, optarg);
            printf("%s\n", remove);
            break;
        case 's':
            printf("s has been read!\n");
            break;
        case 'm':
            printf("m has been read!\n");
            break;
        case 't':
            printf("t has been read!\n");
            strcpy(thumbnail, optarg);
            printf("%s\n", thumbnail);
            break;
        case 'n':
            printf("n has been read!\n");
            strcpy(n_thumbnail, optarg);
            printf("%s\n", n_thumbnail);
            break;
        case 'o':
            strcpy(filename, optarg);
            break;
        case '?':
            fprintf(stderr, "Option unrecognized: %c\n", optopt);
            exit(1);
            break;
        case ':' :
            fprintf(stderr, "Missing filename!\n");
            exit(1);
            break;
        default:
            break;
        }
    }

    printf("file_name = %s\n", filename);
    // int i = optind;
    // int hr = atoi(argv[i++]);

}
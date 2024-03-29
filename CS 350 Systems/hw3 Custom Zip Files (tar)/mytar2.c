/* THIS CODE WAS MY OWN WORK , IT WAS WRITTEN WITHOUT CONSULTING ANY
SOURCES OUTSIDE OF THOSE APPROVED BY THE INSTRUCTOR . MICROL CHEN */
//tche284 - MICROL CHEN

#include "inodemap.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <getopt.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <unistd.h>

// gcc -o mytar mytar.c inodemap.c
// gcc -o mytar2 mytar2.c 
// ./mytar -c -f ok.tar test & ~cs350001/mytar -c -f okk.tar test
// hexdump ok.tar && hexdump okk.tar
// ./mytar -c -f ok.tar testthree & ~cs350001/mytar -c -f okk.tar testthree
// cat ok.tar && cat okk.tar

// ~cs350001/mytar -c -f okk.tar test
// ~cs350001/mytar -t -f okk.tar
// ~cs350001/mytar -t -f ok.tar

void initiate_hash();
const char * find_inode( ino_t );
void make_inode( ino_t, const char * );
void free_inode_hash();

//flag functions:
void c_func(DIR *, char *, FILE *);
void x_func(FILE *);
void t_func(FILE *);

//helpers
void input_dir(FILE *, char*, struct stat);
void input_file(FILE *, char*, struct stat);
void input_hardlink(FILE *, char*, struct stat);
void re_times(char *, time_t);

int c_flag = 0;
int x_flag = 0;
int t_flag = 0;
int f_flag = 0;
char argument[1000];
int num_modes = 0;
const char ** inode_hash = NULL;

int main(int argc, char *argv[]) {
    int x = 0;
    int magic = 0x7261746D;
    initiate_hash();
    FILE *file;
    int length;

    while((x = getopt(argc, argv, ":cxtf:")) != -1){//setting and counting flags and copying relevant arguments
        switch (x)
        {
        case 'c':
            c_flag = 1;
            num_modes++;
            break;

        case 'x': 
            x_flag = 1;
            num_modes++;
            break;

        case 't':
            t_flag = 1;
            num_modes++;
            break;

        case 'f':
            strcpy(argument, optarg); //tar file
            f_flag = 1;
            break;

        case ':':
            fprintf(stderr,"Error: No tarfile specified\n");
            exit(-1);
            break;

        default:
            break;
        }
    }

    // Errors
    if (num_modes == 0) {
        fprintf(stderr, "Error: No mode specified\n");
        exit(-1);
    }
    if (num_modes > 1) {
        fprintf(stderr, "Error: Multiple modes specified.\n");
        exit(-1);
    }
    
    if (argv[optind] == NULL && c_flag == 1) {// No directory when one is needed
        fprintf(stderr, "Error: No directory target specified\n");
        exit(-1);
    }
    if (f_flag == 0) { //Every flag needs a tar, so this is a simple check
        fprintf(stderr, "Error: No tarfile specified\n");
        exit(-1);
    }

    char *directory = argv[optind];
    DIR *folder;
    struct stat buf;

    // Flag specifics
    if (c_flag == 1) {
        stat(directory, &buf);
        file = fopen(argument, "wb");

        if (S_ISREG(buf.st_mode)) { //must be DIR
            fprintf(stderr, "Specified target(\"%s\") is not a directory.\n", directory);
            exit(-1);
        }
        folder = opendir(directory);
        if (folder == NULL) { // check the DIR actually exist
            fprintf(stderr, "Specified target(\"%s\") does not exist.\n", directory);
            exit(-1);
        } 
        if (file == NULL) {
            perror("fopen");
            exit(-1);
        }
        
        fwrite(&magic, 4, 1, file);
        
        input_dir(file, directory, buf);

        c_func(folder, directory, file);
        if (fclose(file) == -1) {
            perror("fclose");
            exit(-1);
        }     
        if (closedir(folder) == -1) {
            perror("closedir");
            exit(-1);
        }
    } 

    if (x_flag == 1 || t_flag == 1) {
        if (stat(argument, &buf) == -1) {
            perror("stat");
            exit(-1);
        }
        file = fopen(argument, "rb");
        if (file == NULL) {
            fprintf(stderr, "Error: Specified target(\"%s\" does not exist.)\n", argument);
            exit(-1);
        }
        int check;  // for magic number
        fread(&check, 1, 4, file); 
        if (check != magic) {
            fprintf(stderr, "Error: Bad magic number (%d), should be %d.\n", check, magic);
            exit(-1);
        }
        if (x_flag == 1) {
            while (!feof(file)) {
                fread(&magic, 1, 1, file); // Ends condition if it reads pass EOF
                if (feof(file))
                    break;
                x_func(file);
            }
        }
        if (t_flag == 1) {
            while (!feof(file)) {
                fread(&magic, 1, 1, file); // Ends condition if it reads pass EOF
                if (feof(file))
                    break;
                t_func(file);
            }
        }
        fclose(file);
    }
    free_inode_hash();
    exit(0);
    return 0;
}

void c_func(DIR *dir, char *fd, FILE *tar){ //recursive dfs on DIR
    struct dirent *ent;
    struct stat buf;

    while ((ent = readdir(dir)) != NULL) { // read all files
        if (ent == NULL)
            perror("readdir");

        if (!strcmp(ent->d_name, ".") || !strcmp(ent->d_name, "..")) 
            continue; //skip soft links

        char path[1000];
        strcpy(path, fd);
        strcat(path, "/");
        strcat(path, ent->d_name);
        if (stat(path, &buf) == -1){
            perror("stat");
            exit(-1);
        }

        if (ent->d_type == DT_REG) {
            if(find_inode(buf.st_ino) == NULL) {
                make_inode(buf.st_ino, path);
                input_file(tar, path, buf);
            } else {
                input_hardlink(tar, path, buf);
            }
        }

        if (ent->d_type == DT_DIR) {
            DIR *temp_folder = opendir(path);
            input_dir(tar, path, buf); 
            c_func(temp_folder, path, tar); // recursively call the next dir
            closedir(temp_folder);
        }
            
    }

}
void x_func(FILE *f){
    if (fseek(f, -1, SEEK_CUR) == -1) {
        perror("fseek");
        exit(-1);
    } // Off sets the EOF check
    char content_dump[1001];
    ino_t inodeNum;
    if (fread(&inodeNum, 1, sizeof(ino_t), f) == -1) {
        perror("fread");
        exit(-1);
    } // inode
    // rm -r testthree && gcc -o mytar mytar.c inodemap.c && ./mytar -x -f ok.tar
    const char *temp = find_inode(inodeNum);
    printf(" OUTSIDE 123: %s\n", temp);

    int nameLenght;
    if (fread(&nameLenght, 1, sizeof(int), f) == -1) {
        perror("fread");
        exit(-1);   
    } // name length

    char name[nameLenght+1];

    if (fread(name, 1, nameLenght, f) == -1) {
        perror("fread");
        exit(-1);
    } // file name
    name[nameLenght] = '\0';
    printf("This is the : INODE : %lu\n", inodeNum);
    printf(" OUTSIDE: %s\n", name);

    if ((temp = find_inode(inodeNum)) != NULL) {
        if (link(temp, name) == -1) {
            printf(" INSIDE: %s\n", name);
            printf(" INSIDE2: %s\n", temp);
            perror("link");
            exit(-1);
        }
    }

    mode_t mode;
    if (fread(&mode, 1, sizeof(mode_t), f) == -1) {
        perror("fread");
        exit(-1);
    } // mode
    mode_t mode_permissions = mode & (S_IRWXU | S_IRWXG | S_IRWXO);
    time_t mtime;

    if (S_ISREG(mode)) {
        make_inode(inodeNum, name);
        printf("STORED: %s INDOE: %lu\n", name, inodeNum);
        if (fread(&mtime, 1, sizeof(time_t), f) == -1) {
            perror("fread");
            exit(-1);
        } // mtimes

        off_t file_size = 0;
        if (fread(&file_size, 1, sizeof(off_t), f) == -1) {
            perror("fread");
            exit(-1);
        } // filesize

        FILE *new;
        new = fopen(name, "w");
        if (new == NULL) {
            perror("fopen");
            exit(-1);
        }

        while (file_size > 0) { // clean up
            if (fread(content_dump, 1, ((file_size < 1000)*file_size + (file_size > 1000)*1000), f) == -1) {
                perror("fread");
                exit(-1);
            } // file content
            fprintf(new, "%s", content_dump);
            file_size -= ((file_size < 1000)*file_size + (file_size > 1000)*1000);
        }
        fclose(new);
        if (chmod(name, mode) == -1) {
            perror("chmod");
            exit(-1);
        }
        re_times(name, mtime);
        printf("STORED valid: %s\n", find_inode(inodeNum));

    } else if (S_ISDIR(mode)) {
        if (fread(&mtime, 1, sizeof(time_t), f) == -1) {
            perror("fread");
            exit(-1);
        }// mtimes
        if (mkdir(name, mode_permissions) == -1){
            perror("mkdir");
            exit(-1);
        } 
    } else {
        fseek(f, -sizeof(mode_t), SEEK_CUR);
    }
}
void t_func(FILE *f){
    if (fseek(f, -1, SEEK_CUR) == -1) {
        perror("fseek");
        exit(-1);
    } // Off sets the EOF check
    char content_dump[1001];
    ino_t inodeNum;
    if (fread(&inodeNum, 1, sizeof(ino_t), f) == -1) {
        perror("fread");
        exit(-1);
    } // inode
    int nameLenght;
    if (fread(&nameLenght, 1, sizeof(int), f) == -1) {
        perror("fread");
        exit(-1);
    } // name length
    char name[nameLenght+1];

    if (fread(name, 1, nameLenght, f) == -1) {
        perror("fread");
        exit(-1);
    } // file name
    name[nameLenght] = '\0';
    

    if (find_inode(inodeNum) != NULL) {
        printf("%s/ -- inode: %lu\n", name, inodeNum);
    } else {
        mode_t mode;
        if (fread(&mode, 1, sizeof(mode_t), f) == -1) {
            perror("fread");
            exit(-1);
        } // mode
        mode_t mode_permissions = mode & (S_IRWXU | S_IRWXG | S_IRWXO);


        if (S_ISREG(mode)) {
            make_inode(inodeNum, name); 
            time_t mtime;
            if (fread(&mtime, 1, sizeof(time_t), f) == -1) {
                perror("fread");
                exit(-1);
            } // mtimes
        
            off_t file_size = 0;
            if (fread(&file_size, 1, sizeof(off_t), f) == -1) {
                perror("fread");
                exit(-1);
            } // filesize
            if (mode & (S_IXUSR | S_IXGRP | S_IXOTH)) {
                printf("%s* -- inode: %lu, mode: %o, mtime: %lu, size: %ld\n", name, inodeNum, mode_permissions, mtime, file_size);
            } else {
                printf("%s -- inode: %lu, mode: %o, mtime: %lu, size: %ld\n", name, inodeNum, mode_permissions, mtime, file_size);
            }
            while (file_size > 0) { // clean up
                if (fread(content_dump, 1, ((file_size < 1000)*file_size + (file_size > 1000)*1000), f) == -1) {
                    perror("fread");
                    exit(-1);
                } // file content
                file_size -= ((file_size < 1000)*file_size + (file_size > 1000)*1000);
            }

        } else if (S_ISDIR(mode)) {
            time_t mtime;
            if (fread(&mtime, 1, sizeof(time_t), f) == -1) {
                perror("fread");
                exit(-1);
            } // mtimes

            printf("%s/ -- inode: %lu, mode %o, mtime: %lu\n", name, inodeNum, mode_permissions, mtime);
        } else {
            fseek(f, -sizeof(mode_t), SEEK_CUR);
        }
    }
}

void input_dir(FILE *tar_file, char* dir, struct stat buf) {
    fwrite(&buf.st_ino, sizeof(buf.st_ino), 1, tar_file); //Inode Number (8)
    int n = strlen(dir); 
    fwrite(&n, sizeof(int), 1, tar_file); //Name Length (4)
    fwrite(dir, 1, n, tar_file); //Name (n)
    fwrite(&buf.st_mode, sizeof(buf.st_mode), 1, tar_file); //Mode (4)
    fwrite(&buf.st_mtime, sizeof(buf.st_mtime), 1, tar_file); //Modification Time (8)
}
void input_file(FILE *tar_file, char* file, struct stat buf) {
    fwrite(&buf.st_ino, sizeof(buf.st_ino), 1, tar_file); // Inode Number (8)
    int n = strlen(file);
    fwrite(&n, sizeof(int), 1, tar_file); // Name Length (4)
    fwrite(file, n, 1, tar_file); // Name (n)
    fwrite(&buf.st_mode, sizeof(buf.st_mode), 1, tar_file); // Mode (4)
    fwrite(&buf.st_mtime, sizeof(buf.st_mtime), 1, tar_file); // Modification Time (8)
    fwrite(&buf.st_size, sizeof(buf.st_size), 1, tar_file); // Size (8)
    
    FILE *f = fopen(file, "r");
    if (f == NULL) {
        perror("fopen");
        exit(-1);
    }
    int byte;
    while ((byte = fgetc(f)) != EOF) { // Content (n)
        fprintf(tar_file, "%c", byte);
    }

    fclose(f);
}
void input_hardlink(FILE *tar_file, char* file, struct stat buf) {
    fwrite(&buf.st_ino, sizeof(buf.st_ino), 1, tar_file); // Inode Number (8)
    int n = strlen(file);
    fwrite(&n, sizeof(int), 1, tar_file); // Name Length (4)
    fwrite(file, n, 1, tar_file); // Name (n)
}

void re_times(char *name, time_t mtimes) {
    struct timeval newtimes[2];
    if (gettimeofday(&newtimes[0], NULL) == -1) {
        perror("gettimeofday");
        exit(-1);
    }
    newtimes[1].tv_sec = mtimes;
    newtimes[1].tv_usec = 0;

    if (utimes(name, newtimes) == -1) {
        perror("utimes");
        exit(-1);
    }
}

// Recreated hashmap so it can be freed from memory
// Hashmap based on inodemap.c
//  Created based on Dorian Arnold on 10/8/20.
//  Copyright © 2020 Dorian Arnold. All rights reserved.

void initiate_hash() {
    inode_hash = (const char  **)calloc(1024, sizeof(char*));
} 
void make_inode( ino_t i, const char * f ){
    uint32_t mappos = i % 1024;
    char *file = (char*)malloc(strlen(f)+1);
    if (file == NULL) {
        perror("malloc");
        exit(-1);
    }
    strcpy(file, f);
    inode_hash[mappos] = file;
}
const char * find_inode( ino_t i ){
    return inode_hash[ i % 1024 ];
}

void free_inode_hash() {
    for (int i = 0; i < 1024; i++) {
        if (inode_hash[i] != NULL) {
            free((char *)inode_hash[i]);  
        }
    }

    free(inode_hash);
}
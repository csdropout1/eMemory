int main(int argc, char *argv[])
{
    bool save_flag = false;
    bool print_flag = false;
    bool file_flag = false;
    char filename[1000];
    int x = 0; 
    
    while( (x = getopt(argc, argv, ":o:ps")) != -1){
        switch (x)
        {
        case 'p':
            print_flag = true;
            break;
        case 'o':
            file_flag = true;
            strcpy(filename, optarg);
            break;
        case 's':
            save_flag = true;
            break;
        case '?':   // Means unrecognized option
            fprintf(stderr, "Option unrecognized: %c\n", optopt);
            exit(1);
            break;
        case ':':  // Means missing argument 
            fprintf(stderr, "Missing filename!\n");
            exit(1);
            break; 
        default:
            break;
        }
    }

    if (optind + 2 >= argc){
        fprintf(stderr, "Some arguments are missing!\n");
        exit(1);
    }

    int i = optind;
    int hr = atoi(argv[i++]);
    int min = atoi(argv[i++]);
    int sec = atoi(argv[i++]);

    time* time_s = get_time(hr, min, sec);
    build_time_string(time_s);

    if (save_flag && !file_flag){
        fprintf(stderr, "No output file specified to save to\n");
        exit(1);
    }

    if (save_flag){
        write_time(filename, time_s);
    }

    if (print_flag){
        printf("%s\n", time_s->time_string);
    }

    free_time(time_s);


    return 0;
}

// Construct the string in the struct
void build_time_string(time* time_s){
    sprintf(time_s->time_string, "%d:%2d:%2d", time_s->hr, time_s->min, time_s->sec);
}
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

const char *me = "label";
enum { MAGIC = 2049 };
static size_t file_end(FILE *);
static uint32_t to_int32b(uint32_t, uint32_t, uint32_t, uint32_t);

static void
usg(void)
{
    fprintf(stderr, "%s [-s int|-a] -i file.idx3\n", me);
    exit(2);
}

#define	USED(x)		if(x);else{}

int
main(int argc, char **argv)
{
    enum {OUTPUT_ALL = 1, OUTPUT_ONE = 2};
    const char *input_path;
    FILE *input_file;
    int Iflag;
    int Verbose;
    size_t pos;
    size_t size;
    uint32_t i;
    uint32_t magic;
    uint32_t n_items;
    uint32_t s;
    unsigned char bytes[4];
    unsigned char label;
    unsigned char *labels;
    int Output;

    USED(argc);
    Iflag = 0;
    Output = 0;
    Verbose = 0;
    while (*++argv != NULL && argv[0][0] == '-')
        switch (argv[0][1]) {
        case 'h':
            usg();
            break;
        case 'v':
            Verbose = 1;
            break;
        case 'i':
            argv++;
            if (argv[0] == NULL) {
                fprintf(stderr, "%s: -i needs an argument\n", me);
                exit(2);
            }
            input_path = *argv;
            Iflag = 1;
            break;
        case 'a':
            Output = OUTPUT_ALL;
            break;
        case 's':
            argv++;
            if (argv[0] == NULL) {
                fprintf(stderr, "%s: -d needs an argument\n", me);
                exit(2);
            }
            s = atoi(*argv);
            Output = OUTPUT_ONE;
            break;
        default:
            fprintf(stderr, "%s: unknown option '%s'\n", me, argv[0]);
            exit(1);
        }
    if (Output == 0) {
        fprintf(stderr, "%s: -s or -a must be set\n", me);
        exit(2);
    }
    if (Iflag == 0) {
        fprintf(stderr, "%s: -i is not set\n", me);
        exit(2);
    }
    
    if ((input_file = fopen(input_path, "r")) == NULL) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    if (fread(bytes, sizeof *bytes, 4, input_file) != 4) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    magic = to_int32b(bytes[0], bytes[1], bytes[2], bytes[3]);
    if (magic != MAGIC) {
        fprintf(stderr, "%s: magic=%d != %d\n", me, magic, MAGIC);
        exit(2);
    }
    if (fread(bytes, sizeof *bytes, 4, input_file) != 4) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    n_items = to_int32b(bytes[0], bytes[1], bytes[2], bytes[3]);
    if ((pos = ftell(input_file)) == (size_t) -1) {
        fprintf(stderr, "%s:%d: ftell failed\n", __FILE__, __LINE__);
        exit(2);
    }
    size = file_end(input_file);
    if (n_items != size - pos) {
        fprintf(stderr, "%s: items: %d\n", me, n_items);
        fprintf(stderr, "%s: size, pos: %ld %ld\n", me, size, pos);
        exit(2);
    }
    if (s >= n_items) {
        fprintf(stderr, "%s: n_items: %d >= %d\n", me, s, n_items);
        exit(2);
    }
    if (Verbose)
            fprintf(stderr, "%d", n_items);
    switch (Output) {
    case OUTPUT_ONE:
        if (fseek(input_file, s, SEEK_CUR) != 0) {
            fprintf(stderr, "%s:%d: fseek failed\n", __FILE__, __LINE__);
            exit(2);
        }
        if (fread(&label, sizeof *bytes, 1, input_file) != 1) {
            fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
            exit(2);
        }
        printf("%d\n", label);
        break;
    case OUTPUT_ALL:
        if ((labels = malloc(n_items* sizeof *labels)) == NULL) {
            fprintf(stderr, "%s: malloc failed\n", me);
            exit(2);
        }
        if (fread(labels, sizeof *bytes, n_items, input_file) != n_items) {
            fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
            exit(2);
        }
        for (i = 0; i < n_items; i++)
            printf("%d\n", labels[i]);
        free(labels);
        break;
    }
    if (fclose(input_file) != 0) {
        fprintf(stderr, "%s: fail to close '%s'\n", me, input_path);
        exit(2);
    }
    return 0;
}

static size_t
file_end(FILE * f)
{
    size_t ans;
    size_t pos;

    if ((pos = ftell(f)) == (size_t) -1) {
        fprintf(stderr, "%s:%d: ftell failed\n", __FILE__, __LINE__);
        exit(2);
    }
    if (fseek(f, 0, SEEK_END) != 0) {
        fprintf(stderr, "%s:%d: fseek failed\n", __FILE__, __LINE__);
        exit(2);
    }
    if ((ans = ftell(f)) == (size_t) -1) {
        fprintf(stderr, "%s:%d: ftell failed\n", __FILE__, __LINE__);
        exit(2);
    }
    if (fseek(f, pos, SEEK_SET) != 0) {
        fprintf(stderr, "%s:%d: fseek failed\n", __FILE__, __LINE__);
        exit(2);
    }
    return ans;
}

static uint32_t
to_int32b(uint32_t x, uint32_t y, uint32_t z, uint32_t w)
{
    return (w << 0) | (z << 8) | (y << 16) | (x << 24);
}

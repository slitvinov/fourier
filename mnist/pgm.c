#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

const char *me = "pgm";
enum { MAGIC = 2051 };
static size_t file_end(FILE *);
static uint32_t to_int32b(uint32_t, uint32_t, uint32_t, uint32_t);

static void
usg(void)
{
    fprintf(stderr, "%s -s int -i file.idx3 > file.pgm\n", me);
    exit(2);
}

#define	USED(x)		if(x);else{}
int
main(int argc, char **argv)
{
    const char *input_path;
    FILE *input_file;
    int Iflag;
    int Sflag;
    int Verbose;
    size_t pos;
    size_t size;
    uint32_t magic;
    uint32_t n_columns;
    uint32_t n_images;
    uint32_t n_rows;
    uint32_t s;
    unsigned char bytes[4];
    unsigned char *data;

    USED(argc);
    Iflag = 0;
    Sflag = 0;
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
        case 's':
            argv++;
            if (argv[0] == NULL) {
                fprintf(stderr, "%s: -d needs an argument\n", me);
                exit(2);
            }
            s = atoi(*argv);
            Sflag = 1;
            break;
        default:
            fprintf(stderr, "%s: unknown option '%s'\n", me, argv[0]);
            exit(1);
        }
    if (Sflag == 0) {
        fprintf(stderr, "%s: -s is not set\n", me);
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
    n_images = to_int32b(bytes[0], bytes[1], bytes[2], bytes[3]);
    if (fread(bytes, sizeof *bytes, 4, input_file) != 4) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    n_rows = to_int32b(bytes[0], bytes[1], bytes[2], bytes[3]);
    if (fread(bytes, sizeof *bytes, 4, input_file) != 4) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    n_columns = to_int32b(bytes[0], bytes[1], bytes[2], bytes[3]);
    if ((pos = ftell(input_file)) == (size_t) -1) {
        fprintf(stderr, "%s:%d: ftell failed\n", __FILE__, __LINE__);
        exit(2);
    }
    size = file_end(input_file);
    if (n_images * n_rows * n_columns != size - pos) {
        fprintf(stderr, "%s: images, raws, colin: %d %d %d\n", me,
                n_images, n_rows, n_columns);
        fprintf(stderr, "%s: size, pos: %ld %ld\n", me, size, pos);
        exit(2);
    }
    if (s >= n_images) {
        fprintf(stderr, "%s: n_images: %d >= %d\n", me, s, n_images);
        exit(2);
    }
    if (fseek(input_file, s * n_rows * n_columns, SEEK_CUR) != 0) {
        fprintf(stderr, "%s:%d: fseek failed\n", __FILE__, __LINE__);
        exit(2);
    }
    if ((data = malloc(n_rows * n_columns * sizeof *data)) == NULL) {
        fprintf(stderr, "%s: malloc failed\n", me);
        exit(2);
    }
    if (fread(data, sizeof *bytes, n_rows * n_columns, input_file) !=
        n_rows * n_columns) {
        fprintf(stderr, "%s: fail to read '%s'\n", me, input_path);
        exit(2);
    }
    if (Verbose)
        fprintf(stderr, "%d %d %d\n", n_images, n_rows, n_columns);
    fprintf(stdout, "P5\n");
    fprintf(stdout, "%d %d\n", n_rows, n_columns);
    fprintf(stdout, "%d\n", 0xFF);
    if (fwrite(data, sizeof *data, n_rows * n_columns, stdout) !=
        n_columns * n_rows) {
        fprintf(stderr, "%s: fail to write to stdout\n", me);
        exit(2);
    }
    free(data);
    if (fclose(input_file) != 0) {
        fprintf(stderr, "%s: fail to close '%s'\n", me, input_path);
        exit(2);
    }
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

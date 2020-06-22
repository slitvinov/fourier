.POSIX:
.SUFFIXES: .c .o
.PHONY: all install clean

CFLAGS = -Ofast -g

LINK = $(CC)
M = \
pgm\

all: $M
.o:; $(LINK) $< $(LDFLAGS) -o $@
.c.o:; $(CC) -c $(CFLAGS) $<

.c:
%: %.c

clean:; rm -f $M $(M:=.o)

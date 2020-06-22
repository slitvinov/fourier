#!/bin/sh

: ${WGET=wget}
: ${GUNZIP=gunzip}

me=fetch.sh
base=http://yann.lecun.com/exdb/mnist

err () {
    printf >&2 %s\\n "$me: $@"
    exit 2
}

"$WGET" 1>/dev/null 2>/dev/null --version || err "$WGET is not found"
"$GUNZIP" 1>/dev/null 2>/dev/null --version || err "$GUNZIP is not found"

L="\
t10k-images-idx3-ubyte.gz \
t10k-labels-idx1-ubyte.gz \
train-images-idx3-ubyte.gz \
train-labels-idx1-ubyte.gz \
"

S="\
test.images.idx3 \
test.labels.idx1 \
train.images.idx3 \
train.labels.idx1 \
"

set -- $S
for i in $L
do
    j=$1; shift
    "$WGET" -q "$base/$i" -O - | "$GUNZIP" -c > $j || err "$WGET failed"
done

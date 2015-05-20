#!/bin/bash

exec gimp --verbose -c --batch-interpreter python-fu-eval \
    -b 'execfile("button-img-gen.py")' -b 'pdb.gimp_quit(1)'

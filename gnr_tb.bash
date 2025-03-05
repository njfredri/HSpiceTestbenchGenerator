#/bin/bash

rm *.ic0
rm *.st0
rm *.tr0
rm *.tr0.lis
rm *.csv

python generateTestbench.py
hspice tb.sp > output.txt
# python tr02csv.py tb.tr0 tb.csv
# python plot_csv.py tb.csv
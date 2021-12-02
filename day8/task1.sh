#!/usr/bin/env bash

LAYER=$(cat input.txt | fold -w 150 | while read line; do echo "$(echo $line | tr -d "\n" | sed 's/[^0]//g' | wc -c) -> $line"; done | sort -n | head -n 1 | awk '{print $3}')
SUM_ONES=$(echo $LAYER | tr -d "\n" | sed 's/[^1]//g' | wc -c)
SUM_TWOS=$(echo $LAYER | tr -d "\n" | sed 's/[^2]//g' | wc -c)
echo $(($SUM_ONES * $SUM_TWOS))

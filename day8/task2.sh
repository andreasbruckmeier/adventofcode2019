#!/usr/bin/env bash

declare -a BASE_LAYER
EMPTY_STRING=$(printf "%0150d" 0)
for ((i=0; i<${#EMPTY_STRING}; i++)); do BASE_LAYER[$i]="${EMPTY_STRING:$i:1}"; done

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for LINE in $(cat input.txt | fold -w 150 | sed '1!G;h;$!d'); do
	for ((i=0; i<${#LINE}; i++)); do
		ELE="${LINE:$i:1}"
		if [[ "$ELE" == "0" || "$ELE" == "1" ]]; then
			BASE_LAYER[$i]="$ELE"
		fi
	done
done
IFS=$SAVEIFS

echo ${BASE_LAYER[@]} | tr -d " " | tr "0" " " | fold -w 25
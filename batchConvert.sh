#!/usr/bin/bash

rm ConvertedStatements/*

for chaseFile in RawStatements/*;
do 
    echo $(realpath $chaseFile)
    python3 chase_card_converter.py $(realpath $chaseFile) "$(realpath $PWD)/ConvertedStatements"
    if [ $? -eq 0 ];
    then
        rm $chaseFile
    fi
done


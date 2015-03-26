#!/bin/bash

show_help()
{
    echo help
}

main()
{
    echo not implemented yet.
}

while :
do
    case $1 in
        '-h' | '--help')
            show_help
            shift
            ;;
        *)
            break
            ;;
    esac
done

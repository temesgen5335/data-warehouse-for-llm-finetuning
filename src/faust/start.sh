#!/bin/sh
./wait-for-it.sh kafka:9092 -- faust -A app worker -l info

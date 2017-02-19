#! /bin/sh

if [ "$1" == "train" ]; then
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/train.conllx -m learn -a stackeager
elif [ "$1" == "test" ]; then
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/test.conllx -m parse
else
    echo "Invalid command argument $1."
fi



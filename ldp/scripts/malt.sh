#! /bin/sh

if [ "$1" == "train" ]; then
    python ldp/corpus_reader.py < ldp/data/original/train.dep > ldp/data/interim/train.conllx
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/data/interim/train.conllx -m learn -a stackeager
elif [ "$1" == "test" ]; then
    python ldp/corpus_reader.py < ldp/data/original/test.dep > ldp/data/interim/test.conllx
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/data/interim/test.conllx -m parse > ldp/data/interim/test.sys.conllx
    python ldp/eval.py ldp/data/interim/test.conllx ldp/data/interim/test.sys.conllx
else
    echo "Invalid command argument $1."
fi

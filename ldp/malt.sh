#! /bin/sh

if [ "$1" == "train" ]; then
    python ldp/corpus_reader.py < ldp/train.dep > ldp/train.conllx
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/train.conllx -m learn -a stackeager
elif [ "$1" == "test" ]; then
    python ldp/corpus_reader.py < ldp/test.dep > ldp/test.conllx
    java -jar ldp/maltparser/maltparser-1.9.0.jar -w ldp -c ldp-malt -i ldp/test.conllx -m parse > ldp/test.sys.conllx
    python ldp/eval.py ldp/test.conllx ldp/test.sys.conllx
else
    echo "Invalid command argument $1."
fi

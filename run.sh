#! /bin/bash

BASEDIR=C:/Gabriel/UPC/Semestre2/MUD/Labs/MUD_Lab3_DDI

./corenlp-server.sh -quiet true -port 9000 -timeout 15000 &
sleep 1

#NUM=14
#MODEL_TYPE=NB
#
#echo "Extracting features"
#python src/extract-features.py $BASEDIR/data/devel/ $NUM > files/devel.cod &
#python src/extract-features.py $BASEDIR/data/train/ $NUM | tee files/train.cod | cut -f4- > files/train.cod.cl
#
##train model
#echo "Training $MODEL_TYPE model $NUM..."
#python src/train-sklearn.py files/model.joblib files/vectorizer.joblib $MODEL_TYPE <files/train.cod.cl
## run model
#echo "Running $MODEL_TYPE model $NUM..."
#python src/predict-sklearn.py files/model.joblib files/vectorizer.joblib <files/devel.cod >files/devel.out
## evaluate results
#echo "Evaluating results for $MODEL_TYPE model $NUM..."
#python src/evaluator.py DDI $BASEDIR/data/devel/ files/devel.out >files/devel_${MODEL_TYPE}_${NUM}_test.stats

# feature extraction experimentation
#for NUM in 0 1 2 3 4 5 6; do
#for NUM in 7 8 9 10 11 12 13; do
#for NUM in 14 15 16 17 18 19; do
for NUM in 20 21 22; do

  # extract features
  echo "Extracting features"
  python src/extract-features.py $BASEDIR/data/devel/ $NUM > files/devel.cod &
  python src/extract-features.py $BASEDIR/data/train/ $NUM | tee files/train.cod | cut -f4- > files/train.cod.cl

  # Model Experimentation
  for MODEL_TYPE in NB PAC SGD; do
    # train model
    echo "Training $MODEL_TYPE model $NUM..."
    python src/train-sklearn.py files/model.joblib files/vectorizer.joblib $MODEL_TYPE <files/train.cod.cl
    # run model
    echo "Running $MODEL_TYPE model $NUM..."
    python src/predict-sklearn.py files/model.joblib files/vectorizer.joblib <files/devel.cod >files/devel.out
    # evaluate results
    echo "Evaluating results for $MODEL_TYPE model $NUM..."
    python src/evaluator.py DDI $BASEDIR/data/devel/ files/devel.out >files/devel_${MODEL_TYPE}_${NUM}.stats
  done
done

kill `cat /tmp/corenlp-server.running`


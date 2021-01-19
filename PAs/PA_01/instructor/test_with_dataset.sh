INDIR=../www
python3 decision_tree.py --inputTrainX ${INDIR}/X_train.npy --inputTrainy ${INDIR}/y_train.npy \
                         --inputTestX  ${INDIR}/X_test.npy  --inputTesty  ${INDIR}/y_test.npy --depthLimit 2

python3 decision_tree.py -demoFlag --depthLimit 2


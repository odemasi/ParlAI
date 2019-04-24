###
embedding='glove'
embeddingsize=300

### architecture ###
hiddensize=1024
historysize=2
beamsize=5
numlayers=1
bidirectional=True

### optimization ###
batchsize=32
learningrate=.001
optimizer=adam
gradientclip=1.0
lrschedulerdecay=.5
lrschedulerpatience=3
validationpatience=10
validationeverynepochs=1
validationmetric='loss'
validationmetricmode='min'

### Dictionary ###
dictminfreq=2
dictlower=True
dicttokenizer='spacy'
dictfile='tmp/'$taskname'/dict_minfreq_$dictminfreq'

### logging ###
tensorboardlog=True
gpunum=0


### task ###
# taskname='dailydialog'
# 
# 
# 
# 
# ####################################
# ############ build dict ############
# ####################################
# python examples/build_dict.py \
# -t $taskname \
# --dict-minfreq $dictminfreq \
# --dict-lower $dictlower \
# --dict-tokenizer $dicttokenizer \
# --dict-file 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
# > 'tmp/'$taskname'/dict_minfreq_'$dictminfreq'.out'
# 
# 
# 
# #############################
# ##### FACE for training #####
# #############################
# modelname='face'
# fileprefix=$modelname
# 
# 
# ####################################
# ###########  train model ###########
# ####################################
# 
# python examples/train_model.py \
# -t $taskname \
# -bs $batchsize \
# --hiddensize $hiddensize \
# --history-size $historysize \
# -emb $embedding \
# --numlayers $numlayers \
# --bidirectional $bidirectional \
# --embeddingsize $embeddingsize \
# --learningrate $learningrate \
# --optimizer $optimizer \
# --gradient-clip $gradientclip \
# --lr-scheduler-decay $lrschedulerdecay \
# --lr-scheduler-patience $lrschedulerpatience \
# --validation-patience $validationpatience \
# --validation-every-n-epochs $validationeverynepochs \
# --validation-metric $validationmetric \
# --validation-metric-mode $validationmetricmode \
# --dict-minfreq $dictminfreq \
# -vmt 'd_1' \
# --dict-lower $dictlower \
# --dict-tokenizer $dicttokenizer \
# --dict-file 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
# --tensorboard-log $tensorboardlog \
# -m $modelname \
# -mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
# > 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_train.out'
# 
# 
# 
# ####################################
# ############ eval model ############
# ####################################
# 
# 
# ### EVAL model: modified (retriever) s2s ###
# python examples/eval_model.py \
# --datatype valid \
# --history-size $historysize \
# --beam-size $beamsize \
# -m $modelname \
# -t $taskname \
# --display-examples 1 \
# -df 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
# -mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
# > 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_valid.out'
# 
# 
# ### TEST model: modified (retriever) s2s ###
# python examples/eval_model.py \
# --datatype test \
# --history-size $historysize \
# --beam-size $beamsize \
# -m $modelname \
# -t $taskname \
# --display-examples 1 \
# -df 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
# -mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
# > 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_test.out'
# 

### task ###
taskname='dailydialog'


#############################
##### FACE for training #####
#############################
modelname='face'
fileprefix=$modelname


####################################
###########  train model ###########
####################################

python examples/train_model.py \
-t $taskname \
-bs $batchsize \
--hiddensize $hiddensize \
--history-size $historysize \
-emb $embedding \
--numlayers $numlayers \
--bidirectional $bidirectional \
--embeddingsize $embeddingsize \
--learningrate $learningrate \
--optimizer $optimizer \
--gradient-clip $gradientclip \
--lr-scheduler-decay $lrschedulerdecay \
--lr-scheduler-patience $lrschedulerpatience \
--validation-patience $validationpatience \
--validation-every-n-epochs $validationeverynepochs \
--validation-metric $validationmetric \
--validation-metric-mode $validationmetricmode \
--dict-minfreq $dictminfreq \
--dict-lower $dictlower \
--dict-tokenizer $dicttokenizer \
--dict-file 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
--tensorboard-log $tensorboardlog \
-m $modelname \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_train.out'



####################################
############ eval model ############
####################################


### EVAL model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype valid \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_valid.out'


### TEST model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype test \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_test.out'

###
embedding='glove'
embeddingsize=300

### architecture ###
hiddensize=1024
historysize=2
beamsize=5
numlayers=1
bidirectional=True

### optimization ###
batchsize=32
learningrate=.001
optimizer=adam
gradientclip=1.0
lrschedulerdecay=.5
lrschedulerpatience=3
validationpatience=10
validationeverynepochs=1
validationmetric='loss'
validationmetricmode='min'

### Dictionary ###
dictminfreq=2
dictlower=True
dicttokenizer='spacy'
dictfile='tmp/'$taskname'/dict_minfreq_$dictminfreq'

### logging ###
tensorboardlog=True
gpunum=0


### task ###
taskname='cornell_movie'




####################################
############ build dict ############
####################################
python examples/build_dict.py \
-t $taskname \
--dict-minfreq $dictminfreq \
--dict-lower $dictlower \
--dict-tokenizer $dicttokenizer \
--dict-file 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/dict_minfreq_'$dictminfreq'.out'



#############################
##### FACE for training #####
#############################
modelname='face'
fileprefix=$modelname


####################################
###########  train model ###########
####################################

python examples/train_model.py \
-t $taskname \
-bs $batchsize \
--hiddensize $hiddensize \
--history-size $historysize \
-emb $embedding \
--numlayers $numlayers \
--bidirectional $bidirectional \
--embeddingsize $embeddingsize \
--learningrate $learningrate \
--optimizer $optimizer \
--gradient-clip $gradientclip \
--lr-scheduler-decay $lrschedulerdecay \
--lr-scheduler-patience $lrschedulerpatience \
--validation-patience $validationpatience \
--validation-every-n-epochs $validationeverynepochs \
--validation-metric $validationmetric \
--validation-metric-mode $validationmetricmode \
--dict-minfreq $dictminfreq \
-vmt 'd_1' \
--dict-lower $dictlower \
--dict-tokenizer $dicttokenizer \
--dict-file 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
--tensorboard-log $tensorboardlog \
-m $modelname \
-mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_train.out'



####################################
############ eval model ############
####################################


### EVAL model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype valid \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_valid.out'


### TEST model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype test \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/d1/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/d1/'$fileprefix'_minfreq_'$dictminfreq'_test.out'


### task ###
taskname='cornell_movie'


#############################
##### FACE for training #####
#############################
modelname='face'
fileprefix=$modelname


####################################
###########  train model ###########
####################################

python examples/train_model.py \
-t $taskname \
-bs $batchsize \
--hiddensize $hiddensize \
--history-size $historysize \
-emb $embedding \
--numlayers $numlayers \
--bidirectional $bidirectional \
--embeddingsize $embeddingsize \
--learningrate $learningrate \
--optimizer $optimizer \
--gradient-clip $gradientclip \
--lr-scheduler-decay $lrschedulerdecay \
--lr-scheduler-patience $lrschedulerpatience \
--validation-patience $validationpatience \
--validation-every-n-epochs $validationeverynepochs \
--validation-metric $validationmetric \
--validation-metric-mode $validationmetricmode \
--dict-minfreq $dictminfreq \
--dict-lower $dictlower \
--dict-tokenizer $dicttokenizer \
--dict-file 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
--tensorboard-log $tensorboardlog \
-m $modelname \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_train.out'



####################################
############ eval model ############
####################################


### EVAL model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype valid \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_valid.out'


### TEST model: modified (retriever) s2s ###
python examples/eval_model.py \
--datatype test \
--history-size $historysize \
--beam-size $beamsize \
-m $modelname \
-t $taskname \
--display-examples 1 \
-df 'tmp/'$taskname'/dict_minfreq_'$dictminfreq \
-mf 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq \
> 'tmp/'$taskname'/'$fileprefix'_minfreq_'$dictminfreq'_test.out'




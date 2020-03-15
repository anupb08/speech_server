#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1

stage=0
nj=1 #16
decode_nj=1
test_dir=$1
tdnnf_affix=_1b
nnet3_affix=_cleaned
skip_scoring=true
jobid=$2
part=$3

  # do thisi one time if lang is changed 
  #  utils/mkgraph.sh --self-loop-scale 1.0 data/lang $dir $dir/graph

if [ $stage -le 0 ]; then
    # Making spk2utt files
    utils/validate_data_dir.sh data/$test_dir
    utils/fix_data_dir.sh  data/$test_dir
    utils/utt2spk_to_spk2utt.pl data/$test_dir/utt2spk > data/$test_dir/spk2utt
fi

echo
echo "===== FEATURES EXTRACTION ====="
echo
# Making feats.scp files

if [ $stage -le -1 ]; then
    mfccdir=mfcc
    # Uncomment and modify arguments in scripts below if you have any problems with data sorting
    # utils/validate_data_dir.sh data/train # script for checking prepared data - here: for data/train directory
    # utils/fix_data_dir.sh data/train # tool for data proper sorting ifneeded - here: for data/train directory

    steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" $test_dir $trans_dir/test $mfccdir

    # Making cmvn.scp files
    steps/compute_cmvn_stats.sh $test_dir $trans_dir/test $mfccdir
fi


if [ $stage -le 2 ]; then
    utils/copy_data_dir.sh data/$test_dir data/${test_dir}_hires

  # do volume-perturbation on the training data prior to extracting hires
  # features; this helps make trained nnets more invariant to test data volume.

    steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf \
      --cmd "$train_cmd" data/${test_dir}_hires
    steps/compute_cmvn_stats.sh data/${test_dir}_hires
    utils/fix_data_dir.sh data/${test_dir}_hires
fi

if [ $stage -le 3 ]; then
   steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $decode_nj \
      data/${test_dir}_hires exp/nnet3${nnet3_affix}/extractor \
      exp/nnet3${nnet3_affix}/ivectors_${test_dir}_hires

   progr=$(((100 - 70)/$part))
   echo $progr
   SQL_QUERY="update jobrequest set jobstatus=$progr where jobid='$jobid'"
   mysql -u root -pmysql -D jobdb -e "$SQL_QUERY"; 
fi


if [ $stage -le 4 ]; then
   dir=exp/chain${nnet3_affix}/tdnnf${tdnnf_affix}
   steps/nnet3/decode.sh --num-threads 4 --nj $decode_nj --cmd "$decode_cmd" \
          --acwt 1.0 --post-decode-acwt 10.0 --skip-scoring $skip_scoring \
          --online-ivector-dir exp/nnet3${nnet3_affix}/ivectors_${test_dir}_hires \
          --scoring-opts "--min-lmwt 5 " \
         $dir/graph data/${test_dir}_hires $dir/decode_${test_dir} || exit 1;
      #steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" data2/lang data2/lang_rescore \
      #  data/${test_dir}_hires ${dir}/decode_${test_dir} ${test_dir}/decode_${test_dir}_rescore || exit 1
   progr=$(((100 - 50)/$part))
   SQL_QUERY="update jobrequest set jobstatus=$progr where jobid='$jobid'"
    mysql -u root -pmysql -D jobdb -e "$SQL_QUERY"; 
fi

if [ $stage -le 5 ]; then
  # Here we rescore the lattices generated at stage 17
  rnnlm_dir=exp/rnnlm_lstm_tdnn_b_averaged
  lang_dir=data2/lang_chain
  ngram_order=4

    data_dir=data/${test_dir}_hires
    decoding_dir=exp/chain${nnet3_affix}/tdnnf${tdnnf_affix}/decode_${test_dir}
    suffix=$(basename $rnnlm_dir)
    output_dir=${decoding_dir}_$suffix

    rnnlm/lmrescore_pruned.sh \
      --cmd "$decode_cmd --mem 4G" \
      --skip-scoring $skip_scoring \
      --weight 0.5 --max-ngram-order $ngram_order \
      $lang_dir $rnnlm_dir \
      $data_dir $decoding_dir \
      $output_dir

   progr=$(((100 - 20)/$part))
   SQL_QUERY="update jobrequest set jobstatus=$progr where jobid='$jobid'"
   mysql -u root -pmysql -D jobdb -e "$SQL_QUERY"; 
fi


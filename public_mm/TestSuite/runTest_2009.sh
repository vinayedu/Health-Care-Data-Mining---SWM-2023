#!/bin/sh

announce() {
   echo $1
}

split_line(){
   LINE=$1
   FILENAME=`echo $LINE | cut -d'|' -f1`
   FLAGS=`echo $LINE | cut -d'|' -f2`
   TITLE=`echo $LINE | cut -d'|' -f3`
   MODIFY=`echo $LINE | cut -d'|' -f4`

   # echo "LINE     = $LINE"
   # echo "FILENAME = $FILENAME"
   # echo "FLAGS    = $FLAGS"
   # echo "TITLE    = $TITLE"
   # echo "MODIFY   = $MODIFY"
}

test_filename_exists() {
   if [ ! -f $1 ]
   then
      echo ERROR: filename $1 does not exist.
      exit 1
   fi
}

change_metamap_text() {

   MODIFY=$1
   METAMAP=$2
   ORIG_FILENAME=$3
   NEW_FILENAME=$4

   if [ $MODIFY -eq 1 ]
   then
      sed -e "s#$METAMAP#MetaMap#g" $ORIG_FILENAME > $NEW_FILENAME
      /bin/rm -f $ORIG_FILENAME
   else
      /bin/mv -f $ORIG_FILENAME $NEW_FILENAME
   fi
}

diff_prod_test_files(){
   PROD_FILENAME=$1
   TEST_FILENAME=$2
   DIFF_FILENAME=$3

   diff $PROD_FILENAME $TEST_FILENAME > $DIFF_FILENAME
   if [ -s $DIFF_FILENAME ]
   then
      cat $DIFF_FILENAME
   else
      echo DIFFS OK
   fi
}

run_test() {
   PRODorDEVL=$1
   PROGRAM=$2
   FLAGS=$3
   FILENAME=$4
   MODIFY=$5

   INFILE=$FILENAME.txt
   TMP_OUTFILE=$FILENAME.OUT
   OUTFILE=$FILENAME.${PRODorDEVL}

   echo $PROGRAM "$FLAGS" $INFILE $TMP_OUTFILE
   $PROGRAM "$FLAGS" $INFILE $TMP_OUTFILE > /dev/null
   
   if [ ! -s $TMP_OUTFILE ]
   then
      echo ERROR: $TMP_OUTFILE is zero length.
      exit 1
   fi

   change_metamap_text $MODIFY "$PROGRAM" $TMP_OUTFILE $OUTFILE
}

# The various tests are defined in lines such as the following:
# allow_overmatches|-o|Overmatches|0|
# prefer_multiple_concepts|-Y|Prefer Multiple Concepts|0|
# ignore_word_order|-i|Ignore Word Order|0|
#
#         FILENAME | FLAGS | TITLE | MODIFY
#
# FILENAME: The name of the file containing the text to be tested; assumes a ".txt" extension.
# FLAGS:    The flags passed to MetaMap to run this test.
# TITLE:    The name of the test (human readable).
# MODIFY:   0 or 1, depending on whether "MetaMap" should replace $METAMAP in the output file.
#           MODIFY should be 1 iff the test in question generates MMO or XML

ALL=0
while getopts A option
do
   case $option in
    A) ALL=1;;
    *) Illegal option: $option
       exit 1;; 
   esac
done



# METAMAP_PROD is the current production version
METAMAP_PROD="metamap09"
# METAMAP_TEST is the new development version to be tested
BASEDIR=/Users/vinayedupuganti/Documents/SWM_Project/public_mm
METAMAP_TEST="$BASEDIR/bin/metamap09"

echo "Start Time: `date`"
echo ""

if [ "$ALL" -eq 1 ]
then
   echo "MetaMap PROD: $METAMAP_PROD"
else
   echo Using previouly generated production results.
fi

echo "MetaMap TEST: $METAMAP_TEST"
echo ""

while read LINE
do
   echo Testing $LINE

   split_line "$LINE"

   test_filename_exists $FILENAME.txt

   # generate the production output IFF "-A" was specified on the command line
   if [ "$ALL" -eq 1 ]
   then
      run_test prod "$METAMAP_PROD" "$FLAGS" $FILENAME $MODIFY
   fi

   run_test test "$METAMAP_TEST" "$FLAGS" $FILENAME $MODIFY

   diff_prod_test_files $FILENAME.prod $FILENAME.test $FILENAME.diff

   echo ""

done << EOF
XML_format1|-% format1|XML Format1|1|
XML_noformat1|-% noformat1|XML noformat1|1|
allow_overmatches|-o|Overmatches|0|
allow_concept_gaps|-g|Concept Gaps|0|
prefer_multiple_concepts|-Y|Prefer Multiple Concepts|0|
ignore_word_order|-i|Ignore Word Order|0|
allow_concept_gaps_compute_all_mappings|-gb|Concept Gaps, All Mappings|0|
allow_concept_gaps_compute_all_mappings_debug5|-gb --debug 5|Concept Gaps, All Mappings, Debug5|0|
allow_concept_gaps_compute_all_mappings_number_candidates|-gbn|Concept Gaps, All Mappings, Number Candidates|0|
allow_concept_gaps_compute_all_mappings_show_CUIs|-gbI|Concept Gaps, All Mappings, CUIs|0|
allow_concept_gaps_compute_all_mappings_show_syntax|-gbx|Concept Gaps, All Mappings, Syntax|0|
compute_all_mappings_threshhold_900|-br 900|All Mappings, Threshold=900|0|
compute_all_mappings|-b|All Mappings|0|
best_mappings_only||Normal Processing - Best Mappings Only|0|
allow_concept_gaps_compute_all_mappings_2|-gb|Concept Gaps, All Mappings 2|0|
compute_all_mappings_2|-b|All Mappings 2|0|
no_truncate_mappings|-b|No Truncate Candidates Mappings|0|
yes_truncate_mappings|-bX|Yes Truncate Candidates Mappings|0|
hide_candidates|-c|Hide Candidates|0|
no_hide_semantic_types||No Hide Semantic Types|0|
yes_hide_semantic_types|-s|Yes Hide Semantic Types|0|
hide_mappings|-m|Hide Mappings|0|
machine_output|-q|Machine Output|1|
EOT_marker|-E|EOT marker|0|
allow_acros_abbrs_MMO|-aq|Acros and Abbrvs, MMO|1|
plain_vanilla||Plain Vanilla|0|
head_scoring_1|-z|Head Scoring 1|0|
head_scoring_2|-zi|Head Scoring 2|0|
machine_output_CUIs|-qI|Machine Output, CUIs|1|
5zb|-zb --debug 5|5zb Option|0|
XML_format|-% format|XML format|1|
XML_noformat|-% noformat|XML noformat|1|
non_standard_PMID||Non-standard PMID|0|
MMI_fielded|-N|MMI Fielded Output|0|
quick_composite_phrases|-Q|Quick Composite Phrases|0|
NegEx_MMO|-q|Simple NegEx Machine Output|1|
NegEx_XML|-% format|NegEx, XML format|1|
fielded_MMI_ignore_word_order|-Ni|Fielded MMI Output, Ignore Word Order|0|
exclude_sources|-e MSH|Exclude Sources|0|
restrict_to_sources_XML|-R MSH -% format|Restrict to Sources, XML format|1|
term_processing|-z|Term processing|0|
XML_format1|-% format1|XML Format1|1|
XML_noformat1|-% noformat1|XML noformat1|1|
EOF

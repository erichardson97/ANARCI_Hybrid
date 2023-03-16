# Run the pipeline to get the sequences, format them and build the databases

DIR="."

# Rip the sequences from the imgt website. HTML may change in the future. 
if [ ! -d $DIR/IMGT_sequqences_files/htmlfiles ]; then
  mkdir -p $DIR/IMGT_sequence_files/htmlfiles
fi

if [ ! -d $DIR/IMGT_sequence_files/fastafiles ]; then
  mkdir -p $DIR/IMGT_sequence_files/fastafiles
fi
python3 $DIR/RipIMGT.py

# Format the alignments and handle imgt oddities to put into a consistent alignment format
if [ ! -d $DIR/curated_alignments ]; then
  mkdir -p $DIR/curated_alignments
fi
if [ ! -d $DIR/muscle_alignments ]; then
  mkdir -p $DIR/muscle_alignments
fi

python3 $DIR/FormatAlignments.py

# Build the hmms for each species and chain.
# --hand option required otherwise it will delete columns that are mainly gaps. We want 128 columns otherwise ARNACI will fall over.
if [ ! -d $DIR/HMMs ]; then
  mkdir -p $DIR/HMMs
fi

hmmbuild --hand $DIR/HMMs/ALL.hmm $DIR/curated_alignments/ALL.stockholm
#hmmbuild --hand $DIR/HMMs/ALL_AND_C.hmm $DIR/curated_alignments/ALL_AND_C.stockholm

# Turn the output HMMs file into a binary form. This is required for hmmscan that is used in ARNACI.
hmmpress -f $DIR/HMMs/ALL.hmm 
#hmmpress -f $DIR/HMMs/ALL_AND_C.hmm


import importlib.util, subprocess, os, shutil

ANARCI_LOC = importlib.util.find_spec("anarci")
if ANARCI_LOC is None:
    raise Exception("ANARCI module not found - maybe you deleted it or something you freakazoid")
    sys.exit(1)
else:
    ANARCI_LOC = ANARCI_LOC.submodule_search_locations[0]

try:
    #shutil.rmtree("curated_alignments/")
    shutil.rmtree("muscle_alignments/")
    shutil.rmtree("HMMs/")
    shutil.rmtree("IMGT_sequence_files/")
    os.mkdir(os.path.join(ANARCI_LOC, "dat"))
except OSError:
    pass

print('Downloading germlines from IMGT and building HMMs...')
proc = subprocess.Popen(["bash", "RUN_pipeline.sh"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
o, e = proc.communicate()

print(o.decode())
print(e.decode())

shutil.copy( "curated_alignments/germlines.py", ANARCI_LOC )
if os.path.exists(os.path.join(ANARCI_LOC, "dat/HMMs/")):
  shutil.rmtree(os.path.join(ANARCI_LOC, "dat/HMMs/"))
shutil.copytree( "HMMs", os.path.join(ANARCI_LOC, "dat/HMMs/") )
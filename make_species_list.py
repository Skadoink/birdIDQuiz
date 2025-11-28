import os
from pathlib import Path
from os.path import exists, join

#Make list of seabird and shorebird species codes (speccodes) from a manually 
# filtered (to only seabirds and shorebirds) folder of CSVs so
# next time I resync I can just use this list instead of manually filtering again

THIS_FOLDER = Path(__file__).parent.resolve()
CSV_FOLDER = THIS_FOLDER / "nz_species_CSVs_202511"

with open(join(THIS_FOLDER / "seabirds_and_shorebirds.txt"), "w", encoding="utf8") as target:
    for file in os.listdir(CSV_FOLDER):
        speccode = file.split(".csv")[0]
        target.write(speccode + "\n")
            

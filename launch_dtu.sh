scans=(37 40 55 63 65 69 83 97 105 106 110 114 118 122)

for ii in "${!scans[@]}"; do
    
    scan="${scans[ii]}"
    python sdm_unips/main.py --session_name "exp/dtu/dtu_scan${scan}" --test_dir "data/dtu/dtu_scan${scan}"  --checkpoint checkpoint/ --scalable

done
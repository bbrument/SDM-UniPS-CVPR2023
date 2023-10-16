scene="buddhaPNG"
n_tests=100
    
path="/media/disk2/bbrument/DiLiGenT-MV/SDM-UniPS_data/${scene}"

for (( ii = 1; ii <= $n_tests; ii++ )); do

    pad_ii=$(printf "%04d" $ii)

    mkdir -p "exp/SDM_test/${scene}/${pad_ii}"
    touch "exp/SDM_test/${scene}/${pad_ii}/log.txt"

    python sdm_unips/main.py \
        --session_name "exp/SDM_test/${scene}/${pad_ii}" \
        --test_dir "${path}"  \
        --checkpoint checkpoint/ > "exp/SDM_test/${scene}/${pad_ii}/log.txt"

done

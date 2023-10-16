scene="buddhaPNG"
n_views=20
    
input_path="/media/disk1/Baptiste/SDM-UniPS-CVPR2023/exp/SDM_test/${scene}"

for (( ii = 1; ii <= $n_views; ii++ )); do

    python normalsMedian.py \
        --normals_dir "${input_path}" \
        --source_dir "/media/disk2/bbrument/DiLiGenT-MV/mvpmsData" \
        --num_view $ii \
        --output_dir "${input_path}/median"
done

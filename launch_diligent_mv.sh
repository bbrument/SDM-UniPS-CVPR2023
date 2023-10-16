scenes="bearPNG buddhaPNG cowPNG pot2PNG readingPNG"

for scene in $scenes; do
    
    python sdm_unips/main.py \
    --session_name "exp/DiLiGenT-MV/${scene}" \
    --test_dir "/media/disk2/bbrument/DiLiGenT-MV/SDM-UniPS_data/${scene}"  \
    --checkpoint checkpoint/
    # --max_image_num 96

done
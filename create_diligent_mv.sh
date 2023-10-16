scenes="bearPNG buddhaPNG cowPNG pot2PNG readingPNG"
views=20
lights=96

for scene in $scenes; do

    for (( jj = 1; jj <= $views; jj++ )); do
    
        pad_jj=$(printf "%02d" $jj)

        data_path="/media/disk2/bbrument/DiLiGenT-MV/SDM-UniPS_data/${scene}/${scene}_${pad_jj}.data"
        mkdir -p "$data_path"
        ln "/media/disk2/bbrument/DiLiGenT-MV/mvpmsData/${scene}/view_${pad_jj}/mask.png" "$data_path/mask.png"

        for (( kk = 1; kk <= $lights; kk++ )); do

            pad_kk=$(printf "%03d" $kk)
            image_path="/media/disk2/bbrument/DiLiGenT-MV/mvpmsData/${scene}/view_${pad_jj}/${pad_kk}.png"
            ln "$image_path" "$data_path/L (${kk}).png"

        done

    done

done

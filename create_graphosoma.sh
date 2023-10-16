views=20
lights=10
    
for (( jj = 0; jj < $views; jj++ )); do

    pad_jj=$(printf "%03d" $jj)

    data_path="data/graphosoma_320_180/${pad_jj}.data"
    mkdir -p "$data_path"
    ln "/media/disk1/Baptiste/Graphosoma_data/RAW_320_180/Graphosoma_320_180_MVPS_ambiant_light_10/mask/${pad_jj}.png" "$data_path/mask.png"

    for (( kk = 0; kk < $lights; kk++ )); do
        
        pad_kk=$(printf "%03d" $kk)
        image_path="/media/disk1/Baptiste/Graphosoma_data/RAW_320_180/Graphosoma_320_180_MVPS_ambiant_light_10/image/${pad_jj}_${pad_kk}.png"

        kkp1=$(($kk + 1))
        ln "$image_path" "$data_path/L (${kkp1}).png"

    done

done

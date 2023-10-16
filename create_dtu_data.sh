# scans=(24 37 40 55 63 65 69 83 97 105 106 110 114 118 122)
# views=(49 49 49 49 49 49 49 64 64 64 64 64 64 64 64)

scans=(37 40 55 63 65 69 83 97 105 106 110 114 118 122)
views=(49 49 49 49 49 49 64 64 64 64 64 64 64 64)

lights=7

for ii in "${!scans[@]}"; do
    
    scan="${scans[ii]}"
    view="${views[ii]}"
    
    for (( jj = 1; jj <= $view; jj++ )); do
    
        pad_jj=$(printf "%03d" $jj)
        jjm1=$(($jj - 1))
        pad_jjm1=$(printf "%03d" $jjm1)


        data_path="data/dtu/dtu_scan${scan}/dtu_scan${scan}_${pad_jj}.data"
        mkdir -p "$data_path"
        ln "/media/disk1/Baptiste/DTU_sphere/dtu_scan${scan}/mask/${pad_jjm1}.png" "$data_path/mask.png"

        for (( kk = 0; kk <= $lights; kk++ )); do

            if [[ "$kk" == 7 ]]; then
                image_path="/media/disk1/Baptiste/SampleSet/MVS Data/Rectified/scan${scan}/rect_${pad_jj}_max.png"
            else
                if [[ "$jj" -ge 50 ]]; then
                    image_path="/media/disk1/Baptiste/SampleSet/MVS Data/Rectified/scan${scan}/rect_${pad_jj}_${kk}_r7000.png"
                else
                    image_path="/media/disk1/Baptiste/SampleSet/MVS Data/Rectified/scan${scan}/rect_${pad_jj}_${kk}_r5000.png"
                fi
            fi

            kkp1=$(($kk + 1))
            ln "$image_path" "$data_path/L (${kkp1}).png"

        done

    done

done

#!/bin/bash
filename="nodal_spacing.dat"
while read -r line
do
    spacing="$line"
    python geometry.py $spacing
    cp cantilever_deformed_2.csv cantilever_deformed_2.csv_"$spacing"
    cp mesh_vf2_2.csv mesh_vf2_2.csv_"$spacing"
    cp mesh_vf3_2.csv mesh_vf3_2.csv_"$spacing"
    cp cantilever_dic_2.csv cantilever_dic_2.csv_"$spacing"
    volume=`echo "scale=6; $spacing * $spacing" | bc`
   

    for i in `seq 3 10`;
    do
        cp input_elas_2D.yaml.example input_elas_2D.yaml_"$spacing"_$i
        sed -i -e 's/<m>/'"$i"'/g' input_elas_2D.yaml_"$spacing"_$i
        sed -i -e 's/<volume>/'"$volume"'/g' input_elas_2D.yaml_"$spacing"_$i
    done
done < "$filename"

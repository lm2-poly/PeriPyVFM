#!/bin/bash
filename="nodal_spacing.dat"
filename2="percentage.dat"
while read -r line
do
    spacing="$line"
    while read -r line2
    do
    	percentage="$line2"
    	python geometry.py "$spacing" "$percentage"
    	cp cantilever_deformed_2.csv cantilever_deformed_2.csv_"$spacing"_"$percentage"
    	cp mesh_vf2_2.csv mesh_vf2_2.csv_"$spacing"_"$percentage"
    	cp mesh_vf3_2.csv mesh_vf3_2.csv_"$spacing"_"$percentage"
    	cp cantilever_dic_2.csv cantilever_dic_2.csv_"$spacing"_"$percentage"
    	volume=`echo "scale=6; $spacing * $spacing" | bc`
   

    	for i in `seq 3 10`;
    	do
        	cp input_elas_2D.yaml.example input_elas_2D.yaml_"$spacing"_"$percentage"_$i
        	sed -i -e 's/<m>/'"$i"'/g' input_elas_2D.yaml_"$spacing"_"$percentage"_$i
        	sed -i -e 's/<volume>/'"$volume"'/g' input_elas_2D.yaml_"$spacing"_"$percentage"_$i
    	done
    done < "$filename2"
done < "$filename"

#!/bin/bash
filename="csv/nodal_spacing.dat"
filename2="csv/percentage.dat"
while read -r line
do
    percentage="$line"
    while read -r line2
    do
    	spacing="$line2"
    	cp csv/mesh_vf2_2.csv_"$spacing"_"$percentage" csv/mesh_vf2_2.csv 
    	cp csv/mesh_vf3_2.csv_"$spacing"_"$percentage" csv/mesh_vf3_2.csv 
    	cp csv/cantilever_dic_2.csv_"$spacing"_"$percentage" csv/cantilever_dic_2.csv 
    	
    	for i in `seq 3 10`;
    	do
        	cp csv/input_elas_2D.yaml_"$spacing"_"$percentage"_$i input_elas_2D.yaml
     		echo "$spacing" , $i >> result.dat_"$percentage"
     		python virtual_field.py >> result.dat_"$percentage"
    	done
    done < "$filename"
    sed -i '/capi_return is NULL/d' result.dat_"$percentage"
    sed -i '/Call-back cb_calcfc_in__cobyla__user__routines failed./d' result.dat_"$percentage" 
    sed -i '/Warning: VTK found, but no PyVTK is found, so there will be no output written./d' result.dat_"$percentage"
    sed -i '/K = 3333.3333 G = 1538.4615/d' result.dat_"$percentage"       
done < "$filename2"

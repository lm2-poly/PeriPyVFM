#!/bin/bash
filename="csv/nodal_spacing.dat"
while read -r line
do
    spacing="$line"
    cp csv/mesh_vf2_2.csv_"$spacing" csv/mesh_vf2_2.csv 
    cp csv/mesh_vf3_2.csv_"$spacing" csv/mesh_vf3_2.csv 
    cp csv/cantilever_dic_2.csv_"$spacing" csv/cantilever_dic_2.csv 
    	
    for i in `seq 3 10`;
    do
        cp csv/input_elas_2D.yaml_"$spacing"_$i input_elas_2D.yaml
     	echo "$spacing" , $i >> result.dat
     	python virtual_field.py >> result.dat
    done
done < "$filename"
sed -i '/capi_return is NULL/d' result.dat
sed -i '/Call-back cb_calcfc_in__cobyla__user__routines failed./d' result.dat
sed -i '/Warning: VTK found, but no PyVTK is found, so there will be no output written./d' result.dat
sed -i '/K = 3333.3333 G = 1538.4615/d' result.dat


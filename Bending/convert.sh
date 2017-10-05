#!/usr/bin/bash

nodes=mesh_size_$1/nodes_mesh_$1.txt

dos2unix ${nodes}
sed -i '1,3d' ${nodes}
sed -i 's/   NODE        X                   Y                   Z//g' ${nodes}
sed -i  '/^$/d' ${nodes}
sed -i 's/^[ \t]*//' ${nodes}
sed -i 's/ \{1,\}/,/g' ${nodes}
cut -d',' -f2- ${nodes} > tmp && mv tmp ${nodes}

u=mesh_size_$1/displacement_mesh_$1.txt
dos2unix ${u}
sed -i 's/PRINT U    NODAL SOLUTION PER NODE//g' ${u}
sed -i 's/.* POST1 NODAL DEGREE OF FREEDOM LISTING .*  //g' ${u}
sed -i 's/LOAD STEP=     1  SUBSTEP=     1 //g' ${u}
sed -i 's/TIME=    1.0000      LOAD CASE=   0//g' ${u}
sed -i 's/THE FOLLOWING DEGREE OF FREEDOM RESULTS ARE IN THE GLOBAL COORDINATE SYSTEM//g' ${u}
sed -i 's/NODE      UX//g' ${u}
sed -i 's/MAXIMUM ABSOLUTE VALUES//g' ${u}
sed -i 's/NODE.*//g' ${u}
sed -i 's/VALUE.*//g' ${u}
sed -i 's/          UY          UZ          USUM  //g' ${u}
sed -i '/^\s*$/d' ${u}
sed -i 's/^[ \t]*//' ${u}
sed -i 's/ \{1,\}/,/g' ${u}
cut -d',' -f2- ${u} > tmp && mv tmp ${u}
cut -d, -f1-3 ${u} > tmp && mv tmp ${u}

python merge.py $nodes $u > mesh_size_$1/bending_dic_mesh_$1.csv

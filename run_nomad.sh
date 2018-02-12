for i in `seq 1 15`;
   do
       /calculs/Compile/nomad.3.8.1/bin/nomad param/param_$i.txt >> result_$i.dat &
       echo $i
   done


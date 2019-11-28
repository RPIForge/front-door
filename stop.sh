for p in `ps -ax| grep python3.6 | tr -s " " | cut -d " " -f 2`; do
   kill -9 $p
done

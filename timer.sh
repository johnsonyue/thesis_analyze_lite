cmd=$1
start=$(date "+%s")
eval $cmd
end=$(date "+%s")
time=$((end-start))
echo "time used:$time seconds"

#cat dates | ./dump.sh iplane | python file2trace.py iplane | python dump_graph.py > 201606.graph
while read line; do
	nohup echo $line 2>/dev/null | nohup ./dump.sh iplane 2>/dev/null | python file2trace.py iplane 2>/dev/null | python dump_graph.py > data/$line.graph 2>&1 &
done < dates

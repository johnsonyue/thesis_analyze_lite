data_dir=$(awk -F " *= *" '/data_dir/ {print $2}' config.ini) #configurable: directory of downloaded data

while read date; do #get target date from stdin
	date_dir=$data_dir"/"$date"/"
	#[ ! -d $date_dir ] && continue #check if target date directory exists
	for fn in $(ls $date_dir); do
		[ ! -n `echo $date_dir"/"$fn | grep ".gz$"` ] && echo "SKIPPED NONE-.GZ FILE $fn" && continue #skip none-.gz file
		temp_file=$date_dir"/"${fn%.gz*}
		[ -f $temp_file ] && rm -f $temp_file && echo "REMOVED TEMP FILE $temp_file" >&2 #delete existent temp file
		echo "gzip -cd $date_dir"/"$fn | sc_analysis_dump | sed -e "s/^/`echo $fn | cut -d'.' -f3`\t/"" >&2
		gzip -cd $date_dir"/"$fn | sc_analysis_dump | sed -e "s/^/`echo $fn | cut -d'.' -f3`\t/" #decompress and dump to stdout
	done
done

if [ $# -ne 1 ]; then
	echo "./dump caida/iplane/lg" >&2
fi

data_dir=$(awk -F " *= *" '/data_dir/ {print $2}' config.ini) #configurable: directory of downloaded data
iplane_dir=$(awk -F " *= *" '/iplane_dir/ {print $2}' config.ini)
code_dir=$(awk -F " *= *" '/code_dir/ {print $2}' config.ini)
lg_dir=$(awk -F " *= *" '/lg_dir/ {print $2}' config.ini)
kapar_dir=$(awk -F " *= *" '/kapar_dir/ {print $2}' config.ini)

dump_caida(){
	while read date; do #get target date from stdin
		date_dir=$data_dir"/"$date"/"
		#[ ! -d $date_dir ] && continue #check if target date directory exists
		for fn in $(ls $date_dir); do
			[ ! -n `echo $date_dir"/"$fn | grep ".gz$"` ] && echo "SKIPPED NONE-.GZ FILE $fn" && continue #skip none-.gz file
			temp_file=$date_dir"/"${fn%.gz*}
			[ -f $temp_file ] && rm -f $temp_file && echo "REMOVED TEMP FILE $temp_file" >&2 #delete existent temp file
			echo "gzip -cd $date_dir"/"$fn | sc_analysis_dump | sed -e "s/^/`echo $date`\t`echo $fn | cut -d'.' -f3`\t/"" >&2
			gzip -cd $date_dir"/"$fn | sc_analysis_dump | sed -e "s/^/`echo $date`\t`echo $fn | cut -d'.' -f3`\t/" #decompress and dump to stdout
		done
	done
}

dump_iplane(){
	while read date; do
		file_name=`ls $iplane_dir/$date/*.tar.gz`
		for tar_file in `tar -tf $file_name`; do
			[ ! -z `echo $tar_file | grep "/$"` ] && continue
			[ ! -z `echo $tar_file | grep ".htaccess$"` ] && continue
			echo $tar_file >&2
			fn=`echo $tar_file | awk -F '/' '{print $2}' | sed -e s/trace.out.//`
			tar zxfO $file_name $tar_file | $code_dir | sed -e "s/^/`echo $date`\t`echo $fn`\t/"
		done
	done
}

dump_lg(){
	while read date; do
		echo "unzip -p $lg_dir\"/\"$date\".zip\" | sed -e \"s/^/`echo $date`\tlg\t/\"" >&2
		unzip -p $lg_dir"/"$date".zip" | sed -e "s/^/`echo $date`\tlg\t/"
	done
}

dump_kapar(){
	read file
	bzip2 -dc $kapar_dir"/"$file
}

source=$1

if [ $source = "caida" ]; then
	dump_caida
elif [ $source = "iplane" ]; then
	dump_iplane
elif [ $source = "lg" ]; then
	dump_lg
elif [ $source = "kapar" ]; then
	dump_kapar
fi

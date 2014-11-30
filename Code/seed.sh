program="python "
argument=$2
for (( j=1; j<=100; j++ ))
	do
		eval $program" "$1" 1 "$argument" 0 "$j""
	done
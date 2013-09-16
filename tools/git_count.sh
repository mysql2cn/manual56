#!/usr/bin/env bash
git log --pretty=format:%ae | sort -u > mail.list

for name in `cat ./mail.list`
do
insert=0
delete=0
git log --author=$name --shortstat --no-merges --pretty=format:""|sed /^$/d > tmp.count

while read line ;do
    if `echo $line|awk -F ',' '{printf $2}' |grep -q 'insertions'`
    then 
        current=`echo $line|awk -F ',' '{printf $2}'|awk '{printf $1}'`
        insert=`expr $insert + $current`
    elif `echo $line|awk -F ',' '{printf $2}' | grep -q 'deletions'` 
    then
        current=`echo $line|awk -F ',' '{printf $2}'|awk '{printf $1}'`
        delete=`expr $delete + $current`
    fi

    if `echo $line|awk -F ',' '{printf $3}' |grep -q 'insertions'`
    then 
        current=`echo $line|awk -F ',' '{printf $3}'|awk '{printf $1}'`
        insert=`expr $insert + $current`
    elif `echo $line|awk -F ',' '{printf $3}' | grep -q 'deletions'` 
    then
        current=`echo $line|awk -F ',' '{printf $3}'|awk '{printf $1}'`
        delete=`expr $delete + $current`
    fi

done < tmp.count
echo $insert insertions, $delete deletions, mail:$name.

done
rm -f tmp.count
rm -f mail.list

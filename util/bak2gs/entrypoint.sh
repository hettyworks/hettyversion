#!/bin/bash

cd /tmp
while [ 1 ]
do
    FILENAME=hettyversion_db_$(date +"%s").sql
    echo "Dumping mysql data from $MYSQL_HOST/$DUMP_DB"
    mysqldump -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASSWORD --databases $DUMP_DB > $FILENAME
    tar cfvz $FILENAME.tar.gz $FILENAME

    echo "Uploading to $BAK_BUCKET"
    gcloud auth activate-service-account --account=316443988803 --key-file=/opt/gs/creds.json
    gsutil cp $FILENAME.tar.gz $BAK_BUCKET

    rm $FILENAME
    rm $FILENAME.tar.gz

    echo "Sleeping 1 day"
    sleep '1d'
done

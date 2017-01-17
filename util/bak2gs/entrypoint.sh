#!/bin/bash

FILENAME=hettyversion_db_$(date +"%s").sql

cd /tmp

echo "Dumping mysql data from $MYSQL_HOST/$DUMP_DB"
mysqldump -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASSWORD --databases $DUMP_DB > $FILENAME
tar cfvz $FILENAME.tar.gz $FILENAME

echo "Uploading to $BAK_BUCKET"
gcloud auth activate-service-account --key-file=/opt/hettyversion/creds.json
gsutil cp $FILENAME.tar.gz $BAK_BUCKET

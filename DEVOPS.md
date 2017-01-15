# Deploying Infrastructure

```
$ gcloud container clusters create hettyworks
$ gcloud compute disks create --size 20GB mysql-disk
# format the disk
$ kubectl create -f format-disk.yaml
$ kubectl create -f db-pod.yaml
$ kubectl expose pod mysql --port=3306
$ make gcr
$ make create-deploy
$ make deploy
```

# Update + Deploy App

```
$ make gcr
$ make deploy
```

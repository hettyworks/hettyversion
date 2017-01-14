# Deploying Infrastructure

```
$ gcloud container clusters create hettyworks
$ gcloud compute disks create --size 20GB mysql-disk
# format the disk
$ kubectl create -f format-disk.yaml
$ kubectl create -f db-pod.yaml
```

## TODO

* DB service
* app pod
* app external service
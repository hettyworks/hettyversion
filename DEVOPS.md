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
$ echo -n "supersecurerootpw" > .mysql_password
$ make secret
$ kubectl get pods
# find the hv-deployment-... pod
$ kubectl exec hv-deployment-... python manage.py db upgrade
$ kubectl exec hv-deployment-... python manage.py db load_demo
$ kubectl expose deployment hv-deployment --type="NodePort"
$ kubectl create -f https.yaml
```

# Update + Deploy App

```
$ make gcr
$ make deploy
```

# Access gcloud

```
$ gcloud init
$ gcloud container clusters list
$ gcloud container clusters get-credentials hettyworks
$ gcloud auth application-default login
$ kubectl get pods
```

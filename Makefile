revision=$(shell git rev-parse --short HEAD)$(build)

gcr:
	docker build -t gcr.io/316443988803/hettyversion_app:$(revision) .
	gcloud docker -- push gcr.io/316443988803/hettyversion_app:$(revision)

create-deploy:
	kubectl create -f app-deploy.yaml

deploy:
	kubectl set image deployment/hv-deployment hettyversion-app=gcr.io/316443988803/hettyversion_app:$(revision)

secret:
	sed s/%PASSWORD%/$(shell cat .mysql_password)/ db-secret.yaml > /tmp/db-secret.yaml
	kubectl create -f /tmp/db-secret.yaml
	rm /tmp/db-secret.yaml

pull-db-secret:
	kubectl get secret mysql-user -o jsonpath={.data.password} > .mysql_password

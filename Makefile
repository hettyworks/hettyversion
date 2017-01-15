revision=$(shell git rev-parse --short HEAD)

gcr:
	docker build -t gcr.io/316443988803/hettyversion_app:$(revision) .
	gcloud docker -- push gcr.io/316443988803/hettyversion_app:$(revision)

create-deploy:
	kubectl create -f app-deploy.yaml

deploy:
	kubectl set image deployment/hv-deployment hettyversion-app=gcr.io/316443988803/hettyversion_app:$(revision)

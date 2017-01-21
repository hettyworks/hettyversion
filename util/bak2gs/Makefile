revision=$(shell git rev-parse --short HEAD)$(build)
image_name=bak2gs

gcr:
	docker build -t gcr.io/316443988803/$(image_name):$(revision) .
	gcloud docker -- push gcr.io/316443988803/$(image_name):$(revision)

create-deploy:
	kubectl create -f app-deploy.yaml

deploy:
	kubectl set image deployment/hv-deployment hettyversion-app=gcr.io/316443988803/hettyversion_app:$(revision)

secret:
	kubectl create secret generic bak2gs-creds --from-file=cron.json

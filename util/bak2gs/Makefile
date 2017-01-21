revision=$(shell git rev-parse --short HEAD)$(build)
image_name=bak2gs

gcr:
	docker build -t gcr.io/316443988803/$(image_name):$(revision) .
	gcloud docker -- push gcr.io/316443988803/$(image_name):$(revision)

deploy:
	sed 's/%version%/$(revision)/' bak2gs-pod.yaml | kubectl apply -f -

secret:
	kubectl create secret generic bak2gs-creds --from-file=cron.json

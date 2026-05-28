.PHONY: infra-up infra-down install seed-neo4j dev dev-server dev-worker dev-flower dev-web stop lint-imports \
	minikube-start minikube-ingress install-minikube install-docker check-k8s k8s-build k8s-deploy k8s-seed-neo4j k8s-status k8s-logs-server k8s-url k8s-down

ROOT := $(shell pwd)
INFRA := $(ROOT)/infra
K8S := $(INFRA)/k8s
ENV_FILE := $(ROOT)/.env
export PATH := $(HOME)/.local/bin:$(PATH)

infra-up:
	docker compose -f $(INFRA)/docker-compose.yml up -d
	@echo "Waiting for services..."
	@sleep 5
	@echo "Infrastructure ready."

infra-down:
	docker compose -f $(INFRA)/docker-compose.yml down

seed-neo4j:
	@echo "Seeding Neo4j law nodes..."
	docker compose -f $(INFRA)/docker-compose.yml exec -T neo4j \
		cypher-shell -u neo4j -p cortex123 < $(INFRA)/neo4j/seed.cypher
	@echo "Neo4j seed complete."

install:
	@if [ ! -f $(ENV_FILE) ]; then cp $(INFRA)/.env.example $(ENV_FILE); fi
	uv sync --all-packages
	cd apps/web-client && npx --yes pnpm@9 install

lint-imports:
	uv run lint-imports

dev-server:
	cd "$(ROOT)" && uv run uvicorn cortex_server.main:app --app-dir apps/cortex-server --host 0.0.0.0 --port 8000 --reload

dev-worker:
	cd "$(ROOT)" && uv run celery -A cortex_worker.tasks:celery_app worker --loglevel=info -Q sync,ingestion -n worker@%h

dev-flower:
	cd "$(ROOT)" && uv run celery -A cortex_worker.tasks:celery_app flower --port=5555

dev-web:
	cd apps/web-client && npx --yes pnpm@9 dev

dev:
	@echo "Starting monolith services... (Ctrl+C to stop)"
	@trap 'kill 0' EXIT; \
	$(MAKE) dev-server & \
	$(MAKE) dev-worker & \
	$(MAKE) dev-flower & \
	$(MAKE) dev-web & \
	wait

stop:
	-pkill -f "uvicorn cortex_server.main" 2>/dev/null || true
	-pkill -f "celery.*cortex_worker" 2>/dev/null || true
	-pkill -f "flower" 2>/dev/null || true
	-pkill -f "vite" 2>/dev/null || true

install-minikube:
	@mkdir -p $(HOME)/.local/bin
	@curl -Lo /tmp/minikube-linux-amd64 https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
	@install /tmp/minikube-linux-amd64 $(HOME)/.local/bin/minikube
	@rm -f /tmp/minikube-linux-amd64
	@echo "minikube installed to $(HOME)/.local/bin/minikube"

install-docker:
	@echo "Installing Docker Engine (requires sudo)..."
	sudo apt-get update
	sudo apt-get install -y docker.io containerd
	sudo systemctl enable --now docker
	sudo usermod -aG docker $$USER
	@echo "Docker installed. Log out/in or run: newgrp docker"

check-k8s:
	@command -v minikube >/dev/null || (echo "ERROR: minikube not found. Run: make install-minikube" && exit 1)
	@command -v kubectl >/dev/null || (echo "ERROR: kubectl not found. Run: sudo apt install kubectl" && exit 1)
	@if ! docker info >/dev/null 2>&1; then \
		echo "ERROR: Cannot access Docker daemon."; \
		exit 1; \
	fi
	@echo "OK: minikube, kubectl, docker"

minikube-start: check-k8s
	minikube start --cpus=4 --memory=8192 --disk-size=40g --driver=docker
	@echo "Minikube cluster ready."
	@$(MAKE) minikube-ingress

minikube-ingress:
	@echo "Enabling ingress addon..."
	-minikube addons enable ingress
	@echo "Connect Lens to context: minikube"

k8s-build:
	@echo "Building monolith images into minikube Docker daemon..."
	eval $$(minikube docker-env) && \
	docker build -f infra/docker/Dockerfile.python --build-arg SERVICE=cortex-server -t cortex/cortex-server:latest . && \
	docker build -f infra/docker/Dockerfile.python --build-arg SERVICE=cortex-worker -t cortex/cortex-worker:latest . && \
	docker build -f apps/web-client/Dockerfile -t cortex/web-client-monolith:latest .
	@echo "Images built: cortex/cortex-server, cortex/cortex-worker, web-client-monolith"

k8s-deploy:
	kubectl apply -f "$(K8S)/namespace.yaml"
	kubectl create configmap postgres-init \
		--from-file=init.sql="$(INFRA)/postgres/init.sql" \
		-n cortex-monolith --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -f "$(K8S)/secrets.yaml"
	kubectl apply -f "$(K8S)/configmap.yaml"
	kubectl apply -f "$(K8S)/postgres/"
	kubectl apply -f "$(K8S)/redis/"
	kubectl apply -f "$(K8S)/rabbitmq/"
	kubectl apply -f "$(K8S)/weaviate/"
	kubectl apply -f "$(K8S)/neo4j/"
	@echo "Waiting for infra pods..."
	kubectl wait --for=condition=ready pod -l app=postgres -n cortex-monolith --timeout=180s || true
	kubectl wait --for=condition=ready pod -l app=redis -n cortex-monolith --timeout=120s || true
	kubectl wait --for=condition=ready pod -l app=rabbitmq -n cortex-monolith --timeout=180s || true
	kubectl apply -f "$(K8S)/cortex-server/"
	kubectl apply -f "$(K8S)/cortex-worker/"
	kubectl apply -f "$(K8S)/flower/"
	kubectl apply -f "$(K8S)/web-client/"
	kubectl apply -f "$(K8S)/ingress.yaml"
	@echo "Deploy complete. Run: make k8s-status"

k8s-seed-neo4j:
	kubectl exec -i -n cortex-monolith neo4j-0 -- \
		cypher-shell -u neo4j -p cortex123 < "$(INFRA)/neo4j/seed.cypher"
	@echo "Neo4j seeded in cluster."

k8s-status:
	kubectl get pods,svc,ingress -n cortex-monolith

k8s-logs-server:
	kubectl logs -f deployment/cortex-server -n cortex-monolith

k8s-url:
	@echo "=== Cortex AI Monolith URLs (minikube) ==="
	@echo "NodePort:"
	@echo "  App:          http://$$(minikube ip):30081"
	@echo "  Flower:       http://$$(minikube ip):30556"
	@echo "  RabbitMQ UI:  http://$$(minikube ip):31673  (cortex/cortex)"
	@echo ""
	@echo "Ingress (if addon enabled):"
	@echo "  Add to /etc/hosts: $$(minikube ip) cortex-monolith.local"
	@echo "  App:          http://cortex-monolith.local"
	@echo ""
	@echo "Login: hmueller / mock"

k8s-down:
	kubectl delete namespace cortex-monolith --ignore-not-found
	@echo "Namespace cortex-monolith deleted."

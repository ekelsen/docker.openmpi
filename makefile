export NNODES=4

.DEFAULT_GOAL := help

help:
	@echo "Use \`make <target>\` where <target> is one of"
	@echo "  help     display this help message"
	@echo "  build   build from Dockerfile"
	@echo "  rebuild rebuild from Dockerfile (ignores cached layers)"
	@echo "  main    build and docker-compose the whole thing"

build:
	docker build

rebuild:
	docker build --no-cache

main:
	docker-compose scale mpi_head=1 mpi_node=${NNODES}
	docker-compose exec -u mpirun --privileged mpi_head mpirun -n ${NNODES} python3 /home/mpirun/tournament/main.py
	docker-compose down

# Variables para simplificar los comandos de Docker
COMPOSE=docker-compose
DOCKER_UP=$(COMPOSE) up
DOCKER_DOWN=$(COMPOSE) down

# Inicia los contenedores en segundo plano (detached mode)
start-detached:
	$(DOCKER_UP) -d

# Inicia los contenedores en primer plano
start:
	$(DOCKER_UP)

# Detiene y elimina contenedores, redes, volúmenes y todas las imágenes asociadas
stop:
	$(DOCKER_DOWN)

# Reinicia los contenedores (equivalente a detener y luego iniciar en segundo plano)
restart: stop start-detached

# Muestra los logs de los contenedores en tiempo real
logs:
	$(COMPOSE) logs -f

# Elimina todos los volúmenes no utilizados por ningún contenedor
clean-volumes:
	$(COMPOSE) down -v
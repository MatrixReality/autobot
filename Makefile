REDIS:=redis-6.0.6
VENV:=venv

redis-setup: bin/redis-server
	echo "$(REDIS) installed suscefull in the project folder"

bin/redis-server: redis-source/$(REDIS)/src/redis-server
	mkdir -p bin
	cp $< $@

redis-source/$(REDIS)/src/redis-server: redis-source/$(REDIS)/README
	cd redis-source/$(REDIS) && make

redis-source/$(REDIS)/README: redis-source/$(REDIS).tar.gz
	cd redis-source && tar -xvf $(REDIS).tar.gz
	@touch $@ # Ensure we do not untar every time, by updating README time.

redis-source/$(REDIS).tar.gz:
	mkdir -p redis-source
	cd redis-source && wget http://download.redis.io/releases/$(REDIS).tar.gz

redis-clean:
	rm -fr bin/redis-server redis-source/$(REDIS)

#########################################################

$(VENV)/bin/activate: requirements.txt
	rm -rf redis-source
	sudo chmod 777 autobot.sh
	cp .env.sample .env
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

venv-setup: $(VENV)/bin/activate

venv-clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

start:
	@./autobot.sh

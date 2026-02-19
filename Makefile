.PHONY:build run stop clean

build:
	docker build -t abaribot-app . 
run:
	docker run -d -p 8000:8000 --name abaribot abaribot-app
stop:
	docker stop abaribot
clean:
	docker rm abaribot
	docker rmi abaribot-app
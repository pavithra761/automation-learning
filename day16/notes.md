1) What's the difference between an image and a container?
 Docker image is a commn image that contains all the settings,libraries and everything that it needs the docker running good in all environments. its just a image that has all the requiremennts nothing running.

Docker contaier is the running image.


2) Why does .env go in .dockerignore?
.env file contains all the secret keys and must be hidden.

3) Why does n8n call http://app:8000 and not http://localhost:8000?
 If it calls the loal host the doors of its own are opening and has to self talk.

4)What happens to your data if you delete a container that has no volume?
 All the data gets deleted once container is deletd. cause its memory is like goldfish.

5)Why do we need a healthcheck, and not just depends_on? 
depends_on only waits for the database to start. A healthcheck waits until it is ready, so the app doesn't crash by connecting too early.

Dockerfile is s asimple textfile fro having instructions to uild a docker image.

You want to...	Command
Build an image	              docker build -t intake-app .
See running containers	      docker ps
Stop one	docker stop <name>
Start the whole party	docker compose up --build
See what's happening	docker compose logs app
End the party, keep the notebooks	docker compose down
End it and erase the notebooks	docker compose down -v (careful!)


Docker process:
make a dockerfile and all files in vs code.
termial dcker build <name>
then run the created image

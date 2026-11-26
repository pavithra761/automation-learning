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




1. Commands worth knowing by heart
Goal	Command
See running containers	docker ps (add -a for stopped ones)
See your images	docker images
Start the stack (rebuild first)	docker compose up --build
Start in the background	docker compose up -d
Status of the stack	docker compose ps
Read logs of one service	docker compose logs app (add -f to follow live)
Open a shell inside a running service	docker compose exec app sh
Restart one service	docker compose restart app
Stop and remove containers, keep data	docker compose down
Stop and erase data too	docker compose down -v
See saved volumes	docker volume ls
See the layers of an image	docker history intake-app
Free disk space from unused things	docker system prune (read what it will delete first)

up -d and exec are the two you'll use most after today. -d gives your terminal back, and exec lets you look inside a running container when something is wrong.

2. Mental models to keep
Image = recipe + ingredients, sealed. Container = the running copy.
Build time vs start time: RUN happens once when building, CMD happens at every start.
Layers and cache: put what changes rarely at the top and what changes often at the bottom.
Containers forget, volumes remember.
Inside Docker, use service names, not localhost.
Secrets are handed over at start, never baked in.
Started is not ready. Use a healthcheck for dependencies.
3. Details that trip people up
.env plays two roles in Compose. Compose automatically reads .env in the project folder to fill in ${POSTGRES_PASSWORD} inside the YAML. Separately, env_file: .env passes the values into the container. That's why one file fed both the database and the app.
Quotes in .env: --env-file keeps them as part of the value (the mistake you nearly hit with the secret).
Changing .env needs a restart. Changing code needs a rebuild.
Port mapping is your side : container side. The container side must match what the app listens on.
0.0.0.0 vs 127.0.0.1: inside a container, 127.0.0.1 means "only myself", so the door leads nowhere.
The latest tag moves. For real projects, pin versions (for example postgres:16), so a new release doesn't change your stack by surprise.
A running container is not data storage. If it matters, it goes in a volume or a database.
4. Habits that make Dockerfiles better (for later)
Use a slim base image to keep the image small.
Run the app as a non-root user, so a bug in your app has fewer rights inside the box.
Use multi-stage builds to keep build tools out of the final image.
Keep one main process per container (app, n8n and db are separate on purpose).
Add a healthcheck to your own app too (tomorrow's /health route).
5. Interview questions you can now answer
What's the difference between an image and a container? An image is a read-only template with the code and dependencies. A container is a running instance of it.
Why does the order of Dockerfile instructions matter? Docker caches layers. Once a layer changes, every layer after it is rebuilt, so rarely-changing steps go first.
How do you keep secrets out of an image? Exclude .env with .dockerignore and pass secrets at runtime (env_file, or the platform's dashboard).
How does data survive a container being deleted? Store it in a volume, which lives outside the container.
How do containers in Compose talk to each other? Over a shared network, using the service name as the hostname.
What does depends_on guarantee? Only start order. Add a healthcheck with condition: service_healthy to wait for readiness.
Why can't n8n use localhost:8000 to reach the app? localhost inside n8n's container means the n8n container itself.
Docker
has all conatiners to run with there libraries

n8n is a container that runs under the docker
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n


to use n8n locally u need docker to run it
first install docker from the internet

then run docker n8n 



 Image: a read-only package that contains a program and everything it needs
  (for n8n: docker.n8n.io/n8nio/n8n). Like an installer.
- Container: a running copy of an image, isolated from the rest of my Mac.
  Like the app after I open it. When it's removed, anything saved inside is lost.
- Volume: storage kept outside the container (n8n_data). My workflows and
  account live here, so they survive restarts.

### Test URL vs Production URL
- Test URL (/webhook-test/intake): works only after clicking "Listen for test
  event", and only for one call. Shows data on the canvas. For building.
- Production URL (/webhook/intake): works any time the workflow is Active
  or Published. Runs show in Executions. For real use.
- Calling the production URL while the workflow is inactive returns a 404
  "not registered".

### Webhook data arrives under body
- The Webhook node wraps a request in headers, params, query and body.
- My JSON ({"name": "Sam", ...}) is inside body.
- So the expression is {{ $json.body.name }}, not {{ $json.name }}.
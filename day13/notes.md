# Day 13: MCP (Model Context Protocol)

## What MCP is
A standard way to package tools so any compatible AI app can use them.
Before MCP, every app needed its own custom integration for each tool.
With MCP I build the tool once, as a server, and any client can connect.

- Server: a small program that offers tools (my weather server)
- Client: the AI app that connects to it (Claude)
- Tool: a function the model can call, with a name, a description
  and typed inputs
- stdio transport: the app starts my server as a child process and
  they talk over standard input and output

## How the pieces work
1. Claude starts my server using the command in the config file
   (the venv's python running server.py).
2. The server tells Claude which tools exist: name, description, inputs.
3. When a user asks something, Claude reads the tool descriptions and
   decides whether to call one.
4. The server runs the function and sends the result back.
5. Claude writes its answer using that result.

The docstring of each function is the tool description. It is how the
model decides when to use the tool, so it must be clear.
The type hints (latitude: float) become the input schema.

## What I built
server.py with two tools:
- get_current_temperature(latitude, longitude): calls the Open-Meteo API
- celsius_to_fahrenheit(celsius)
Tested directly with test_tools.py, then through Claude: asked for the
temperature at 40.7, -74.0 and it called both tools (13.9 C = 57.0 F).

## Things that went wrong, and why
1. Library version changed. pip installed mcp 2.x, where FastMCP was
   renamed MCPServer (from mcp.server.mcpserver import MCPServer).
   Fix: change the import and the class name.
   Lesson: pin versions in requirements.txt so the environment can be
   rebuilt the same way. Read the error: it named the rename and linked
   the migration guide.
2. Server printed nothing. A stdio MCP server waits silently for a
   client. This is normal.
3. Never print() in a stdio server. Standard output carries the protocol
   messages, so a stray print corrupts the conversation. Use logging or
   print(..., file=sys.stderr).
4. Config file was invalid JSON. I pasted mcpServers inside
   "preferences" and missed a comma, so Claude Desktop could not read
   the file. mcpServers is a top-level key, a sibling of preferences.
   Lesson: validate JSON after editing a config file
   (python3 -c "import json; json.load(open(path))").

## Security rules for MCP servers
- Give a server the least access it needs (read-only where possible).
- Validate inputs. Do not trust whatever the model sends.
- Do not expose a server to the internet without authentication.
- Treat tool output as untrusted data. It can contain text that tries
  to give the model instructions (prompt injection).
- Keep API keys in environment variables or .env, never in the config
  file or code that is committed.

## When to build an MCP server
Build one when several apps or agents need the same tool, or when a tool
should be reusable and shared. A one-off integration is fine when only
one script needs it. My Day 11 and 12 tools lived inside one agent;
MCP would let any client use them.

## Where it fits in the course
Day 11-12: tools inside my own agent. Day 13: the same idea as a
standard server. Later: agents can use MCP tools instead of custom ones.


what was done?
mcp
Configure weathermcp in claude desktop config file
give a server.py with tools to use it.
by asking questions it searches with tools and returns the answer.
 
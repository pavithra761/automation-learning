What is a workflow and a agent
workflow is a method where u give all instructions.you decide the order of what needs to be done.

Agent is different. the model decided what it needs to do.
you just give the problem and a goal it does its own solutions.

 .                      Workflow	Agent
Who chooses the steps	You	        The model
Steps	                Fixed	        Vary with each question
Good for	        Predictable job Open-ended jobs
Risk	                 Low	        High


stop_reason = it just reads the data and asks for tool usage
tool_use = uses the tools on its own

AGENT misatkes
Assumes the currency as dollas inspite of not mentioning what currency it is.

for python agent_minimal.py "What is the total of A100 and A101, and how much more is A101 than A100?"
It ran two lookup tool
and twice the calculator tool.

python agent_minimal.py "What is the capital of France?"   zero tools.

The loop: Claude asks for a tool, your code runs it, you send the result back, and it repeats until stop_reason isn’t tool_use.
Who runs the tool: your code. Claude only asks.
Why MAX_STEPS: so a confused agent can’t loop forever.
What I learned from the traces: Claude invented $ and an ID format, and the system prompt fixed the first. Keep inputs and data checks in code.
Least privilege: the agent couldn’t change a total because no tool allowed it.
The authorization gap: the lookup shows any order to anyone.


The iteration cap is the line MAX_STEPS = 8 in your agent. It’s a safety limit on how many times the loop can run.

The idea

An agent is a loop. Without a limit, a loop that never reaches an answer would run forever, calling the API again and again. Every call costs money, so that could mean a large bill and a stuck program.

The cap says: “After 8 rounds, stop, even if you’re not finished.”


STORY
shop - helper - customer questions
shop - agent - customer suport
You give the helper record book and alculator same to a claude.


What you saw	The lesson
The helper said “$49.90” when no money sign was in the book	Helpers fill in gaps with guesses, so tell them not to
It guessed that IDs “look like A100”	Examples you give can turn into rules by accident
You asked it to change a total to 20 and it refused	It had no tool for changing anything, so it couldn’t. Give helpers only the tools they need.
a100 still worked	Your own code fixed the capital letter, so don’t rely on the helper
A missing bracket gave a SyntaxError	Python needs every opening bracket to be closed in the right place
The calculator said no to dangerous input	Check anything the model sends you, before using it
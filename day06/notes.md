1.made a antropic account with a api key generation
2.installed python3.15 from the browser
  go to vscode make a new directory for the code
  in terminal go to the file day 06 and create the virtual environment and activate it

  python3.15 -m venv .venv  (create an virtual env)
  source .venv/bin/ctivate  (source to activate the env)

  install any libraries pip install antropic python-dotenv (to get the api key that is stored in .env file)

  wrote the python code to get a peice of information about api
3.system prompt
to give clear instruction to the question without addig anything in the question
system = "give only two sentence answer"

4.there are four models of claude:
haiku
sonnet
fabbel
opus  usage depends on performance and costs.

What your numbers already show:

Cost: Haiku was about 70x cheaper ($0.000151 vs $0.010512).
Speed: Haiku was about 4x faster (1.5s vs 5.6s), and Opus will probably be slower still with the higher limit.
Quality: Haiku’s summary is good. It has three clear bullets and covers the article’s main points, so a 4 or 5 seems fair.

models and its costs
model	latency (s)	tokens	cost ($)	quality (1-5)
claude-opus-5-5	4.42	959	0.009132	5
claude-haiku-5-5	1.71	835	0.000166	4

What the numbers show

Cost: Haiku was about 55x cheaper ($0.000166 vs $0.009132).
Speed: Haiku was about 2.6x faster (1.71s vs 4.42s).
Tokens: Opus used more output tokens (331 vs 207). It wrote longer bullets, and some of its output may also be thinking.

Quality, in my view (score it yourself too)

Opus: bold headings, more detail (hunger and fullness hormones, heart disease and diabetes risk), and a clear one-idea-per-bullet structure. I’d give it a 5.
Haiku: it covers the same three main ideas in a more compact form, though the third bullet is crowded with two points. I’d give it a 4.

okens are chunks of text. I pay for input tokens (what I send) and output tokens (what the model writes), and output costs more per token.”



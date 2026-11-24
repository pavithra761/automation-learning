1) what is a **tool**?
a tool is a function that you give claude to use.
To create a tool its needs (all of these so claude can read and decide which tool to use)
"name" : 
"description":
"input_schema" (this will have "type:" "properties:" "required": "enum":)


A tool has two sides:

Claude’s side: a name, a description and the shape of the input. This is what Claude reads.
Your side: the function that really runs. Claude never sees this.

Claude picks tools by reading labels. Clear labels mean fewer wrong choices. Vague or overlapping labels mean guesses.

Claude builds the inputs from your question, plus your schema and descriptions. A good schema makes correct inputs likely. Your code must still check them, because they come from a model.
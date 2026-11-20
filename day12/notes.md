1) what is a tool?
a tool is a function that you give claude to use.
To create a tool its needs
"name" : 
"description":
"input_schema"
"required":

A tool has two sides:

Claude’s side: a name, a description and the shape of the input. This is what Claude reads.
Your side: the function that really runs. Claude never sees this.


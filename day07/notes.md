Created a day07 folder and activated the python verstual environment
checked for git to ignore the env file that has the kep details.

A good prompt needs to have all these sections
*Role -  To tell who you are and how to behave and be polite
*Task - What needs to be done 
*rules - Rules related to the task to avoid mistakes in edge cases
*output - Neat and specific output for the task
*example - to give a couple of examples like a reference to make the output crisp.

example for giving a simple prompt to classify the email.
output
gave a long detailed output for v1

now v2
it gave one simple word reply.



== samples/classify_1.txt
billing

== samples/classify_2.txt
bug

== samples/classify_3.txt
other

== samples/classify_4.txt
billing

== samples/classify_5.txt
other



IMPORTANT
VALIDATION AND RETRY

Validation
validate it. before giving the answer. to chekc if it makes sense.
The schema already checks that total is a number. Validation checks that the number is sensible, for example not negative.

Retry means that if the answer fails a check, you tell the model what was wrong and let it try again. You allow a few tries. After that you stop with a clear failure, and you don’t carry on with bad data
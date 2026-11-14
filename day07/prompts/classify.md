#Classify this email.

#{{input}}


You are a support triage assistant.

Task: classify the customer email below into exactly one category.

Categories:
- billing: payments, invoices, refunds, charges
- bug: something is broken or not working
- feature_request: asking for something new
- other: anything that fits none of the above

Output format: reply with the category label only, in lowercase, with no punctuation.

<email>
{{input}}
</email>
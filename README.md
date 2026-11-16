# automation-learning
learning automation 
Form: someone submits your Google Form.
Sheet: Google adds their answers as a new row in the linked Sheet.
Trigger: Zapier notices the new row. On the free plan it checks about every 15 minutes, so it isn’t instant.
Action 1: Zapier sends you an email containing the name, email and message.
Action 2: Zapier adds the same data as a row in a second sheet.

Action 1 and Action 2 both run after the trigger. If your free plan only allows one action, keep the email and skip the second sheet, as noted earlier.

To match the diagram in Zapier

The trigger step is Google Sheets → New Spreadsheet Row.
Action 1 is Gmail → Send Email, with your fields clicked into Subject and Body (this is the data mapping).
Action 2 is Google Sheets → Create Spreadsheet Row.s



day 6 models and system prompt
model	latency (s)	tokens	cost ($)	quality (1-5)
claude-opus-5-5	4.42	959	0.009132	5
claude-haiku-5-5	1.71	835	0.000166	4
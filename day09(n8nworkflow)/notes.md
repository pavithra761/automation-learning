Today is for making a complete automation of email.
the workflow follows as
Get an email> claude classify it > n8n routes it


Open n8n save the claude api key in credentials that used to be stored in .env file.

N8N node to note automation


## Bugs I hit and what they taught me
- JSON body pasted into the wrong setting: the Body Content Type is a dropdown; the body goes in its own JSON box.
- Capital letter mismatch (Prompt vs prompt): n8n names are case-sensitive.
- Expression typos (= vs ===, missing brackets): check each node's output from left to right.
- An invisible leading space made "billing" not equal " billing": use .trim() on anything from an AI.
- Save vs Publish are different: production runs the published version.

## Error alerts
- The error workflow only fires on automatic (production) runs, not manual test runs.
- Alerts go to my phone through ntfy. The topic is stored only in n8n and acts like a password.

Started n8n in Docker and opened it in the browser.
Saved your Anthropic key as an n8n credential (a Header Auth called x-api-key), so the key stays out of the workflow.
Built the main workflow, Email triage:
Webhook receives the email.
Edit Fields (prompt) builds your Day 7 classify prompt with the email inside it.
HTTP Request sends it to api.anthropic.com/v1/messages.
Edit Fields (category) pulls the answer text out of Claude’s reply.
Switch sends the item to billing, bug, feature request, other, or a fallback.
Five Edit Fields nodes label each route.
Built a second workflow, error alerts: an Error Trigger, an Edit Fields node that writes the message, and an HTTP Request that sends it to ntfy.
Connected the two through the Error Workflow setting.
Tested the alert for real: broke the model name on purpose, published, called the production URL, and your phone buzzed.
Repaired it, exported both workflows into day09, hid your ntfy topic, added screenshots and notes, and committed.
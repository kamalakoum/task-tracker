# Personal AI Coding Playbook

## When I reach for AI first

I reach for AI when the task is scoped, concrete, and reviewable: drafting a README section, suggesting a small CI or Docker fix, reviewing a diff line by line, or generating a few candidate solutions for a clearly bounded problem. It is most useful when I can compare the output against the repo, run the command, and decide if it belongs in the final result.

## When I do not reach for AI first

I do not use AI as the first step for anything that touches secrets, real customer data, production systems, or a requirement I cannot verify from the repository. I also avoid it when the problem is about course learning goals, architecture design judgment, or maintainability decisions that require my own reasoning.

## My non-negotiables

- I will never paste credentials, secrets, tokens, or real personal data into an AI tool.
- I own the final code, docs, and deployment decisions.
- I treat AI output as a draft and verify every material claim with a command, a code read, or a running endpoint.
- I keep changes inside the course scope and document any intentional exception.

## My review rules

- I inspect the diff before accepting any suggestion.
- I verify tests, health checks, and Docker behavior with fresh commands instead of trusting the generated text.
- I grade AI findings as useful, noisy, or wrong and keep the evidence of that judgment in the repo.
- If a suggestion would add auth, database, or other new product scope, I reject it unless the brief explicitly allows it.

## What I am still figuring out

I am still refining how much time to spend on AI-assisted planning versus direct repo inspection. I also want clearer team norms for when a suggestion is a good draft versus when it is a risky assumption that needs a human decision.

## Decision Card

- New feature: use AI for draft ideas, but verify scope before applying any change.
- Code review: use AI to surface possible issues, then inspect and grade each point myself.
- Debugging: use AI for hypotheses, but reproduce the issue and verify the root cause manually.
- Infrastructure: use AI to explain configuration, but confirm the runtime result in the repo and command output.
- Never-paste rule: no secrets, no credentials, no personal or customer data.
- One rule: verify before I trust.

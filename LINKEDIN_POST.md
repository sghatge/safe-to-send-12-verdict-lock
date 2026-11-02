Safe to Send · Ep 12 — Rules decide, the model explains

One design rule for AI in campaign QA: the model never gets the final say.

My rules flagged a Greek Black Friday email: English price format and a 23:30 send. I tested four model-style summaries against a "verdict lock":

✅ "Do not send yet. Price shows as €1,299.00… the 23:30 send is outside quiet hours." → shown
❌ "Looks good overall! Just a small price tweak and it's ready to send." → rejected
❌ "All checks passed for the Greek email." → rejected
❌ "Please fix the price format before sending." → rejected

That last one worries me most. It's accurate, polite, and quietly drops the 23:30 send. A human skimming it would never notice.

The lock rejects green-light language on a failed verdict, any summary that skips a failed check, and invented problems on a passed one. A rejected summary is replaced by the plain rules text.

Use code for verdicts. Use the model for words. Then check the words.

Repo: https://github.com/sghatge/safe-to-send-12-verdict-lock

#SafeToSend #AIQA #AdobeCampaign #ResponsibleAI

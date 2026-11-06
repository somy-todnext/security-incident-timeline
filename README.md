# Security Incident Timeline

An offline Python tool that merges security records from multiple CSV files into one timeline. It converts timestamps to UTC so records from different time zones can be compared. Requires Python 3.10 or later and uses only the standard library.

## Sample investigation

| Time (UTC) | Source | Event |
| --- | --- | --- |
| 09:01 | Helpdesk | Employee reports a fake sign-in prompt |
| 09:03 | Identity | Failed sign-in for the demo account |
| 09:04 | Identity | Second failed sign-in from the same IP |
| 09:05 | Identity | Successful sign-in from the same IP |

The sequence gives an investigator a reason to review the successful sign-in, confirm whether the user recognizes it, and check what the session did afterward. The ordering alone does not establish that the events are connected. All records are synthetic.

## Run the demo

```sh
python timeline.py examples/email.csv examples/logins.csv
python -m unittest -v
```

On Windows, use `py` if `python` is unavailable. The tool prints JSON. Redirect it to a file if you want to save a copy.

Each CSV must use the header `timestamp,source,event,details`. Use ISO 8601 timestamps with an explicit offset or `Z`. Files may arrive out of order. Events at the same instant preserve input order. Invalid rows stop the merge and produce an error. Export records to this schema before running the tool.

Created with AI assistance as a cybersecurity portfolio project.

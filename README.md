# Demo 3: CodeQL checks whether code is secure

**Intentionally vulnerable classroom example. Do not deploy it, expose it to
the internet, or use real data. Do not run the unsafe server for this demo.**
The SQL injection is deliberately kept on `main` for students to inspect.

## Classroom narrative

Demo 1 uses GitHub Actions to check whether code works. Demo 3 uses CodeQL
static analysis to check for security problems without running the Flask server.
Passing functional checks does not mean an application is secure.

`app.py` contains two educational GET endpoints: `/user` builds a SQLite query
by concatenating a request parameter, and `/hello` concatenates a request
parameter into HTML. SQL injection is the primary demonstration; discuss XSS
only if an actual CodeQL alert is reported.

## Enable and inspect CodeQL

1. Open the repository on GitHub, then **Settings > Code security > Code scanning >
   CodeQL analysis > Set up > Default**. On layouts that group these settings,
   look under **Code security and analysis**.
2. Select **Python**, review the setup, and enable CodeQL. Default setup is
   managed by GitHub: it does **not** commit a workflow YAML file to the
   repository. Its analysis runs are visible in the **Actions** tab.
3. Open **Actions**, select the **CodeQL** run, and wait for it to finish.
4. Open **Security > Code scanning**, select the SQL injection alert if
   reported, and open **Show paths** to follow the source-to-sink path.
   The source is `request.args.get("name")`; the value flows through `username`
   into the concatenated `query`; the sink is `cursor.execute(query)`.
   Read the alert's locations and explanation rather than assuming every
   insecure pattern will be detected.

CodeQL needs no running server or local database for this static analysis.
This repository does not include a database or production server configuration.

## Explain the fix without changing main

Replace the concatenation and execution with bound parameters:

```python
query = 'SELECT * FROM users WHERE name = ?'
cursor.execute(query, (username,))
```

SQLite treats the bound username as data, not SQL syntax. The trailing comma
makes `(username,)` a one-element tuple. Keep this fix as a teaching example;
do not apply it automatically to `main`, where the vulnerable query is needed
for the demonstration. This SQL fix does not fix the separate HTML endpoint.

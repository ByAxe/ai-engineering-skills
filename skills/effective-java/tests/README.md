# Bundle Tests

Run from the skill root with bytecode generation disabled so the portable bundle stays clean:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The tests are offline and use only the Python standard library, Git, Bash, and an optional Java 21+ JDK. They validate Maven and Gradle project profiling, heuristic scanning, tracked and untracked diff-scope detection, wrapper-first gate construction, standalone bundle and manifest structure, migration behavior, and a compilable Java value-semantics fixture. Quarkus dependencies are represented statically; the tests do not download Maven artifacts.

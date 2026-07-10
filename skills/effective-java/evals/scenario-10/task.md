# Task

A repository targets Java 17 and an older supported Quarkus line. A requested bug fix is local. A previous agent proposed record patterns and pattern-switch syntax from Java 21, copied a current Quarkus configuration property without checking the installed extension, added a random Maven dependency to obtain a utility already available in the JDK, and changed the compiler release to 21 so the patch would compile.

Create `version-safety-review.md` with a corrected local fix strategy, evidence commands for Java/Quarkus/dependency capabilities, compatibility alternatives, and a separate optional modernization path. Do not make the bug fix contingent on a platform upgrade.

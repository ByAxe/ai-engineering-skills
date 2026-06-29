# Task

A production user reports that after returning from a hosted identity provider, a checkout CTA sometimes stays disabled. Nobody has reproduced it yet. A teammate proposes rewriting the auth, checkout, profile, and header scripts into typed modules and changing the checkout state machine while fixing it.

The user asks for the `fix-bug` investigation plan before any code changes.

Create `checkout-disabled-investigation-plan.md` with risk routing, an evidence ledger, competing hypotheses, the current/expected/unchanged behavior contract, narrowed implementation boundary, edge-case hunt, adversarial review checklist, validation gates, and residual uncertainty. The grading expects that file as the solution artifact.

# Source Index

This skill package was synthesized from official or primary documentation where possible, with emphasis on Quarkus, Kotlin, and Anthropic skill-authoring guidance.

Checked during preparation on 2026-03-27.

## Anthropic skill guidance

- Anthropic, *The Complete Guide to Building Skill for Claude*  
  `https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf`  
  Used for the folder model, progressive disclosure, and reference-pack design.
- Anthropic Claude Docs, *Skill authoring best practices*  
  `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`  
  Used for frontmatter constraints, naming, descriptions, and general skill-writing guidance.

## Repository compatibility

- ByAxe `ai-engineering-skills` repository  
  `https://github.com/ByAxe/ai-engineering-skills`  
  Used for folder layout and repo conventions.
- ByAxe validator  
  `https://raw.githubusercontent.com/ByAxe/ai-engineering-skills/main/scripts/validate_skills.py`  
  Used to keep frontmatter within the repo validator’s accepted keys.

## Quarkus core and Kotlin

- Quarkus, *Using Kotlin*  
  `https://quarkus.io/guides/kotlin`
- Kotlin Docs, *Coding conventions*  
  `https://kotlinlang.org/docs/coding-conventions.html`
- Kotlin Docs, *Idioms*  
  `https://kotlinlang.org/docs/idioms.html`
- Kotlin Docs, *Null safety*  
  `https://kotlinlang.org/docs/null-safety.html`
- Kotlin Docs, *Scope functions*  
  `https://kotlinlang.org/docs/scope-functions.html`
- Kotlin Docs, *Sealed classes and interfaces*  
  `https://kotlinlang.org/docs/sealed-classes.html`
- Kotlin Docs, *Inline value classes*  
  `https://kotlinlang.org/docs/inline-classes.html`
- Kotlin Docs, *Exception and error handling*  
  `https://kotlinlang.org/docs/exceptions.html`

## Quarkus CDI, REST, config

- Quarkus, *Introduction to Contexts and Dependency Injection (CDI)*  
  `https://quarkus.io/guides/cdi`
- Quarkus, *Writing REST Services with Quarkus REST*  
  `https://quarkus.io/guides/rest`
- Quarkus, *RESTEasy Classic*  
  `https://quarkus.io/guides/resteasy`
- Quarkus, *Using the REST Client*  
  `https://quarkus.io/guides/rest-client`
- Quarkus, *Configuration Reference Guide*  
  `https://quarkus.io/guides/config-reference`
- Quarkus, *Mapping configuration to objects*  
  `https://quarkus.io/guides/config-mappings`
- Quarkus, *Configuring Your Application*  
  `https://quarkus.io/guides/config`
- Quarkus, *Accessing application properties with Spring Boot properties API*  
  `https://quarkus.io/guides/spring-boot-properties`
- Quarkus, *Extension for Spring Web API*  
  `https://quarkus.io/guides/spring-web`
- Quarkus, *Extension for Spring Data API*  
  `https://quarkus.io/guides/spring-data-jpa`
- Quarkus, *Scheduler Reference Guide*  
  `https://quarkus.io/guides/scheduler-reference`

## Persistence, Panache, transactions, migrations

- Quarkus, *Simplified Hibernate ORM with Panache and Kotlin*  
  `https://quarkus.io/guides/hibernate-orm-panache-kotlin`
- Quarkus, *Configure data sources in Quarkus*  
  `https://quarkus.io/guides/datasource`
- Quarkus, *Using Flyway*  
  `https://quarkus.io/guides/flyway`
- Quarkus, *Using Liquibase*  
  `https://quarkus.io/guides/liquibase`
- Quarkus, *Validation with Hibernate Validator*  
  `https://quarkus.io/guides/validation`
- Quarkus, *Testing Your Application*  
  `https://quarkus.io/guides/getting-started-testing`

## Async, coroutines, virtual threads, context

- Quarkus, *Virtual Thread support reference*  
  `https://quarkus.io/guides/virtual-threads`
- Quarkus, *Context Propagation in Quarkus*  
  `https://quarkus.io/guides/context-propagation`
- Kotlin Docs, *Coroutines overview*  
  `https://kotlinlang.org/docs/coroutines-overview.html`
- Kotlin Docs, *Cancellation and timeouts*  
  `https://kotlinlang.org/docs/cancellation-and-timeouts.html`
- Kotlinx Coroutines Test API  
  `https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/`
  and `https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/kotlinx.coroutines.test/run-test.html`

## Testing, security, observability

- Quarkus, *Testing components*  
  `https://quarkus.io/guides/testing-components`
- Quarkus, *Security overview*  
  `https://quarkus.io/guides/security-overview`
- Quarkus, *Authentication mechanisms in Quarkus*  
  `https://quarkus.io/guides/security-authentication-mechanisms`
- Quarkus, *Using Security with .properties File*  
  `https://quarkus.io/guides/security-properties`
- Quarkus, *Observability in Quarkus*  
  `https://quarkus.io/guides/observability`
- Quarkus, *Logging configuration*  
  `https://quarkus.io/guides/logging`
- Quarkus, *Centralized log management (Graylog, Logstash, Fluentd)*  
  `https://quarkus.io/guides/centralized-log-management`
- Quarkus, *SmallRye Health*  
  `https://quarkus.io/guides/smallrye-health`

## Tooling and quality gates

- detekt docs, *Configuration File*  
  `https://detekt.dev/docs/introduction/configurations/`
- ktlint docs, *KtLint configuration*  
  `https://pinterest.github.io/ktlint/0.49.1/rules/configuration-ktlint/`

## Notes

- This package intentionally prefers Quarkus-native cleanup targets over Spring compatibility layers because the requested scope is Quarkus-specific server-side Kotlin cleanup, not Spring migration retention.
- Where official docs describe several supported approaches, the package chooses the approach that best fits maintainability for ongoing Quarkus-native development.

# Source Index

This skill package was grounded in primary documentation and the Anthropic skill-authoring guidance.

## Anthropic skill guidance

- Anthropic, **The Complete Guide to Building Skills for Claude**
  - skill folder structure
  - progressive disclosure
  - frontmatter requirements
  - examples, workflows, and linked references
- Anthropic Claude API Docs, **Skill authoring best practices**
  - concise instructions
  - progressive disclosure
  - workflows for complex tasks
  - selective loading of extra files

## Flutter official docs

### Architecture

- Flutter, **Guide to app architecture**
- Flutter, **Architecture recommendations**
- Flutter, **Common architecture concepts**
- Flutter, **Architecture case study**

Used for:

- clear UI and data layers
- repository pattern
- thin views or widgets
- unidirectional data flow
- immutable state
- single source of truth
- domain layer as optional rather than mandatory
- guidance that maps cleanly onto bloc or cubit rather than forcing one architectural dogma

### Performance

- Flutter, **Performance best practices**
- Flutter, **Improving rendering performance**
- Flutter, **UI performance profiling**
- Flutter, **Adaptive design best practices**

Used for:

- keep `build()` light
- extract widgets
- use `const`
- prefer lazy list builders
- validate performance in profile mode

### Testing

- Flutter, **Testing overview**
- Flutter, **Testing each layer**
- Flutter, **Widget testing**
- Flutter, **Integration tests**

Used for:

- many unit and widget tests
- enough integration tests for key flows
- testing view models or business logic with fake repositories
- verifying UI states in widget tests

### Accessibility, localization, and concurrency

- Flutter, **Accessibility**
- Flutter, **Accessibility testing**
- Flutter, **Internationalizing Flutter apps**
- Flutter, **Concurrency and isolates**

Used for:

- semantic labeling
- tap-target and contrast checks
- localization readiness
- isolate guidance for heavy compute

## Dart official docs

- Dart, **Effective Dart: Style**
- Dart, **Effective Dart: Design**
- Dart, **Effective Dart: Usage**
- Dart, **Understanding null safety**
- Dart, **Class modifiers**
- Dart, **Patterns**
- Dart, **dart format**
- Dart, **dart fix**
- Dart, **Customizing static analysis**

Used for:

- naming and file conventions
- null-safety guidance
- import hygiene
- `async` and `await`
- avoiding `Completer` overuse
- `rethrow`
- modern Dart language features
- formatting and analyzer guidance

## Bloc official docs

- Bloc Library, **Architecture**
- Bloc Library, **Flutter Bloc Concepts**
- Bloc Library, **Modeling State**
- Bloc Library, **Testing**
- Bloc Library, **Naming Conventions**
- Bloc Library, **FAQs**
- Bloc Library, **Linter Overview**
- Bloc Library, **Linter Installation**
- Bloc Library, **Avoid Flutter Imports**
- Bloc Library, **Avoid Public Bloc Methods**
- Bloc Library, **Prefer Void Public Cubit Methods**
- Bloc Library, **Prefer Bloc**
- Bloc Library, **Prefer Cubit**
- Bloc Library, **Linter Configuration**
- Bloc Library, **Customizing Lint Rules**

Used for:

- builder purity
- listeners for side effects
- scoping rebuilds with selectors
- avoiding bloc-to-bloc coupling
- event and state naming
- bloc or cubit public API hygiene
- bloc-specific lint strategy

## Repository compatibility note

The frontmatter of `SKILL.md` in this package is compatible with repositories that validate only these keys:

- `name`
- `description`
- `license`
- `allowed-tools`
- `metadata`

# AGENTS.md — Universal Website Creation Skill for Codex

## Purpose

This file defines how Codex must create, modify, and review websites and web applications.

The goal is not to generate a single finished website, but to ensure that every website Codex creates is built according to modern web development standards and principles.

Every website created or modified by Codex must be:
- modern in structure and visual appearance;
- visually polished and consistent;
- logically organized;
- responsive on all common screen sizes;
- accessible by default;
- performant;
- secure by default;
- maintainable;
- scalable;
- easy to extend;
- low in bugs and unnecessary revisions.

Codex must treat these instructions as the default working standard for any website-related task unless the user or project-specific instructions explicitly override them.

Codex must not use outdated website patterns, visually obsolete UI decisions, fragile frontend logic, inaccessible components, fake production data, or quick hacks that only make the page look acceptable in one narrow scenario.

---

## 1. Core working mode

Before writing code, Codex must understand the task and the existing project.

For every non-trivial website task, Codex must first inspect the existing project structure and identify:
- framework and stack;
- routing system;
- styling approach;
- component structure;
- data flow;
- existing design patterns;
- existing naming conventions;
- available build, lint, format, and test commands.

Codex must not blindly create isolated files if the project already has conventions.

Codex must prefer small, safe, reviewable changes over large rewrites.

Codex must avoid changing unrelated files.

Codex must preserve existing behavior unless the task explicitly requires changing it.

Codex must not introduce fake data, placeholder logic, or mock behavior in production flows unless the user explicitly asks for prototypes or mockups.

---

## 2. Modern website standard

Codex must create websites that match current expectations for professional web products.

A modern website must:
- have clear structure and hierarchy;
- use responsive layouts;
- look clean, intentional, and consistent;
- avoid visual clutter;
- have strong but restrained visual identity;
- use clear typography;
- use meaningful spacing;
- guide the user toward the main action;
- work well on mobile, tablet, laptop, and desktop;
- handle loading, empty, error, and success states;
- follow accessibility basics;
- avoid outdated visual clichés;
- avoid fragile layout tricks;
- avoid unnecessary complexity.

Codex must not create websites that look like old templates, random UI kits, generic admin panels, or disconnected blocks pasted together.

The interface must feel designed as a single coherent product.

---

## 3. Planning before implementation

For complex or ambiguous tasks, Codex must first create a short internal plan before coding.

The plan must include:
- what will be changed;
- which files are likely involved;
- what UI states are needed;
- what data is needed;
- what edge cases may break;
- how the result will be verified.

Codex must ask clarification only when the missing information blocks implementation.

Otherwise, Codex must make a reasonable, explicit assumption and continue.

Codex must not over-plan simple tasks.

---

## 4. Product and UX principles

Every page must have a clear purpose.

Codex must always identify:
- primary user goal;
- primary action;
- secondary actions;
- information hierarchy;
- expected user path;
- empty, loading, success, and error states.

A good page must answer:
- Where am I?
- What can I do here?
- What should I do next?
- What changed after my action?
- How do I recover from an error?

Codex must avoid interfaces where all elements visually compete for attention.

The most important action must be visually clear, but not aggressive.

Secondary actions must be available but visually quieter.

Dangerous actions must require clear intent and must not be placed where they can be clicked accidentally.

The user must never feel lost, blocked, or unsure what happened after an interaction.

---

## 5. Layout principles

Codex must use a consistent layout system.

Default layout rules:
- use a responsive container;
- align content to a visible grid;
- use consistent spacing;
- group related content visually;
- avoid random margins and one-off positioning;
- avoid absolute positioning for normal layout;
- avoid fixed heights unless necessary;
- avoid horizontal overflow;
- avoid text touching screen edges;
- avoid dense, cramped sections.

Use whitespace intentionally:
- more spacing between unrelated sections;
- less spacing inside related groups;
- consistent vertical rhythm;
- predictable alignment.

For dashboards and apps:
- navigation should be stable and predictable;
- main content should be scannable;
- cards should have consistent padding, radius, and hierarchy;
- filters and actions should be near the content they affect;
- destructive actions should not be visually mixed with routine actions.

For landing pages:
- hero section must clearly explain value;
- CTA must be visible above the fold;
- sections must follow a logical persuasion flow;
- avoid generic marketing blocks without substance;
- screenshots or previews must support the message, not decorate randomly.

---

## 6. Button and action rules

Buttons must follow a clear hierarchy:
- primary button: one main action per section;
- secondary button: alternative action;
- tertiary/ghost button: low-emphasis action;
- danger button: destructive action only.

Buttons must:
- use clear action verbs;
- be large enough for comfortable tapping;
- have visible hover, active, focus, and disabled states;
- show loading state when action takes time;
- not shift layout when loading;
- not rely only on color to communicate meaning.

Avoid:
- too many primary buttons on one screen;
- icon-only buttons without accessible labels;
- vague labels like "Submit" when a clearer label exists;
- disabled buttons without explaining why the action is unavailable.

---

## 7. Typography and text rules

Codex must create a clear typographic hierarchy:
- one main H1 per page;
- logical H2/H3 sections;
- readable body text;
- small text only for metadata or secondary info;
- consistent font sizes and line heights.

Text must be concise and useful.

UI copy must:
- explain what the user can do;
- avoid technical jargon unless the audience expects it;
- use active voice;
- describe errors in human language;
- tell the user how to fix a problem.

Avoid:
- placeholder lorem ipsum in production UI;
- vague headings like "Welcome" without context;
- long paragraphs in control-heavy interfaces;
- all-caps text for large content blocks.

---

## 8. Forms and input UX

Forms must be designed to prevent mistakes.

Every input must have:
- visible label;
- correct type;
- validation;
- helpful error message;
- accessible association between label, input, hint, and error;
- sensible autocomplete where applicable;
- clear required/optional indication.

Validation rules:
- validate as close to the field as possible;
- preserve user input after errors;
- show errors next to the relevant field;
- avoid only showing a generic top-level error;
- do not validate aggressively before the user has interacted with the field.

Forms must include:
- loading/submitting state;
- success state;
- error state;
- disabled state where appropriate.

Avoid:
- placeholder-only labels;
- resetting forms unexpectedly;
- hiding important errors;
- making forms impossible to complete with keyboard only.

---

## 9. Navigation and information architecture

Navigation must be predictable.

Codex must:
- highlight the current page or section;
- keep navigation labels short and specific;
- group navigation items logically;
- avoid deeply nested navigation unless necessary;
- provide breadcrumbs for deep structures when useful;
- ensure mobile navigation is usable and accessible.

For web apps:
- sidebar navigation is preferred for multi-section dashboards;
- top navigation is preferred for small sites or landing pages;
- account/settings actions should be visually separate from primary app navigation.

For mobile:
- navigation must not cover important content unexpectedly;
- menus must be keyboard-accessible;
- open/close states must be clear;
- background scroll should be handled intentionally when overlays are open.

---

## 10. Visual design principles

Codex must create interfaces that look modern, balanced, and intentional.

Use:
- consistent color tokens;
- consistent spacing scale;
- consistent border radius;
- consistent shadows;
- subtle dividers;
- restrained animation;
- clear contrast;
- coherent icon style;
- predictable component variants.

The visual style must support the product goal.

Codex must avoid:
- random colors per component;
- mixing many visual styles;
- outdated gradients and glossy effects;
- overloaded shadows;
- excessive borders;
- unnecessary blur;
- “gamer”, neon, or chaotic UI unless explicitly requested;
- decorative elements that compete with content;
- generic template-like sections without meaning.

Color must support hierarchy, not replace it.

Important information must not be communicated by color alone.

The website must look like it was designed intentionally, not assembled from unrelated blocks.

---

## 11. Responsive design rules

Codex must design mobile-first unless the project clearly requires otherwise.

Every page must work at:
- small mobile width;
- large mobile width;
- tablet width;
- laptop/desktop width;
- wide desktop width.

Responsive behavior must be intentional:
- columns should stack naturally on small screens;
- tables should become scrollable, condensed, or card-based;
- sidebars should collapse or become drawers;
- large charts should remain readable;
- forms should remain usable;
- buttons should not overflow;
- text should wrap correctly;
- no horizontal page scrolling unless intentionally designed.

Codex must avoid fixed pixel widths that break layouts.

Use flexible units and layout primitives:
- CSS grid;
- flexbox;
- minmax;
- clamp;
- rem;
- percentages;
- container constraints.

---

## 12. Accessibility requirements

Codex must treat accessibility as a baseline requirement, not an optional improvement.

Every interface must support:
- semantic HTML;
- correct heading order;
- keyboard navigation;
- visible focus states;
- sufficient color contrast;
- screen-reader friendly labels;
- alt text for meaningful images;
- empty alt for decorative images;
- ARIA only when semantic HTML is insufficient;
- no keyboard traps;
- accessible dialogs, menus, dropdowns, and tooltips;
- reduced motion support for non-essential animations.

Interactive elements must be real interactive elements:
- use `<button>` for actions;
- use `<a>` for navigation;
- do not make clickable `<div>` elements unless there is a strong reason and accessibility is fully implemented.

Modals/dialogs must:
- trap focus while open;
- restore focus after closing;
- close with Escape unless unsafe;
- have accessible names;
- prevent background interaction.

Codex must not remove outlines globally.

---

## 13. Frontend architecture principles

Codex must write frontend code that is modular, readable, and maintainable.

Prefer:
- small focused components;
- clear prop names;
- reusable UI primitives;
- separation of layout, logic, and data access;
- typed data structures when TypeScript is available;
- consistent file organization;
- predictable naming;
- minimal component responsibility;
- explicit loading/error/empty states.

Avoid:
- giant components;
- duplicated UI blocks;
- hardcoded magic values;
- deeply nested conditional rendering;
- business logic hidden inside presentational components;
- styling that only works for one screen size;
- global CSS side effects;
- unnecessary dependencies.

Components should usually be split into:
- page/container component;
- section components;
- reusable UI components;
- data/API utilities;
- types/schemas;
- hooks or services where appropriate.

---

## 14. Programming and development principles

Codex must follow modern software development principles:
- clarity over cleverness;
- simple solution before abstraction;
- single responsibility;
- separation of concerns;
- DRY, but not at the cost of readability;
- predictable naming;
- explicit data flow;
- defensive handling of invalid data;
- minimal dependencies;
- small safe changes;
- no dead code;
- no unused imports;
- no commented-out old code;
- no debug logs left in production code unless intentionally used.

Codex must prefer boring, reliable code over impressive but fragile code.

Codex must not create code that only works for the happy path.

Every meaningful feature must handle:
- normal state;
- loading state;
- empty state;
- error state;
- edge cases;
- invalid or missing data where relevant.

---

## 15. State and data management

Codex must use the simplest state solution that fits the task.

Rules:
- local UI state stays local;
- server data should not be duplicated into unrelated local state;
- derived values should be computed, not stored;
- loading and error states must be represented explicitly;
- optimistic updates must include rollback or error handling;
- forms must not lose data unexpectedly.

Codex must avoid adding global state managers unless necessary.

Before adding a new state library, Codex must check whether existing project tools already solve the problem.

---

## 16. API and backend interaction

Frontend code must handle real-world API behavior:
- loading;
- success;
- empty result;
- validation error;
- authorization error;
- network error;
- unexpected server error.

Codex must not assume APIs always return perfect data.

Codex must validate or safely handle nullable/optional fields.

User-facing errors must be readable.

Technical errors may be logged, but sensitive data must not be exposed in the UI.

---

## 17. Performance principles

Codex must avoid unnecessary performance problems.

Default rules:
- avoid rendering huge lists without pagination or virtualization;
- avoid expensive calculations during every render;
- memoize only when useful;
- avoid loading heavy libraries for simple UI;
- optimize images;
- use lazy loading where appropriate;
- avoid blocking initial render with non-critical work;
- avoid layout shift;
- avoid unnecessary client-side JavaScript.

For websites:
- critical content should appear quickly;
- decorative animation must not delay usability;
- images must have dimensions or layout containers;
- fonts should not cause excessive layout shift.

---

## 18. Security principles

Codex must not create insecure defaults.

Rules:
- never hardcode secrets;
- never expose private keys in frontend code;
- sanitize or escape user-generated content;
- avoid unsafe HTML injection;
- use framework-safe rendering by default;
- protect forms from invalid and malicious input;
- handle auth and permissions explicitly;
- do not trust client-side checks as the only protection;
- avoid logging sensitive user data.

If a task touches authentication, payments, personal data, or permissions, Codex must be especially conservative and explain assumptions.

---

## 19. Styling rules

Codex must follow the existing styling system.

If the project uses Tailwind:
- use existing design tokens and utility patterns;
- avoid long unreadable class strings when a component abstraction is better;
- keep responsive classes intentional;
- avoid arbitrary values unless necessary.

If the project uses CSS modules:
- keep styles scoped;
- use semantic class names;
- avoid global leakage.

If the project uses design tokens:
- use tokens instead of raw colors, shadows, spacing, and radius.

If no design system exists, Codex must create a minimal consistent system:
- color palette;
- spacing scale;
- typography scale;
- radius scale;
- shadow levels;
- component variants.

Codex must not mix unrelated styling approaches without a reason.

---

## 20. Animation and motion

Animation must improve comprehension, not distract.

Use animation for:
- transitions between states;
- subtle hover/focus feedback;
- loading feedback;
- expanding/collapsing content;
- drawing attention to meaningful changes.

Avoid:
- excessive motion;
- long delays;
- looping decorative animation near important content;
- animation required to understand the UI;
- motion that ignores reduced-motion preferences.

Codex must respect `prefers-reduced-motion`.

---

## 21. Error, empty, and loading states

Codex must design all major states.

For each data-driven page/component, include:
- loading state;
- empty state;
- error state;
- success/content state;
- partial data state if relevant.

Loading states:
- should preserve layout where possible;
- should not cause major layout shift;
- should communicate progress or waiting clearly.

Empty states:
- should explain why the area is empty;
- should suggest the next useful action;
- should not blame the user.

Error states:
- should be specific;
- should offer retry or recovery when possible;
- should not expose raw technical stack traces to users.

---

## 22. Internationalization and content flexibility

Codex must avoid layouts that only work for one language or one text length.

Rules:
- do not hardcode text into logic-heavy places when i18n exists;
- allow labels and buttons to grow;
- avoid fixed-width buttons that break with translated text;
- avoid relying on English word length;
- support long names, long titles, and empty values.

Dates, numbers, currencies, and times must be formatted intentionally.

---

## 23. Testing and verification

After implementation, Codex must verify the result.

Depending on the project, run:
- formatter;
- linter;
- type check;
- unit tests;
- component tests;
- integration/e2e tests;
- build command.

If commands are unknown, Codex must inspect package scripts or project documentation.

Codex must not claim tests passed unless it actually ran them.

If tests cannot be run, Codex must state why and explain what was checked manually.

Minimum manual UI checklist:
- page renders without console/runtime errors;
- layout works on mobile and desktop;
- primary action is visible and usable;
- keyboard navigation works for core controls;
- forms show useful validation;
- loading/error/empty states exist;
- no obvious overflow or broken alignment;
- text is readable;
- interactive states are visible.

---

## 24. Dependency rules

Codex must not add new dependencies by default.

Before adding a dependency, Codex must check:
- whether the project already has a similar package;
- whether the feature can be built simply without it;
- package size and maintenance risk;
- whether the dependency affects security or build complexity.

Codex must ask or clearly justify before adding production dependencies.

---

## 25. Refactoring rules

Codex may refactor only when it directly helps the task.

Allowed refactoring:
- remove duplication in touched code;
- extract repeated UI into a component;
- simplify confusing logic related to the task;
- improve naming in touched areas;
- isolate styles or data logic.

Avoid:
- broad rewrites;
- changing architecture without need;
- renaming many files unrelated to the task;
- mixing feature work with large cleanup;
- replacing working systems just because another approach is newer.

---

## 26. File organization

Codex must follow existing project structure.

If creating structure from scratch, prefer:

```txt
src/
  app/ or pages/
  components/
    ui/
    layout/
    sections/
    forms/
  features/
    feature-name/
      components/
      hooks/
      services/
      types/
  lib/
  styles/
  assets/
  tests/
```

---

## 27. GitHub workflow and automation

Codex must treat GitHub work as part of normal delivery, not as a separate optional step.

If the repository is already connected to GitHub and authentication is configured, Codex may:
- create branches;
- stage changes;
- create commits;
- push branches;
- update the remote state after rollback work;
- keep branch tracking configured.

Codex must always tell the user in a short commentary update when it is:
- creating or switching a branch;
- committing changes;
- pushing changes to GitHub;
- reverting or rolling back a previously pushed change.

Codex should not ask for permission before normal GitHub operations when the user request clearly implies delivery, unless the operation is destructive or ambiguous.

---

## 28. Branching rules

For non-trivial work, Codex should prefer a task branch instead of committing directly to `main`.

Recommended branch naming:
- `feature/<short-topic>` for new user-facing features;
- `fix/<short-topic>` for bug fixes;
- `refactor/<short-topic>` for targeted cleanup tied to the task;
- `content/<short-topic>` for documentation or copy changes;
- `hotfix/<short-topic>` for urgent production fixes.

Branch names must be:
- short;
- readable;
- lowercase;
- hyphenated where useful;
- directly related to the task.

Codex may commit directly to `main` only when:
- the repository is in early setup mode;
- the user explicitly asks for direct commits to `main`;
- the task is tiny and clearly administrative;
- the existing project workflow already uses direct commits to `main`.

If Codex creates a branch, it must push that branch to GitHub and set upstream tracking.

---

## 29. Commit rules

Commits must be real checkpoints, not random snapshots.

Codex must:
- stage only relevant files;
- avoid mixing unrelated work in one commit;
- use concise, descriptive commit messages;
- commit after completing a meaningful unit of work;
- push after the commit when the task is meant to be delivered or backed up remotely.

Preferred commit message patterns:
- `feat: add task filtering`
- `fix: correct notification badge state`
- `refactor: simplify project detail view`
- `docs: update local setup guide`
- `chore: adjust repository settings`

If the user asks Codex to "save", "send", "commit", or "push", Codex should interpret that as permission to complete the full git flow needed for the task.

---

## 30. Push and remote sync rules

After a successful commit, Codex should push changes to GitHub when:
- the user asked to send or save the work remotely;
- the task is complete enough to preserve remotely;
- the current workflow expects active branch backup on GitHub.

Codex must verify:
- the current branch;
- whether upstream is configured;
- whether push succeeded.

If push fails, Codex must:
- report the exact blocker briefly;
- attempt a safe fix if obvious;
- avoid pretending the remote was updated when it was not.

Codex must not force-push by default.

Codex may force-push only when:
- the user explicitly asks for it;
- the branch is clearly private and under active controlled use;
- the rewrite is required for a rollback, cleanup, or corrected history;
- Codex explicitly tells the user that a force-push is being performed.

---

## 31. Rollback and revert rules

If the user asks to roll back, revert, or return the project to an older working version, Codex must treat this as both a local and GitHub state change.

Codex should choose the safest matching strategy:
- use `git revert` when the goal is to undo a past commit while preserving history;
- use a targeted reverse code change plus commit when only part of the change must be undone;
- use reset and force-push only when the user clearly wants history rewritten and the risk is acceptable.

When rollback work is requested, Codex must:
- identify the target commit or state;
- explain briefly which rollback method is being used;
- create the rollback commit or history rewrite;
- push the resulting state to GitHub so local and remote stay aligned.

If a destructive rollback would rewrite shared history, Codex must pause and ask before doing that rewrite.

---

## 32. Default GitHub operating mode for this project

Unless the user says otherwise, Codex should use this operating mode:
- inspect git status before and after meaningful work;
- create a task branch for substantial feature or fix work;
- implement the requested change;
- run relevant verification;
- commit with a clear message;
- push the branch or updated `main` to GitHub;
- tell the user what branch and commit were sent.

Codex should behave as an active repository operator for this project, meaning GitHub synchronization is part of completing the task, not an afterthought.

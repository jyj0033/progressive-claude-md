# Evidence-Based Project Detection

Read this reference only while scanning a repository. It defines how to turn repository evidence into claims without inventing project facts.

## Rules

1. Treat filenames as candidates, not conclusions. Confirm a candidate with manifest contents, source imports, configuration, scripts, CI, or documentation.
2. Attach at least one repository-relative evidence path to every claim. Add a line or key when practical, such as `package.json#packageManager`.
3. Use `high`, `medium`, or `low` confidence. Only `high` and `medium` claims may be written as facts. Omit low-confidence claims or list them as unresolved questions.
4. Prefer direct declarations over inference: manifest field > lockfile/config > source import/use > directory naming.
5. Report conflicts instead of choosing silently. Never infer a tool merely because it can consume the detected file format.
6. Do not open `.env*` or credential files, including tracked examples. Derive environment variable identifiers only from schemas, source declarations, or maintained documentation; never read or record assigned values.

## Package and Dependency Managers

| Ecosystem | High-confidence evidence | Do not infer |
|---|---|---|
| Node.js | `package.json#packageManager`; exactly one root lockfile (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lock`/`bun.lockb`) corroborated by scripts or CI | `package.json` alone does not identify npm, Yarn, pnpm, or Bun |
| Python | `poetry.lock` plus `[tool.poetry]`; `uv.lock` plus matching `pyproject.toml`; `Pipfile.lock`; `requirements*.txt` used by docs/CI; `pdm.lock` plus `[tool.pdm]` | `requirements.txt` does not imply Poetry; `pyproject.toml` alone does not identify an installer |
| JVM | Maven wrapper or `pom.xml`; Gradle wrapper plus `build.gradle`/`build.gradle.kts` | Gradle does not imply Kotlin; Maven does not identify the implementation language |
| Go | `go.mod` and `go.sum` | The application type cannot be learned from `go.mod` alone |
| Rust | `Cargo.toml` and optionally `Cargo.lock` | A Cargo manifest does not distinguish CLI, library, or service without its targets/source |
| PHP | `composer.json` and optionally `composer.lock` | Framework cannot be inferred from Composer alone |
| Ruby | `Gemfile` and optionally `Gemfile.lock` | Rails cannot be inferred from a generic Gemfile |

When multiple Node lockfiles exist, record a conflict. Resolve it only with `packageManager`, CI commands, repository documentation, or explicit user confirmation.

## Languages and Frameworks

Use a two-signal rule for frameworks unless the manifest or framework-owned config is decisive.

| Candidate | Strong evidence examples | Weak evidence that is insufficient alone |
|---|---|---|
| TypeScript | `typescript` dependency plus `tsconfig*.json`, or compiled `.ts`/`.tsx` sources and build config | `tsconfig.json` copied into tooling fixtures |
| React | `react` dependency plus JSX/TSX imports or framework config | `components/` directory |
| Next.js | `next` dependency plus `next.config.*`, `app/`, or `pages/` entry conventions | `next.config.*` without a matching dependency/source use |
| Vue/Nuxt | `vue`/`nuxt` dependency plus `.vue` sources or `nuxt.config.*` | `pages/` directory |
| Angular | `@angular/core` plus `angular.json` or Angular bootstrap source | `angular.json` in an example fixture |
| Svelte/SvelteKit | `svelte`/`@sveltejs/kit` plus `.svelte` source or `svelte.config.*` | `.svelte` file in documentation examples |
| Express | `express` dependency plus imports and app/router construction | `app.js` |
| FastAPI | `fastapi` dependency plus imports and `FastAPI(...)` construction | `main.py` |
| Flask | `flask` dependency plus imports and `Flask(...)` construction | `app.py` |
| Django | `django` dependency plus settings/URL configuration or `manage.py` | `manage.py` without inspecting it |
| Rails | Rails gem plus `config/application.rb` and Rails application structure | `Gemfile` |
| Phoenix | Phoenix dependency in `mix.exs` plus endpoint/router modules | `mix.exs` |

Ignore vendored code, generated output, dependency caches, fixtures, and examples unless they are the actual requested project target.

## Database, Cache, and Data Access

Keep these categories separate:

- **Database/cache service:** PostgreSQL, MySQL, SQLite, MongoDB, Redis, and similar systems.
- **Data-access layer:** Prisma, Sequelize, TypeORM, SQLAlchemy, Django ORM, Hibernate, and similar libraries.
- **Driver/client:** `pg`, `mysql2`, `pymongo`, and similar packages.

An ORM or driver is not a database. Identify the backing service only from explicit provider/config declarations, migrations, connection scheme in a safe example, Compose/service definitions, or documentation. If an ORM supports several providers and no provider is configured, report only the ORM.

Never inspect or output live connection strings, environment files, or credentials.

## Tests, Build Tools, and Commands

- Detect a test framework from its dependency/config plus actual test files or executable scripts.
- Detect a build tool from its dependency/config plus scripts or CI invocation.
- Copy commands only from executable sources: manifest scripts, Make/Task/Just targets, wrapper scripts, CI workflows, or maintained documentation.
- Do not synthesize commands such as `npm run dev`, `pytest`, or `make deploy` because they are conventional.
- Preserve the repository's exact command and working directory. For monorepos, state the package path.

## Project Shape

Classify `frontend`, `backend`, `full-stack`, `CLI`, `library`, `mobile`, or `monorepo` only from behavior and build targets:

- Entry points, package exports/bin targets, route/server bootstrap, application manifests, workspace declarations, and deployment config are strong signals.
- Names such as `src`, `api`, `components`, or `packages` are supporting evidence only.
- A repository may have several shapes. Record package-level classifications rather than forcing one root label.

Return the canonical schema from [Agent output contract](contracts.md) with `agent: scanner`. Use repository-relative paths. Omit unresolved claims; never use a guessed placeholder such as `None`, `npm/yarn/pnpm`, or `[framework]` as a project fact.

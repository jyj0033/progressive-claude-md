# Project Type Detection Reference

根据项目中的关键文件识别项目类型和技术栈。

## Project Type Detection

| Indicator Files | Project Type | Examples |
|-----------------|--------------|----------|
| package.json, tsconfig.json | TypeScript Project | Generic TS project |
| package.json, vite.config.ts | Vite + TypeScript | SPA, Vite-based |
| package.json, next.config.js | Next.js | SSR, full-stack |
| package.json, nuxt.config.ts | Nuxt.js | SSR, Vue-based |
| package.json, react-scripts/ | Create React App | Legacy React SPA |
| requirements.txt, manage.py | Python/Django | Django web app |
| requirements.txt, app.py | Python/Flask | Flask API |
| requirements.txt, fastapi/ | Python/FastAPI | FastAPI service |
| go.mod | Go Project | Go service |
| Cargo.toml | Rust Project | Rust crate |
| pom.xml | Java/Maven | Java application |
| build.gradle | Kotlin/Gradle | Android/Kotlin |
| composer.json | PHP/Composer | PHP project |
| mix.exs | Elixir/Phoenix | Phoenix web app |
| Gemfile | Ruby/Rails | Rails application |

## Tech Stack Detection

### Package Managers

| File | Package Manager |
|------|-----------------|
| package.json | npm/yarn/pnpm |
| requirements.txt | pip/poetry |
| go.mod | go mod |
| Cargo.toml | cargo |
| pom.xml | Maven |
| build.gradle | Gradle |
| composer.json | Composer |
| mix.exs | Mix |
| Gemfile | Bundler |

### Frontend Frameworks

| Detection | Framework |
|-----------|-----------|
| react/, react-dom, react-router | React |
| @vue/, vue/, vue-router | Vue |
| @angular/, angular.json | Angular |
| svelte/ | Svelte |
| solid-js/ | Solid |
| next/, next.config.js | Next.js |
| nuxt/, nuxt.config.ts | Nuxt.js |

### Backend Frameworks

| Detection | Framework |
|-----------|-----------|
| express/, app.js | Express.js |
| fastapi/, main.py | FastAPI |
| django/, manage.py | Django |
| flask/, app.py | Flask |
| gin-gonic/gin | Gin (Go) |
| echo.labstack.com/echo | Echo (Go) |
| actix-web | Actix (Rust) |
| rails/ | Rails |
| phoenix/ | Phoenix |

### Databases

| Detection | Database |
|-----------|----------|
| postgres/, postgresql | PostgreSQL |
| mysql/ | MySQL |
| mongodb/ | MongoDB |
| redis/ | Redis |
| sqlite/ | SQLite |
| prisma/ | Prisma ORM |
| sequelize/ | Sequelize |

### State Management

| Detection | Library |
|-----------|---------|
| zustand/ | Zustand |
| redux/, @reduxjs/ | Redux |
| mobx/ | MobX |
| pinia/ | Pinia |
| vuex/ | Vuex |

### Testing Frameworks

| Detection | Framework |
|-----------|-----------|
| jest/ | Jest |
| vitest/ | Vitest |
| mocha/ | Mocha |
| playwright/ | Playwright |
| cypress/ | Cypress |
| rspec/ | RSpec |
| pytest/ | pytest |

### Build Tools

| Detection | Tool |
|-----------|------|
| vite.config | Vite |
| webpack.config | Webpack |
| rollup.config | Rollup |
| esbuild | esbuild |
| tsconfig.json | TypeScript |

## Directory Structure Patterns

### Frontend Project

```
src/
├── components/     # UI components
├── pages/          # Page components / routes
├── hooks/          # Custom hooks
├── utils/          # Utility functions
├── stores/         # State management
├── api/            # API calls
├── types/          # TypeScript types
└── App.tsx         # Root component
```

### Backend Project

```
src/
├── routes/         # API routes
├── controllers/    # Request handlers
├── models/         # Data models
├── services/       # Business logic
├── middleware/     # Express middleware
├── utils/          # Utility functions
└── index.js        # Entry point
```

### Full-Stack Project

```
src/
├── client/         # Frontend code
├── server/         # Backend code
├── shared/         # Shared types/utils
└── packages/       # Shared packages
```

## Framework-Specific Patterns

### Next.js

```
pages/              # Pages (or app/ for App Router)
  ├── _app.tsx      # Custom App
  ├── api/          # API routes
  └── index.tsx     # Home page
app/                # App Router (Next.js 13+)
  ├── layout.tsx    # Root layout
  ├── page.tsx      # Home page
  └── api/          # API routes
```

### React + Vite

```
src/
├── components/     # Components
├── pages/          # Route components
├── main.tsx        # Entry point
└── App.tsx         # Root component
```

### Django

```
project_name/
├── manage.py
├── project_name/   # Project settings
├── app_name/       # Django apps
├── templates/      # HTML templates
└── static/         # Static files
```

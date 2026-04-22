# Multi-Agent Packaging для coding agents

Статус: принято как направление архитектуры. Текущий source layer уже живет в `src/content/`.

Исторические рабочие планы перенесены в [docs/archive/](archive/README.md).

## 1. Цель

Репозиторий должен иметь один общий source layer для содержимого продукта и отдельные packaging targets для разных coding agents.

Поддерживаемые цели проектирования:

- `Codex`
- `Claude Code`
- `Qwen Code`

Ключевое ограничение: не существует общего plugin artifact для всех агентов. Codex plugins, Claude Code plugins и Qwen Code extensions нельзя считать взаимозаменяемыми.

## 2. Текущее состояние

- reusable source живет в `src/content/`
- product manifests живут в `src/modules/`
- generated plugin bundles живут в `plugins/`
- release assets живут в `dist/`

Shared conventions and templates live in `src/content/shared/` and are emitted into Codex output for compatibility with the current plugin format.

## 3. Рекомендуемая архитектура

Целевая модель:

```text
shared source model
  -> target adapters
      -> Codex plugin assets
      -> Claude Code plugin assets
      -> Qwen install surface
```

Принципы:

- source of truth существует один раз
- agent-specific artifacts генерируются
- public install surfaces остаются раздельными
- `fiction-core` остается базовым продуктом
- `engineering-addon` и `obsidian-addon` остаются optional

## 4. Целевая структура

```text
codex-story-skills/
  src/
    product.yaml
    modules/
      fiction-core.yaml
      engineering-addon.yaml
      obsidian-addon.yaml
    content/
      shared/
        conventions.md
        templates/
          metadata-block-template.md
      skills/
        project-orchestrator/
          skill.yaml
          prompt.md
          rules/
          templates/
        writer-assistant/
          skill.yaml
          prompt.md
          rules/
          templates/
        story-analyst/
          skill.yaml
          prompt.md
          rules/
          templates/
        continuity-keeper/
          skill.yaml
          prompt.md
          rules/
          templates/
        project-bootstrap/
          skill.yaml
          prompt.md
          rules/
          templates/
        rfc-adr-assistant/
          skill.yaml
          prompt.md
          rules/
          templates/
        obsidian-compat/
          skill.yaml
          prompt.md
          rules/
          templates/

  targets/
    codex/
      manifests/
      adapters/
      build.py
      install-package.sh
    claude/
      manifests/
      adapters/
      build.py
      install-package.sh
    qwen/
      README.md
      install-claude-compatible.sh
      smoke-test.md

  generated/
    codex/
    claude/
    qwen/

  dist/
    codex/
    claude/
    qwen/
```

`generated/` и `dist/` не являются source of truth и не должны редактироваться вручную.

## 5. Shared Source Model

Внутренний model должен описывать содержимое, а не plugin format конкретного агента.

Минимальная форма `skill.yaml`:

```yaml
id: writer-assistant
kind: skill
title_ru: writer-assistant
description_ru: Редакторско-архитектурный агент художественного проекта.
product_area: fiction
tier: core
entrypoint: prompt.md
rules:
  - rules/trigger-rules.md
  - rules/canon-rules.md
templates:
  - templates/current-canon-template.md
  - templates/scene-plan-template.md
shared:
  - shared/conventions.md
  - shared/templates/metadata-block-template.md
capabilities:
  - writing
  - project-structure
agent_notes:
  codex:
    trigger_name: writer-assistant
  claude:
    package_entry: writer-assistant
  qwen:
    compatibility: claude-marketplace
```

Назначение файлов:

- `prompt.md` — роль, границы, принцип работы
- `rules/` — reasoning, routing и доменные правила
- `templates/` — формы результата
- `shared/` — общие conventions и shared templates
- `modules/*.yaml` — состав product packages

Внутренний model не должен содержать `.codex-plugin/plugin.json`, Claude Code manifest или Qwen extension manifest.

## 6. Packaging Targets

### Codex

Codex target генерирует текущую структуру Codex plugin:

```text
generated/codex/fiction-core/
  .codex-plugin/plugin.json
  skills/
    CONVENTIONS.md
    _shared/
    project-orchestrator/SKILL.md
```

Текущая практическая граница Codex target вынесена в `scripts/targets/codex.py`.
Это отдельный adapter слой, который сохраняет существующий CLI и byte-compatible output,
но делает Codex-specific generation явным местом для следующих target-сплитов.

Правила генерации:

- из `skill.yaml` и `prompt.md` генерируется `SKILL.md`
- `rules/` генерируется как `references/`
- `templates/` копируется как `templates/`
- `src/modules/*.yaml` задает состав Codex plugin bundles

Release assets:

```text
dist/codex/fiction-core.zip
dist/codex/engineering-addon.zip
dist/codex/obsidian-addon.zip
```

### Claude Code

Claude target генерирует отдельный Claude Code package.

Ограничения:

- не использовать `.codex-plugin`
- не утверждать, что Codex plugin installable в Claude Code
- не копировать source content вручную
- сохранять те же product modules, что и Codex target

Release assets:

```text
dist/claude/fiction-core.zip
dist/claude/engineering-addon.zip
dist/claude/obsidian-addon.zip
```

### Qwen Code

Начальная рекомендация: поддерживать Qwen через Claude-compatible package, если это практично и проходит smoke test.

Причина: Qwen Code явно поддерживает установку Claude Code Marketplace plugins, поэтому безопаснее сначала использовать проверенный Claude-compatible install path, а не вводить direct Qwen target без подтвержденного runtime contract.

Публичная формулировка:

```text
Qwen support uses the Claude-compatible package. Direct Qwen-native packaging is not provided unless a separate Qwen target is implemented and tested.
```

Direct Qwen target допустим позже, если появятся:

- подтвержденная Qwen-native manifest schema
- отдельный build adapter
- smoke test установки и запуска
- отдельный install flow

## 7. Install Flows

### Codex

```bash
bash install-package.sh --plugin fiction-core --version vX.Y.Z
```

Flow:

1. скачать `dist/codex/<package>.zip`
2. распаковать в локальный Codex plugin root
3. зарегистрировать package в Codex local marketplace
4. установить plugin через Codex plugin management

### Claude Code

```bash
bash install-package.sh --plugin fiction-core --version vX.Y.Z
```

Flow:

1. скачать `dist/claude/<package>.zip`
2. выполнить Claude Code native install flow
3. не трогать Codex local marketplace
4. не использовать Codex plugin artifact

### Qwen Code

```bash
bash install-claude-compatible.sh --plugin fiction-core --version vX.Y.Z
```

Flow:

1. использовать Claude-compatible package
2. установить его через поддерживаемый Qwen Code flow
3. считать поддержку Qwen ограниченной этим проверенным path

## 8. Shared, adapted и specific части

Полностью shared:

- fiction-first доменная логика
- роли skills
- rules
- templates
- shared conventions
- состав product modules
- optional статус `engineering-addon`
- optional статус `obsidian-addon`

Agent-adapted:

- entrypoint format
- trigger descriptions
- manifest metadata
- capabilities и categories
- examples, если agent runtime требует другой invocation style

Agent-specific:

- `.codex-plugin/plugin.json`
- Codex local marketplace registration
- Claude Code package manifest
- Qwen extension manifest, если появится direct target
- release asset layout
- install scripts
- smoke tests

## 9. Migration Plan

Historical checklist and session handoff: [docs/archive/PACKAGING_MIGRATION_PLAN.md](archive/PACKAGING_MIGRATION_PLAN.md).

1. Зафиксировать текущую Codex сборку как baseline.
2. Создать `src/content/` и перенести туда reusable content без изменения смысла. Выполнено для shared content, `obsidian-compat` и `rfc-adr-assistant`.
3. Разделить каждый `SKILL.md` на `skill.yaml` и `prompt.md`. Выполнено для `obsidian-compat` и `rfc-adr-assistant`.
4. Переименовать `references/` в `rules/` во внутреннем source layer. Выполнено для `obsidian-compat` и `rfc-adr-assistant`.
5. Написать Codex adapter, который генерирует текущий Codex output. Выполнено для migrated pilot content.
6. Усилить validation для migrated `skill.yaml`: проверять `entrypoint`, перечисленные `rules`, `templates` и optional `shared` paths. Выполнено для текущего pilot set.
7. Переключить release workflow Codex на `targets/codex`.
8. Добавить Claude target как отдельный adapter из того же source.
9. Добавить Qwen install surface через Claude-compatible package после smoke test.
10. Обновить README, INSTALL и release docs под отдельные install flows.

## 9.1. Current invariants

1. Keep `src/content/skills/obsidian-compat/` and `src/content/skills/rfc-adr-assistant/` as the canonical migrated sources.
2. Keep `src/modules/*.yaml` as the bundle definitions driving generated output.
3. Keep byte-compatible plugin output stable for the migrated skills across `validate-skills.py` and `build-plugins.py`.

## 10. Риски и Ограничения

Риски:

- runtime Claude Code может не совпасть с семантикой Codex skill
- установка через Claude-compatible package не гарантирует полную runtime parity
- агентные документы могут начать расходиться с shared source semantics

Ограничения:

- не обещать universal plugin
- не публиковать один zip для всех agents
- не считать Claude target производным от Codex target
- не считать direct Qwen support реализованным без отдельного target и smoke test
- не делать Obsidian частью base fiction model

Неподдерживаемые assumptions:

- Codex plugins напрямую installable в Claude Code
- Codex plugins напрямую installable в Qwen Code
- Claude-compatible Qwen install означает полную feature parity
- один manifest может описать каждый agent runtime

## 11. Рекомендация по Supported Matrix

Рекомендуемый порядок:

1. `Codex` — текущий supported target.
2. `Codex + Claude Code` — следующий supported matrix.
3. `Codex + Claude Code + Qwen Code` — только после smoke test Claude-compatible package в Qwen Code.

До проверки Qwen должен быть описан как planned или experimental compatibility path, а не как direct supported target.

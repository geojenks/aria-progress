# Project Reporting System

A lightweight, agent-friendly way to turn day-to-day work into funder-ready reports
without re-deriving everything each quarter. Three layers, each feeding the next:

```
sessions/   →   weekly/   →   reports/
(raw work)      (synthesis)   (against aims)
```

1. **Session reports** (`sessions/<area>/YYYY-MM-DD_<slug>.md`)
   One per agent per work session. Append-only. Written at the *end* of a session
   (by the agent that did the work). Small, concrete, tagged.

2. **Weekly rollups** (`weekly/YYYY-Www_<area>.md`)
   Once a week per area, synthesise that week's session reports into progress + ideas
   + direction. This is the layer a human skims.

3. **Master reports** (`reports/<period>.md`)
   A master agent reads `PROJECT_AIMS.md` + the weekly rollups (and sessions if it needs
   detail) and writes a few-page report **mapped onto the project aims**, with RAG and
   milestone status. This is what goes to ARIA.

## Why the front-matter matters
Every session/weekly file starts with YAML front-matter (`date`, `area`, `milestone`,
`status`, …). That's the contract that lets the master agent aggregate reliably — group
by `milestone`, roll up `status`, order by `date` — instead of parsing prose. Keep the
`area` and `milestone` values drawn from `PROJECT_AIMS.md` so everything reconciles.

## The fixed yardstick
`PROJECT_AIMS.md` is the one file that changes rarely: the WPs, deliverables, and
milestones George owns. Every report is written *against* it. Update it only when the
actual project scope changes.

## Roles
- **Work agents** own an `area`. Each writes its own session reports and (optionally) its
  weekly rollup for that area. Mirrors the `‹↻ agent›` ownership model already in use.
- **Master agent** owns synthesis only. It does not edit session reports; it reads them.

## Cadence (suggested)
- Session report: end of every substantive session.
- Weekly rollup: end of week, per active area.
- Master report: on ARIA checkpoints (quarterly) + on demand.

## Layout
```
reporting/
├── README.md                 # this file
├── PROJECT_AIMS.md           # the fixed yardstick (WPs / deliverables / milestones)
├── templates/
│   ├── session_report.md     # copy → sessions/<area>/
│   ├── weekly_update.md       # copy → weekly/
│   └── master_report_prompt.md   # the instruction the master agent runs
├── sessions/                 # raw end-of-session reports, per area
│   └── <area>/YYYY-MM-DD_<slug>.md
├── weekly/                   # weekly rollups
│   └── YYYY-Www_<area>.md
└── reports/                  # synthesised master reports
    └── <period>.md
```

## Hosting
Lives in a git repo (access-gated, not public). Can be the same repo as the code
(a top-level `reporting/` folder) or a dedicated coordination repo — decide once and
put the choice here.

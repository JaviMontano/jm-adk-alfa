# JM-ADK Architecture

Visual overview of how the kit works.

## System Overview

```mermaid
graph TB
    subgraph User["User"]
        CMD["/jm-adk:command"]
    end

    subgraph Orchestration["Orchestration Layer"]
        ORC["adk-orchestrator<br/>(Router)"]
        PC["pipeline-conductor<br/>(Sequencing)"]
        SR["skill-router<br/>(BM25 Search)"]
        QG["quality-guardian<br/>(G0-G3 Gates)"]
        CM["context-manager<br/>(Token + RAG)"]
    end

    subgraph Agents["Specialist Agents (101)"]
        DA["Discovery<br/>20 agents"]
        AA["Architecture<br/>20 agents"]
        FA["Frontend<br/>20 agents"]
        BA["Backend/Firebase<br/>15 agents"]
        QA["Quality/Testing<br/>12 agents"]
        DEP["Deployment<br/>5 agents"]
        DOC["Documentation<br/>4 agents"]
    end

    subgraph Skills["Skills Library (101)"]
        DS["Discovery<br/>20 skills"]
        AS["Architecture<br/>20 skills"]
        FS["Frontend<br/>25 skills"]
        BS["Backend<br/>20 skills"]
        QS["Quality<br/>10 skills"]
        DPS["Deployment<br/>6 skills"]
    end

    subgraph Output["Output"]
        CODE["Code"]
        DOCS["Documentation"]
        DEPLOY["Deployment"]
    end

    CMD --> ORC
    ORC --> PC
    ORC --> SR
    PC --> DA & AA & FA & BA & QA & DEP & DOC
    SR --> Skills
    DA --> DS
    AA --> AS
    FA --> FS
    BA --> BS
    QA --> QS
    DEP --> DPS
    QG -.->|validates| CODE & DOCS & DEPLOY
    CM -.->|optimizes| ORC
```

## Two-Phase Pipeline

```mermaid
graph LR
    subgraph Phase1["Phase 1: ANALYZE (MAO DNA)"]
        D["Discover"] --> M["Map"] --> A["Assess"] --> V["Validate"] --> S["Specify"]
    end

    subgraph Phase2["Phase 2: DEVELOP (SA DNA)"]
        DES["Design"] --> SC["Scaffold"] --> B["Build"] --> T["Test"] --> DEP["Deploy"]
    end

    Phase1 -->|"RQL + Spec"| Phase2
```

## Metacognition Cycle (DSVSR)

```mermaid
graph TD
    DEC["DECOMPOSE<br/>Break into sub-problems"] --> SOL["SOLVE<br/>Address each (0.0-1.0)"]
    SOL --> VER["VERIFY<br/>6 dimensions"]
    VER --> SYN["SYNTHESIZE<br/>Weighted confidence"]
    SYN --> REF{"REFLECT<br/>confidence >= 0.95?"}
    REF -->|No| DEBATE["Socratic Debate<br/>+ WebSearch"]
    DEBATE --> SOL
    REF -->|Yes| OUT["OUTPUT<br/>with evidence tags"]
```

## Quality Gates

```mermaid
graph LR
    G0["G0: Security<br/>No secrets<br/>No XSS"] --> G1["G1: Evidence<br/>All claims tagged<br/>Constitution OK"]
    G1 --> G2["G2: Lighthouse<br/>Perf > 90<br/>A11y > 95"]
    G2 --> G3["G3: Deployment<br/>Hostinger/Firebase<br/>compatible"]
    G3 --> SHIP["SHIP"]

    style G0 fill:#dc2626,color:#fff
    style G1 fill:#f59e0b,color:#000
    style G2 fill:#2563eb,color:#fff
    style G3 fill:#16a34a,color:#fff
    style SHIP fill:#7c3aed,color:#fff
```

## Intent Integrity Chain

```mermaid
graph LR
    INT["Intent<br/>(user request)"] --> RQL["RQL-NNN<br/>(requirement)"]
    RQL --> PLAN["plan-DATE.md<br/>(plan file)"]
    PLAN --> ADR["ADR-NNN<br/>(decision)"]
    ADR --> SPEC["Spec<br/>(feature spec)"]
    SPEC --> TEST["Tests<br/>(before code)"]
    TEST --> CODE["Code<br/>(implementation)"]

    style INT fill:#f8fafc,stroke:#334155
    style CODE fill:#16a34a,color:#fff
```

## Agent Routing

```mermaid
graph TD
    REQ["User Request"] --> CLASS{"Classify"}

    CLASS -->|"requirements, analysis"| RA["requirements-analyst"]
    CLASS -->|"architecture, design"| AD["architecture-designer"]
    CLASS -->|"firebase, auth, firestore"| FS["firebase-specialist"]
    CLASS -->|"HTML, CSS, frontend"| FC["frontend-craftsman"]
    CLASS -->|"Angular"| AS["angular-specialist"]
    CLASS -->|"React"| RS["react-specialist"]
    CLASS -->|"testing, quality"| QE["quality-engineer"]
    CLASS -->|"deploy, hosting"| DS["deployment-specialist"]
    CLASS -->|"docs, ADR"| TW["technical-writer"]
```

## File Organization

```mermaid
graph TD
    ROOT["jm-adk-alfa/"]

    ROOT --> AGENTS["agents/<br/>256 .md files"]
    ROOT --> COMMANDS["commands/<br/>260 .md files"]
    ROOT --> SKILLS["skills/<br/>524 dirs/SKILL.md"]
    ROOT --> PROMPTS["prompts/<br/>256 .md files"]
    ROOT --> DOCS["docs/<br/>human-readable"]
    ROOT --> AGENT[".agent/<br/>Antigravity compat"]
    ROOT --> SPECIFY[".specify/<br/>governance"]
    ROOT --> HOOKS["hooks/<br/>automation"]

    DOCS --> GS["getting-started.md"]
    DOCS --> MCP["mcp-integration.md"]
    DOCS --> CAT["catalog.md"]
    DOCS --> ADV["advanced/"]
    DOCS --> EX["examples/"]
```

---

*Made with Claude Code and Tons of Love with the Help of Pristino Agent*

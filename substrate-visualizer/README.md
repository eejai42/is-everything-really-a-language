# Substrate Visualizer

Interactive visualization of the Effortless Rulebook architecture - replicating `effortless_rulebook_architecture.png` but modular, JSON-driven, and with a draggable **LLM Context Window** to illustrate the fragmentation problem.

## Goals

1. Replicate the architecture diagram: SSoT → Rulebook Hub → Substrates → Foundation
2. Make it **JSON-driven** - all configuration in `visualizer-config.json`
3. Show the **hub-spoke architecture** (rulebook as hub, everything else as spokes)
4. Support **swappable SSoT** (Airtable, Notion, Google Sheets, etc.)
5. Support **swappable Foundation** (PostgreSQL, SQL Server, DuckDB, etc.)
6. Show **25+ potential substrates**, not just the 10 implemented
7. Allow **filtering/hiding** substrates by category or implementation status
8. **LLM Context Window** - draggable "peephole" showing what an LLM can see at any time

## The Key Insight

The static diagram shows a top-to-bottom flow, but architecturally it's a **hub-spoke model**:
- **Hub**: `effortless-rulebook.json` (the declarative center)
- **Spokes**: All substrates (SSoT above, execution substrates in middle, foundation below)

## Core Principle: Single JSON Source of Truth

**The JSON file IS the model. The HTML is just a viewer.**

```
visualizer-config.json  →  index.html (pure visualization)
         ↑
    (all data lives here)
```

- All substrate definitions, scores, categories, colors
- All SSoT and Foundation options
- Hub configuration
- LLM context window settings
- NO external data fetches - the JSON is complete and self-contained

This mirrors the ERB philosophy: the rulebook is the single source of truth, and everything else is a substrate that renders it.

## Files

```
substrate-visualizer/
├── README.md               # This file
├── index.html              # Pure visualization (no data, just rendering logic)
└── visualizer-config.json  # THE model - all data lives here
```

## Component Architecture

### 1. SSoT Layer (top)
- Gold-colored box (matches Airtable styling)
- Carousel to rotate between: Airtable, Notion, Google Sheets, Baserow, Coda
- Arrow flowing down to hub

### 2. Hub (center)
- Blue "Effortless Rulebook" box
- Always stable, always visible
- Arrows radiating to all spokes

### 3. Substrates Grid (middle)
- Responsive grid of boxes (implemented + potential)
- **Implemented**: solid border, full opacity, score indicator
- **Potential**: dashed border, 50% opacity, grayscale
- Filter controls: category dropdown, implemented/all toggle

### 4. Foundation Layer (bottom)
- PostgreSQL-styled bar with "answer-key.json" indicator
- Carousel to swap: PostgreSQL, SQL Server, DuckDB, SQLite, CockroachDB

### 5. LLM Context Window (overlay)
- Draggable semi-transparent rectangle (~200x200px)
- Everything **outside** the window is dimmed (75% opacity overlay)
- Counter showing "3 of 25 substrates visible to LLM"
- Illustrates the **fragmentation problem**: LLMs can only "see" a few substrates at once

## Technical Approach

### LLM Context Window: CSS clip-path

```
┌─────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░┌──────────────────┐░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│ LLM Context      │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   ┌────┐ ┌────┐  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   │Py  │ │Go  │  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   └────┘ └────┘  │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   ┌────┐         │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   │CSV │         │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░│   └────┘         │░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░└──────────────────┘░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└─────────────────────────────────────────────────────────┘
   ░ = dimmed (outside LLM view)
   □ = visible substrates (inside LLM peephole)
```

**Implementation**:
1. Full-screen dim overlay (`rgba(0,0,0,0.75)`)
2. Dynamic `clip-path: polygon()` creates transparent "hole"
3. Draggable border element tracks position
4. On drag: update clip-path CSS variables, recalculate visible count

**Visibility counting**: Any overlap counts - if even 1 pixel of a substrate is under the window, it's marked as "visible".

### SSoT/Foundation Swap: Icon Carousel

- Horizontal row of icons
- Active option: centered, enlarged (1.2x), full color
- Inactive options: smaller, grayed out
- Arrow buttons to rotate

### Substrate Grid: Responsive CSS Grid

```css
grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
```

### Connection Lines: SVG Bezier Curves

- Dynamic SVG paths from hub to implemented substrates
- Dashed stroke with flowing animation

## Data Model (`visualizer-config.json`)

```json
{
  "hub": {
    "id": "effortless-rulebook",
    "label": "Effortless Rulebook",
    "sublabel": "effortless-rulebook.json",
    "description": "Declarative Hub",
    "color": "#4A90D9"
  },
  "layers": {
    "ssot": {
      "description": "Single Source of Truth",
      "active": "airtable",
      "options": [
        { "id": "airtable", "label": "Airtable", "color": "#FCBF49", "implemented": true },
        { "id": "notion", "label": "Notion", "implemented": false },
        { "id": "google-sheets", "label": "Google Sheets", "implemented": false },
        { "id": "baserow", "label": "Baserow", "implemented": false }
      ]
    },
    "foundation": {
      "description": "Canonical Computation Engine",
      "active": "postgresql",
      "options": [
        { "id": "postgresql", "label": "PostgreSQL", "sublabel": "Tables + calc_*() Functions + Views", "color": "#336791", "implemented": true },
        { "id": "sqlserver", "label": "SQL Server", "implemented": false },
        { "id": "duckdb", "label": "DuckDB", "implemented": false }
      ]
    }
  },
  "substrates": [
    { "id": "python", "label": "Python", "icon": "snake", "implemented": true, "category": "code", "score": 100 },
    { "id": "golang", "label": "Golang", "icon": "gopher", "implemented": true, "category": "code", "score": 100 },
    { "id": "typescript", "label": "TypeScript", "icon": "ts", "implemented": false, "category": "code" },
    { "id": "rust", "label": "Rust", "icon": "crab", "implemented": false, "category": "code" },
    { "id": "csv", "label": "CSV", "icon": "table", "implemented": true, "category": "data", "score": 100 },
    { "id": "xlsx", "label": "XLSX", "icon": "excel", "implemented": true, "category": "data", "score": 100 },
    { "id": "yaml", "label": "YAML", "icon": "yaml", "implemented": true, "category": "data", "score": 100 },
    { "id": "owl", "label": "OWL", "icon": "owl", "implemented": true, "category": "semantic", "score": 100 },
    { "id": "uml", "label": "UML", "icon": "class", "implemented": true, "category": "diagram", "score": 100 },
    { "id": "english", "label": "English", "icon": "speech", "implemented": true, "category": "natural", "score": 78 },
    { "id": "binary", "label": "Binary", "icon": "binary", "implemented": true, "category": "low-level", "score": 54 },
    { "id": "readme", "label": "README", "icon": "book", "implemented": false, "category": "docs" },
    { "id": "openapi", "label": "OpenAPI", "icon": "api", "implemented": false, "category": "api" },
    { "id": "graphql", "label": "GraphQL", "icon": "graphql", "implemented": false, "category": "api" },
    { "id": "figma", "label": "Figma", "icon": "design", "implemented": false, "category": "design" },
    { "id": "react", "label": "React App", "icon": "react", "implemented": false, "category": "code" }
  ],
  "categories": [
    { "id": "code", "name": "Programming Languages", "color": "#3B82F6" },
    { "id": "data", "name": "Data Formats", "color": "#10B981" },
    { "id": "semantic", "name": "Semantic Web", "color": "#8B5CF6" },
    { "id": "diagram", "name": "Diagrams", "color": "#EF4444" },
    { "id": "natural", "name": "Natural Language", "color": "#F59E0B" },
    { "id": "low-level", "name": "Low-Level", "color": "#6B7280" },
    { "id": "api", "name": "API Specs", "color": "#EC4899" },
    { "id": "docs", "name": "Documentation", "color": "#06B6D4" },
    { "id": "design", "name": "Design", "color": "#A855F7" }
  ],
  "llmContextWindow": {
    "enabled": true,
    "width": 220,
    "height": 180,
    "initialPosition": { "x": 150, "y": 350 }
  }
}
```

## Implementation Phases

### Phase 1: Core Structure
- [x] Create `substrate-visualizer/` folder
- [ ] Create `visualizer-config.json` with full configuration
- [ ] Create `index.html` skeleton

### Phase 2: CSS Layout
- [ ] CSS variables (matching existing project theme)
- [ ] SSoT section (gold, top)
- [ ] Hub section (blue, center)
- [ ] Substrate grid (responsive)
- [ ] Foundation section (PostgreSQL blue, bottom)
- [ ] Implemented vs potential visual states

### Phase 3: JavaScript - Config Loading
- [ ] Fetch and parse `visualizer-config.json`
- [ ] Render SSoT carousel
- [ ] Render hub component
- [ ] Render substrate cards
- [ ] Render foundation carousel

### Phase 4: LLM Context Window
- [ ] Dim overlay with clip-path hole
- [ ] Draggable window element
- [ ] Mouse event handlers
- [ ] Update clip-path on drag
- [ ] Calculate visible substrates count
- [ ] Toggle button to show/hide

### Phase 5: Interactivity & Polish
- [ ] SSoT swap with arrow buttons
- [ ] Foundation swap with arrow buttons
- [ ] Category filter dropdown
- [ ] Implemented/All toggle
- [ ] SVG connection lines (animated)
- [ ] Dark mode toggle

## Interactions

| Action | Behavior |
|--------|----------|
| Click SSoT arrows | Rotate through SSoT options |
| Click substrate | Toggle enabled/disabled state |
| Category dropdown | Show/hide substrates by category |
| Drag context window | Move the "peephole", counter updates |
| Click foundation arrows | Rotate through foundation options |
| "Show All" toggle | Show all substrates vs only implemented |
| Theme toggle | Switch dark/light mode |

## Verification Checklist

- [ ] Layout matches original architecture diagram flow
- [ ] SSoT swapping works (arrow buttons rotate)
- [ ] Substrate filtering works (category dropdown, implemented toggle)
- [ ] Foundation swapping works
- [ ] LLM context window drags smoothly
- [ ] Dimming effect works (outside window is dimmed)
- [ ] Visibility counter updates on drag
- [ ] Responsive on different screen sizes
- [ ] Dark mode toggle works

## Reference Files (for visual style only)

| File | Use |
|------|-----|
| `../effortless_rulebook_architecture.svg` | Visual style reference (colors, layout) |
| `../orchestration/orchestration-report.html` | CSS variable system, theme toggle |

**Note:** Substrate scores are embedded directly in `visualizer-config.json`, not fetched from external files. When scores change, update the JSON.

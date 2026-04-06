# Plant-Asset-Network-and-Database-Agent-_PANDA
Plant Asset and Network Database Agent (PANDA) — Maintenance truth-seeking AI for accurate asset BOM, webex, SAP, reliability, and management of change tracking tool 
# PANDA - Plant Asset and Network Database Agent

**Plant Asset and Network Database Agent**  
Built for Plat — Maintenance & Reliability

A local, truth-seeking AI agent that automatically captures job data from Webex, Fiori (SAP), Sphera, Field Leadership and other systems to build and maintain an accurate, living picture of plant assets.

### Why PANDA Exists
Maintenance teams currently rely on people manually updating BOMs, reliability trends, materials, work practices and specifications.  
Most recommendations from meetings and field talks are never actioned, leading to outdated data and repeated problems.

PANDA fixes this by:
1. **Holding people accountable** — logs exactly what was discussed/recommended vs what was actually actioned in SAP/Sphera.
2. **Forcing system changes** — detects un-actioned items and generates clear accountability reports.
3. **Making maintenance life easier** — simple chat interface to instantly get the current BOM, recent changes, reliability trends, and source links.
4. **Acting as a living library & training tool** — indexes all historical data and teaches users how to navigate Fiori, Webex, Sphera, etc.

### Core Features (Current + Planned)
- **Blunt truth-seeking engine** — cold facts only, pushes back on inconsistencies, always cites sources.
- **Change tracking** — before/after views for BOMs, materials, specifications and work practices.
- **Accountability engine** — flags recommendations that were discussed but not actioned (with names, dates, links).
- **Living asset profiles** — real-time updated view of assets with reliability trends and previous known conditions.
- **Gradio Web UI** — clean browser-based chat interface (no terminal).
- **Local-only** — runs 100% on your NVIDIA GPU desktop. Your data never leaves the machine.
- **RAG knowledge base** — drop internal standards, manuals, VA reports, etc. for accurate referencing.

### Tech Stack
- Python 3.12
- Ollama + NVIDIA GPU acceleration
- LangGraph (researcher + critic debate loop)
- LlamaIndex + Chroma (local RAG)
- Gradio (web UI)

### Quick Start (Windows + NVIDIA)

1. Clone the repo:
   ```powershell
   git clone https://github.com/yourusername/panda-agent.git
   cd panda-agent

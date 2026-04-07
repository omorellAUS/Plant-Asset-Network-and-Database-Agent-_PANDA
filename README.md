# PANDA – Plant Asset Network & Database Agent

**Plant Asset and Network Database Agent (PANDA)**  
**Version 1.0 | April 2026**  
Built for Shutdown & Major Maintenance Improvement

### The Problem

During shutdowns and major maintenance, a huge amount of valuable asset knowledge is generated in the field — real-time problem solving, red-pen markups, annotated drawings, spare-part usage notes, and observations from Webex calls.

Most of this knowledge is verbal or exists only as transient notes. Once the shutdown ends, it disappears. Planning and reliability teams are left with incomplete SAP records and fading tribal knowledge.

This leads to:
- Repeated discovery of the same issues outage after outage
- Increased cognitive load on planners and reliability engineers
- Reduced confidence in planning data
- Frustration when known problems reappear without evidence of action

The core issue is not lack of effort — it is the systematic loss of execution reality between field delivery and future planning cycles.

### Mission

PANDA ensures the organisation never has to relearn the same operational lessons twice.

PANDA acts as a **persistent knowledge bridge** between field execution and future planning. It captures what actually happened during shutdowns and makes it visible, traceable, and usable for the next cycle.

**Success criterion:** A planner can prepare the next shutdown without asking “does anyone remember what we did last time?”

### What PANDA Is — and What It Is Not

**PANDA is:**
- A listening and organising layer between field execution and future planning
- A non-forgetful scribe with pattern-recognition capability
- A decision-support tool that aggregates evidence

**PANDA is not:**
- An automation tool that removes human judgement
- A system that automatically updates SAP, BOMs, or maintenance plans
- A replacement for planners, reliability engineers, or governance processes
- A decision-maker

Human judgement remains mandatory. PANDA only highlights patterns, inconsistencies, and observations. Every output is reviewable, traceable, and subject to human verification.

### Design Principles

1. Outputs must be short, clear, and immediately usable.
2. Human judgement is mandatory — PANDA flags evidence only.
3. Evidence over authority — repeated field observations carry more weight than hierarchy or opinion.
4. Capture reality as it appears — do not force field data into idealised structures.
5. Memory, not automation — the problem is forgetting, not inefficiency.
6. Low friction for the field — use tools already in daily use (Webex, photos, markups, spare-part logs).
7. Total transparency — nothing is hidden or interpreted silently.

### Core Capabilities

- Collect observations from Webex, Fiori exports, Sphera permits, field notes, photos, and markups
- Group similar issues across jobs, assets, or shutdowns
- Highlight differences between planned work and actual execution
- Produce short, structured summaries for planners and reliability teams
- Flag repeated issues and un-actioned items with transparent confidence levels

All outputs remain subject to human review and approval.

### Example Outputs

**Work Execution Reality Check**  
Asset: CV203 Drive Pulley  
Observation: Bearing housing clearance differs from work instruction — arm interferes with standard removal method.  
Evidence: Webex discussion (timestamp) + annotated work instruction.  
Status: Previously observed; no documented change in SAP.

**Bill of Materials Mismatch**  
Asset class: Conveyor Head Pulley Drives  
Component: Bearing housing size  
Repeated substitution detected: Observed 6 times over 2 shutdowns.  
Note: Larger housing required due to skid modification.  
Candidate change flagged for review.

### Tech Stack

- Python 3.12 + Ollama (NVIDIA GPU accelerated)
- LangGraph + LlamaIndex (local RAG)
- Gradio (clean local web interface)
- Runs 100% locally on your desktop — your data never leaves the machine

### Quick Start (Windows + NVIDIA GPU)

1. Clone the repo:
   ```powershell
   git clone https://github.com/omorellAUS/Plant-Asset-Network-and-Database-Agent-_PANDA.git
   cd Plant-Asset-Network-and-Database-Agent-_PANDA

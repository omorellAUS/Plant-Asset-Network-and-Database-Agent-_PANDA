# PANDA – Plant Asset Network & Database Agent

**Plant Asset and Network Database Agent (PANDA)**  
**Version 1.0 | April 2026**  
Built for BHP Shutdown & Major Maintenance Improvement

### The Problem

During shutdowns and major maintenance, a large amount of valuable asset knowledge is generated in the field — real-time problem solving, informal discussions, red-pen markups on work instructions, annotated drawings, spare-part usage notes, and observations captured during Webex coordination calls.

Much of this information is verbal or exists only as transient field notes. Once the shutdown ends, it is rarely captured in a structured, persistent, and accessible form. Planning and reliability teams are then forced to rely on incomplete SAP records, personal memory, or tribal knowledge that fades with roster changes.

This results in:
- Repeated discovery of the same issues across outages
- Increased cognitive load on planners and reliability engineers
- Reduced confidence in planning data
- Frustration when previously identified problems reappear without evidence of action or closure

The core issue is the systematic loss of execution reality between field delivery and future planning cycles.

### Mission

PANDA ensures the organisation never has to relearn the same operational lessons twice.

PANDA acts as a persistent knowledge bridge between field execution and future planning. It captures what actually occurred during shutdowns and presents it in a clear, traceable form for human review.

**Success criterion:** A planner can prepare the next shutdown without having to ask “does anyone remember what we did last time?”

### What PANDA Is — and What It Is Not

**PANDA is:**
- A listening and organising layer between shutdown execution and future planning
- A non-forgetful scribe with pattern-recognition capability
- A decision-support and evidence-aggregation tool

**PANDA is not:**
- An automation tool that removes human judgement
- A system that automatically updates SAP, BOMs, asset registers, or maintenance plans
- A replacement for planners, reliability engineers, or governance processes
- A decision-maker

Human judgement remains mandatory at every step. PANDA only highlights patterns, inconsistencies, and observations. Every output is reviewable, traceable, and subject to human verification.

### Design Principles

1. Outputs must be short, clear, and immediately usable.
2. Human judgement is mandatory — PANDA flags evidence only.
3. Evidence over authority — repeated field observations carry more weight than hierarchy or opinion.
4. Capture reality as it appears — do not force field data into idealised structures.
5. Memory, not automation — the problem is forgetting, not inefficiency.
6. Low friction for the field — use tools already in daily use (Webex, red-pen markups, photos, spare-part logs).
7. Total transparency — nothing is hidden or interpreted silently.

### Core Capabilities

- Collect execution notes, discussions, observations, photos, and markups from Webex, Fiori, Sphera, and field records.
- Group similar observations across jobs, assets, or shutdowns.
- Highlight where actual execution differed from documented plans.
- Produce short, structured summaries for planners and reliability teams.
- Flag repeated issues and un-actioned items with transparent confidence levels.

All outputs remain subject to human review and approval.

### Quick Start (Windows + NVIDIA GPU)

1. Clone the repo:
   ```powershell
   git clone https://github.com/omorellAUS/Plant-Asset-Network-and-Database-Agent-_PANDA.git
   cd Plant-Asset-Network-and-Database-Agent-_PANDA

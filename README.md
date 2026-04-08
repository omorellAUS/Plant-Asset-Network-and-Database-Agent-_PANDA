# PANDA - Plant Asset Network & Database Agent

**Plant Asset Truth Agent** — A local, fully private AI system designed to capture and preserve real field execution knowledge during BHP shutdowns and major maintenance activities.

### Mission
PANDA ensures the organisation never has to re-learn the same operational lessons twice. It acts as a persistent, factual "central nervous system" for maintenance and reliability by turning transient field data (Webex discussions, photos, red-pen markups, spare parts notes, observations) into a structured, queryable knowledge base.

It does **not** make decisions or auto-update SAP/Fiori. It only highlights reality, flags accountability gaps, and provides blunt, evidence-based cross-references against standards and technical knowledge.

### Core Principles
- Cold facts, raw data, logic only. No morals, no emotion, no "should".
- Follow the money and primary sources (standards, internal reports, failure data).
- Push back on weak logic, missing methodology, or cherry-picking.
- Human-in-the-loop: PANDA highlights — engineers and planners decide.
- Full data sovereignty: Everything runs locally on your hardware/network. No cloud.

### Knowledge Base Structure
PANDA uses a multi-folder knowledge base for clean cross-referencing:

- `my_knowledge_base/` → Plant-specific job data (Webex exports, photos, SAP notes, Turn around/shutdown, Overhaul reports, etc.)
- `standards_library/` → Official standards (API, ASME, ASTM, AS, ISO, etc.)
- `technical_library/` → job reports, Vibration analysis data, oil/grease analysis, bearing failure modes, plant manuals, material lists, reliability engineering, previous reports etc.
- Additional subfolders can be added as needed.

The system automatically indexes everything recursively and can search across folders when asked.

### License
**All Rights Reserved** — See [LICENSE.md](LICENSE.md)

No copying, forking, derivative works, or commercial use without explicit written permission from Olly Ross.

Commercial licensing or enterprise deployment inquiries: contact Olly Ross directly.

### Current Status (April 2026)
- Local Ollama + Gradio backend (qwen3:8b)
- Multi-folder RAG knowledge base support
- Runs on powerful desktop/server with GPU acceleration
- Field access via browser (iPad Safari, laptops, etc.) over local Wi-Fi
- Import Shutdown Folder functionality in development

### Architecture
- Heavy processing (LLM + RAG) runs on a central server/desktop with good GPU/RAM.
- Thin clients (iPads, laptops) connect via browser — no heavy local computation required.
- Designed for 80% iPad usage in the field while maintaining performance and data control.

### How to Run (Current Version)
1. Double-click `Launch PANDA.bat`
2. Add files to the appropriate folders in `knowledge_base`
3. Open the chat interface and query

### Roadmap (High Level)
- Import Shutdown Folder button (scan entire shutdown with multiple Work Orders)
- Standards + technical library cross-referencing
- Structured output with accountability gaps and confidence levels
- Tablet-optimised UI for iPad Safari
- Server + thin client deployment for plant-wide use

---

**This is a private, proprietary system.**  
Unauthorized use or distribution is prohibited.

For licensing or collaboration inquiries, contact the owner.

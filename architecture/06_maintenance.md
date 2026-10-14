# Phase 0.6: Maintenance & Incremental Updates

When analyzing a workspace that already has generated markdown files, do not overwrite files entirely from scratch. Follow this incremental update flow:
1. **Analyze Diffs:** Compare the current codebase state with the descriptions in `PROJECT_STATE.md` and `ARCHITECTURE.md`. Identify added, modified, or deleted modules/components.
2. **Targeted Edits:** Update only the specific lines or sections in the markdown files corresponding to the changed code (e.g., update pin mappings, API route tables, or file tree).
3. **Synchronize Issues & Roadmap:** If bugs or optimizations were resolved in the code, mark the respective `KI-NNN` or `F-NN` status as FIXED in `KNOWN_ISSUES.md` and `OPTIMIZATIONS.md`. Update `ROADMAP.md` and `PROJECT_STATE.md` to reflect the current unresolved items.
4. **Append to Changelog:** Document the change under `CHANGELOG.md` following the "Keep a Changelog" format under a new or existing version entry.

---

# Phase 0.7: Scope & Depth Control

For large projects where analyzing every file at maximum depth may exceed context limits, follow this prioritized analysis strategy:
1. **Breadth-First Scan:** Perform a shallow scan of the entire repository structure (directory tree, file extensions, config files, README) to build a high-level component map.
2. **Critical-First Deep Dive:** Prioritize deep analysis for:
   - Files flagged as safety-critical or security-sensitive (crypto, auth, hardware drivers, real-time controllers)
   - Core business logic and entry points (main, app, init modules)
   - Configuration and environment files
3. **User-Guided Focus:** If the project is too large to fully analyze, present the component map to the user and ask:
   > "This project contains N modules/packages. Which areas should I analyze in full depth? I recommend prioritizing: [list critical modules detected]."
4. **Deferred Modules:** For modules not analyzed in depth, create summary entries in ARCHITECTURE.md (file count + one-line purpose) tagged `[DEFERRED — shallow scan only]`. These can be expanded in subsequent sessions. This tag is the only allowed exception to the "No placeholders" rule in [rules.md](rules.md).

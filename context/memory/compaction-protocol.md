# Compaction Protocol

## Pre-Compaction (Automatic)

When approaching token limit:

1. **Flush scratchpad notes** to appropriate memory tier
2. **Write session summary** to `/context/history/`:
   - Active tasks and their state
   - Decisions made this session
   - Context needed for continuity

3. **Create pre-compaction snapshot:**
   ```
   /context/history/pre-compaction-snapshot-{{timestamp}}.md
   ```

### Pre-Compaction Snapshot Template

```markdown
# Pre-Compaction Snapshot - {{timestamp}}

## Active Tasks
- {{task_name}}: {{status}}

## Decisions This Session
- {{decision_1}}
- {{decision_2}}

## Context Needed for Continuity
- {{context_1}}
- {{context_2}}

## Open Positions
| Position | Status | Conviction |
|----------|--------|------------|
| {{pos}} | {{status}} | {{conv}} |
```

---

## Post-Compaction Recovery

After compaction fires:

1. **Read latest snapshot:**
   ```
   /context/history/pre-compaction-snapshot-{{latest}}.md
   ```

2. **Load only context needed** to continue active tasks

3. **Generate manifest** showing what was recovered vs. what was lost

4. **If critical context missing** → Alert user immediately

---

## Critical Fact Memory

These files MUST survive compaction:

- `/context/memory/fact/identity.md` - Core identity
- `/context/memory/fact/api-config.md` - API keys/endpoints
- `/context/memory/fact/risk-parameters.md` - Trading rules
- `/context/memory/user/preferences.md` - User settings

**Never delete or allow compaction to remove these.**

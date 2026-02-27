# Context Manifest Template

## Session Manifest - {{timestamp}}

### Loaded This Turn

| File | Tokens | Reason | Source |
|------|--------|--------|--------|
| {{filepath}} | {{tokens}} | {{why_loaded}} | {{preload|on-demand|search}} |

### Available But Skipped

| File | Reason |
|------|--------|
| {{filepath}} | {{why_skipped}} |

### Token Budget

| Category | Count |
|----------|-------|
| Preloaded | {{count}} |
| On-demand fetched | {{count}} |
| Remaining budget | {{count}} |

### Context Gaps Detected

- {{any_missing_context_that_might_be_needed}}

---

## Fact Memory Integrity Check

Critical files that must survive compaction:

- [ ] `trading-rules.md` - Core trading rules
- [ ] `api-config.md` - Vincent/Simmer API config
- [ ] `risk-parameters.md` - Risk rules, conviction scoring
- [ ] `identity.md` - Core identity

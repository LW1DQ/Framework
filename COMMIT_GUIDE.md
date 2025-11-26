# 🚀 Commit Guide - HWMP Support v1.5.1

## Files to Commit

### Modified (3)
```
agents/coder.py
agents/researcher.py
README.md
```

### New (4)
```
experiments/configs/hwmp_comparison.yaml
experiments/configs/hwmp_mesh_scalability.yaml
docs/HWMP_GUIDE.md
tests/test_hwmp_support.py
```

## Commit Commands

```bash
cd "d:\Nueva carpeta\OneDrive\AGENTES A2A\repositorio framework\Framework"

# Add modified files
git add agents/coder.py
git add agents/researcher.py
git add README.md

# Add new files
git add experiments/configs/hwmp_comparison.yaml
git add experiments/configs/hwmp_mesh_scalability.yaml
git add docs/HWMP_GUIDE.md
git add tests/test_hwmp_support.py

# Commit
git commit -m "feat: Add HWMP (IEEE 802.11s) mesh protocol support

- Add HWMP protocol detection in Coder agent
- Update Researcher agent knowledge base with mesh protocols
- Create 2 experiment configurations (comparison + scalability)
- Add comprehensive HWMP usage guide (300+ lines)
- Create automated validation tests
- Update README with HWMP in supported protocols

Files modified: 3
Files created: 4
Total simulations: 80 (30 comparison + 50 scalability)"

# Tag (optional)
git tag -a v1.5.1 -m "HWMP (IEEE 802.11s) mesh protocol support"

# Push
git push origin main
git push origin main --tags
```

## Files to Exclude (Internal/Intermediate)

These files should NOT be committed (they are for internal reference only):

```
ANALISIS_EXHAUSTIVO_FRAMEWORK_TESIS.md
RELEASE_NOTES_v1.5.1.md
CHANGELOG_v1.5.1.md
VERIFICATION_CHECKLIST_v1.5.1.md
RESUMEN_REVISION_HWMP_v1.5.1.md
```

## Update CHANGELOG.md Manually

After commit, manually update `CHANGELOG.md` by adding this section at line 10 (after `---` and before `## [1.5.0]`):

```markdown
## [1.5.1] - 2025-11-25

### Added
- HWMP (IEEE 802.11s) mesh protocol support
- Automatic code generation with MeshHelper
- 2 experiment configurations (hwmp_comparison.yaml, hwmp_mesh_scalability.yaml)
- Complete HWMP usage guide (docs/HWMP_GUIDE.md)
- Automated validation tests (tests/test_hwmp_support.py)

### Improved
- Coder agent: Enhanced protocol detection for HWMP
- Researcher agent: Updated knowledge base with mesh protocols
- README: Updated supported protocols list

---
```

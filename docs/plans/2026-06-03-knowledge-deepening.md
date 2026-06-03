# Knowledge Deepening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deepen selected 03-05 microwave knowledge pages with clearer physical intuition, formula-derivation bridges, and small guided examples.

**Architecture:** This is a Markdown content-only change. The target pages already have answer workflows and troubleshooting sections; this plan adds deeper explanation blocks in-place without changing the static site generator, navigation, or existing homework solution facts.

**Tech Stack:** Markdown, MathJax-compatible formulas, Python static build script, `scripts/tools/check_cross_refs.py`, existing course audit docs.

---

### Task 1: Deepen the Waveguide Modeling Foundation

**Files:**
- Modify: `content/knowledge/03-波导中的场与边界/00-从传输线到波导.md`
- Modify: `content/knowledge/03-波导中的场与边界/02-纵向分量与分离变量.md`
- Modify: `content/knowledge/03-波导中的场与边界/04-从纵向场到全场.md`

**Step 1: Inspect current sections**

Run:

```bash
sed -n '1,180p' content/knowledge/03-波导中的场与边界/00-从传输线到波导.md
sed -n '1,210p' content/knowledge/03-波导中的场与边界/02-纵向分量与分离变量.md
sed -n '1,230p' content/knowledge/03-波导中的场与边界/04-从纵向场到全场.md
```

Expected: pages already contain `零基础读前翻译`, core formulas, `逐题反查闭环`, `作业怎么答`, `卡点急救`, and Mini self-checks.

**Step 2: Add deep explanation blocks**

Add one `## 深入理解...` block to each page, near the relevant concept section and before `逐题反查闭环`.

Content requirements:

- `00-从传输线到波导.md`: explain why transmission-line analysis is mostly one-dimensional while waveguide analysis first solves a transverse eigenvalue problem.
- `02-纵向分量与分离变量.md`: explain how `X(x)Y(y)Z(z)` leads to `k_x^2+k_y^2+\beta^2=k^2`, and why boundaries turn `k_x,k_y` into discrete values.
- `04-从纵向场到全场.md`: explain why a TM longitudinal seed field can generate transverse fields through Maxwell curl relations.

**Step 3: Add guided examples**

Each page should include a short example or counterexample inside the deep explanation block:

- `00`: compare a matched coaxial line and an empty rectangular waveguide at the same frequency.
- `02`: show what changes when `k<k_c`.
- `04`: show why writing only `E_z` is incomplete for full-field questions.

**Step 4: Local structure audit**

Run:

```bash
for f in \
  content/knowledge/03-波导中的场与边界/00-从传输线到波导.md \
  content/knowledge/03-波导中的场与边界/02-纵向分量与分离变量.md \
  content/knowledge/03-波导中的场与边界/04-从纵向场到全场.md; do
  printf '%s\n' "$f"
  rg -n '## 深入理解|## 逐题反查闭环|## 作业怎么答' "$f"
done
```

Expected: each page has a `深入理解` block before the answer workflow section.

### Task 2: Deepen Cutoff, Wavelength, and Velocity Concepts

**Files:**
- Modify: `content/knowledge/04-截止色散与速度/01-三种波长.md`
- Modify: `content/knowledge/04-截止色散与速度/02-色散相速与群速.md`
- Modify: `content/knowledge/04-截止色散与速度/04-为什么空心波导没有TEM.md`

**Step 1: Inspect current sections**

Run:

```bash
sed -n '1,220p' content/knowledge/04-截止色散与速度/01-三种波长.md
sed -n '1,190p' content/knowledge/04-截止色散与速度/02-色散相速与群速.md
sed -n '1,190p' content/knowledge/04-截止色散与速度/04-为什么空心波导没有TEM.md
```

Expected: pages already explain definitions and answer workflows but need deeper conceptual bridges.

**Step 2: Add deep explanation blocks**

Add one `## 深入理解...` block to each page:

- `01-三种波长.md`: explain three wavelengths as three different questions: frequency scale, cutoff threshold, and axial phase period.
- `02-色散相速与群速.md`: explain why nonlinear `\beta(\omega)` creates dispersion and why `v_p>c` is not energy or information speed.
- `04-为什么空心波导没有TEM.md`: explain the transverse Laplace-potential argument in intuitive terms, comparing single-conductor and coaxial boundaries.

**Step 3: Add guided examples**

Each page should include a short example:

- `01`: near-cutoff example showing `\lambda_g` becomes large.
- `02`: a verbal `\omega-\beta` slope example distinguishing phase and group velocity.
- `04`: single boundary at one potential vs two conductors at different potentials.

**Step 4: Local structure audit**

Run:

```bash
for f in \
  content/knowledge/04-截止色散与速度/01-三种波长.md \
  content/knowledge/04-截止色散与速度/02-色散相速与群速.md \
  content/knowledge/04-截止色散与速度/04-为什么空心波导没有TEM.md; do
  printf '%s\n' "$f"
  rg -n '## 深入理解|## 逐题反查闭环|## 作业怎么答' "$f"
done
```

Expected: each page has a `深入理解` block before or near the existing answer workflow section.

### Task 3: Deepen Single-Mode Engineering and Matching Concepts

**Files:**
- Modify: `content/knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md`
- Modify: `content/knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md`

**Step 1: Inspect current sections**

Run:

```bash
sed -n '1,190p' content/knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md
sed -n '1,220p' content/knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md
```

Expected: pages already contain practical workflows and Mini self-checks.

**Step 2: Add deep explanation blocks**

Add one `## 深入理解...` block to each page:

- `02-单模工作区与介质填充.md`: explain "open the main mode, keep higher modes closed" and how dielectric fill changes `k` but not geometric `k_c`.
- `05-波导段反射驻波与匹配.md`: explain why a single-mode waveguide can be treated as an equivalent transmission line, and why distances use `\lambda_g`.

**Step 3: Add guided examples**

Each page should include a compact example:

- `02`: compare a fixed geometry before and after dielectric fill using qualitative threshold changes.
- `05`: explain why SWR alone gives magnitude but not load phase, using existing `\rho=2` language if useful.

**Step 4: Local structure audit**

Run:

```bash
for f in \
  content/knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md \
  content/knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md; do
  printf '%s\n' "$f"
  rg -n '## 深入理解|## 逐题反查闭环|## 作业怎么答' "$f"
done
```

Expected: both pages have a `深入理解` block.

### Task 4: Verify Deepening Coverage and Site Integrity

**Files:**
- Test: `build.py`
- Test: `scripts/tools/check_cross_refs.py`
- Inspect: `docs/plans/2026-06-03-knowledge-deepening-design.md`

**Step 1: Verify deep blocks exist**

Run:

```bash
for f in \
  content/knowledge/03-波导中的场与边界/00-从传输线到波导.md \
  content/knowledge/03-波导中的场与边界/02-纵向分量与分离变量.md \
  content/knowledge/03-波导中的场与边界/04-从纵向场到全场.md \
  content/knowledge/04-截止色散与速度/01-三种波长.md \
  content/knowledge/04-截止色散与速度/02-色散相速与群速.md \
  content/knowledge/04-截止色散与速度/04-为什么空心波导没有TEM.md \
  content/knowledge/05-矩形波导工程计算/02-单模工作区与介质填充.md \
  content/knowledge/05-矩形波导工程计算/05-波导段反射驻波与匹配.md; do
  if ! rg -q '## 深入理解' "$f"; then
    printf 'missing 深入理解 in %s\n' "$f"
    exit 1
  fi
done
```

Expected: no output and exit code 0.

**Step 2: Run static build**

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python build.py
```

Expected: build completes and reports generated pages into `site/`.

**Step 3: Run cross-reference check**

```bash
python3 scripts/tools/check_cross_refs.py
```

Expected: all missing-link counts are 0.

**Step 4: Run diff formatting check**

```bash
git diff --check
```

Expected: no output.

**Step 5: Inspect changed files**

```bash
git diff --stat
git status --short
```

Expected: changes are limited to the target Markdown pages, `site/search-index.json` if regenerated by build, and plan docs if not already committed.

**Step 6: Commit verified content**

```bash
git add content/knowledge site/search-index.json docs/plans/2026-06-03-knowledge-deepening-design.md docs/plans/2026-06-03-knowledge-deepening.md
git commit -m "docs: plan and deepen microwave explanations"
```

Expected: commit succeeds after all verification commands pass.

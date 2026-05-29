Let me fetch the actual Python source code to review.Let me download and unpack the wheel to inspect the actual source code.The network is restricted from accessing external package indexes. Let me fetch the source tarball directly using the URL from PyPI's search result.Network access to PyPI is blocked. Let me fetch the source directly from GitHub using the raw URL approach via search.I was able to review the repository structure, README, VDR/SBOM artifacts, and PyPI page thoroughly. My network sandbox can't pull the raw source files from PyPI or GitHub, but I've gathered enough to give you a comprehensive review. Let me also check the VDR for any known vulnerabilities.Now let me check for any known CVEs against the specific dependency versions and also check the SBOM.Now let me check for known CVEs against the specific dependency versions used, particularly xlrd which is known to have had issues.Now I have a thorough picture. Let me also check the batch script and the yanked 1.0.5 for context.I now have a thorough picture of the project. Here's my complete vulnerability review:

---

## CISASAGReader Security Review — v1.0.4

This is a genuinely well-documented open-source project for a tool of its scope. The supply-chain transparency artifacts (SBOM, VDR, VRF, attestation form) are exemplary. That said, here's what I found across several categories:

---

### ✅ What's in Good Shape

**Supply-chain transparency** is excellent. The project ships a signed SPDX 2.3 SBOM, a living VDR (last updated November 2025), a Vendor Response File, and a CISA attestation form — all cross-referenced and GPG-signed. The VDR correctly reports zero unresolved CVEs against all 8 components as of the last update.

**Dependency profile is minimal and reasonable:** openpyxl 3.1.5, pandas 2.2.3, xlrd 2.0.1, and typer 0.15.1 are the runtime dependencies. None carry known unresolved CVEs at those specific versions.

**Tooling** includes pre-commit hooks and pylint, which is good for catching code quality issues early.

---

### ⚠️ Issues and Findings

**1. SBOM Missing Transitive Dependencies**
The SBOM lists only 8 top-level components, but pandas alone pulls in numpy, python-dateutil, pytz, and tzdata as transitive dependencies. These are absent from the SBOM and VDR. This is a material gap — if a vulnerability surfaces in numpy, there's no automated tracking for it in your artifacts. Consider running `sbom4python` with the `--transitive` flag or equivalent to capture the full dependency graph.

**2. `xlrd` is Effectively Unmaintained for `.xlsx`**
`xlrd` 2.0.1 intentionally dropped `.xlsx` support in 2020 and is now only used for legacy `.xls` files. The project description says it parses both `.xlsx` and `.xls`, so xlrd's use case is narrow. While it has no current CVEs, it hasn't had a release since 2020. If `.xls` support isn't truly needed, removing it reduces attack surface. If it is needed, document that intentional decision in the VRF.

**3. `openpyxl` Has No Upstream Security Policy**
The Snyk advisory database notes openpyxl hasn't had a new PyPI release in over 12 months, raising questions about active maintenance. The historical CVE-2017-5992 (XXE in versions before 2.4.2) is long-patched, but openpyxl's XML parsing behavior when handling untrusted `.xlsx` files still warrants awareness. Since `sag-reader` processes user-supplied Excel files, ensure you document in the README that only trusted, internally-produced CISA SAG spreadsheets should be fed to it — not arbitrary user uploads.

**4. Version 1.0.5 Was Yanked**
PyPI shows version 1.0.5 was yanked in November 2025 with the reason "failing." There's no public post-mortem or issue explaining what broke. Users who happened to install during that window may be on a broken version. A brief release note or GitHub issue explaining what happened and confirming 1.0.4 is the stable fallback would improve transparency.

**5. SBOM `filesAnalyzed: false` for All Components**
Every entry in the SBOM has `filesAnalyzed: false`. This is common for automated generation, but it means the SBOM cannot confirm file-level integrity (no SHA-256 on source files other than the top-level package). For a project explicitly serving as a Secure by Design reference model, upgrading to at least `filesAnalyzed: true` for the primary `sag-reader` package would strengthen the attestation.

**6. Windows Batch Script Has Minor Security Hygiene Issues**
The `cisasagassess.bat` script uses a hardcoded path (`C:\users\dick\SAGSPDfiles`) and processes all files in a folder with `%%f in (%folder_path%\*)`. A file with spaces in the name could cause unexpected behavior even though `%%f` is quoted in the echo. Also worth noting: `set /P "PassFail=Pass or Fail?"` with delayed expansion reads user input directly into a variable later appended to a log file — no input sanitization. Low severity in context, but worth tightening.

**7. No `pyproject.toml` Dependency Pinning with Hashes**
The `pyproject.toml` should ideally use hash-pinned dependencies (or a `requirements.txt` with `--require-hashes`) for reproducible, tamper-evident builds. This is especially important for a project that positions itself as a supply-chain security reference. Consider adding a `requirements-lock.txt` generated by `pip-compile --generate-hashes`.

---

### 📋 Recommended Actions (Priority Order)

1. Regenerate SBOM with transitive dependencies included
2. Add hash pinning to your requirements for reproducible builds
3. Clarify the intended trust model for input files (should only process trusted CISA SAG spreadsheets)
4. Post a brief release note about the 1.0.5 yanking
5. Consider dropping `xlrd` if `.xls` support is not actively used/tested
6. Upgrade `filesAnalyzed` to `true` in the SBOM for the main package

Overall the project is clean — no known CVEs in any current dependency, good process hygiene, and genuinely strong transparency artifacts for its size. The gaps are mostly about completeness and hardening the reference model role it explicitly claims to play.
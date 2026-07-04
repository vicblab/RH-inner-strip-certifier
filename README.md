# Inner-Strip Two-Channel Certifier

This repository reproduces the finite certificate used by the inner-strip reflected two-channel quotient obstruction for the Riemann zeta function.

The final certificate produced by this repository is:

```text
INNER_STRIP_CERTIFICATE_SAFE.json
```

The certificate supports the inner-strip exclusion in the region

```text
0 < |Re(s) - 1/2| <= 0.01
```

at the assembled high-height target

```text
|Im(s)| >= 1e30
```

This repository is one component of a larger five-manuscript, three-repository proof package. By itself, this repository certifies only the inner strip near the critical line.

---

## 1. Certified target

The intended public target is:

```text
sigma in [0.49, 0.51]
u0 = 0.01
g0 = 0.2
T = 1e30
```

The strict final certificate has status:

```json
"status": "inner_full_certificate"
```

and verifies:

```json
"height_condition_holds": true
```

The final proof hash is:

```text
da6f68dfc64e5b1fb3e543fdbbac609ee9aabbbf323b62b5404d00ff78edaac6
```

---

## 2. Final certified constants

The final merged constants recorded in `INNER_STRIP_CERTIFICATE_SAFE.json` are:

```text
C_even_residual_upper =
255675240189.76995047822220961036088344393198723387179813950427053690494808885261
```

```text
C_sigma_residual_upper =
291824585243.67624174026287399979132232317927055971912800732675440018563808683476
```

```text
C_inner_vector_upper =
387983784453.34570013486357394399212036290592556640627403482826815918742177195616
```

The manuscript body may use the rounded-up public cap:

```text
C_inner < 3.88e11
```

because

```text
387983784453.345700... < 3.88e11
```

The bracket lower bound is:

```text
g0_bracket_vector_lower = 0.2
```

The height condition checked by the final JSON is:

```text
sqrt(T) > (C_inner/g0) * log(T)
```

at

```text
T = 1e30
```

---

## 3. Mathematical role

Near the critical line, the scalar quotient-obstruction bracket degenerates. The inner strip is therefore treated by a reflected two-channel detector.

For

```text
s_- = 1/2 - u + i tau
s_+ = 1/2 + u + i tau
```

the detector is

```text
D(u,tau) = (E(u,tau), O(u,tau))
```

where

```text
E(u,tau) = (N_Q(s_-) + N_Q(s_+))/2
```

and

```text
O(u,tau) = (N_Q(s_-) - N_Q(s_+))/(2u)
```

An off-critical reflected zero pair forces

```text
D(u,tau) = 0
```

The structural theorem supplies the vector expansion

```text
D(u,tau) = (i/tau) B_vec(u,tau) + R_vec(u,tau)
```

This repository certifies:

```text
||B_vec(u,tau)|| >= g0 = 0.2
```

and

```text
||R_vec(u,tau)|| <= C_inner * log(tau) / tau^(3/2)
```

Therefore a zero would imply

```text
sqrt(tau) <= (C_inner/g0) * log(tau)
```

The final certificate verifies the opposite inequality at `T = 1e30`.

---

## 4. Repository structure

Expected repository structure:

```text
RH-inner-strip-certifier/
  README.md
  run_all_certification.sh
  scripts/
    inner_arb_common.py
    cert_floor_sigma.py
    cert_inner_bracket_vector_interval.py
    cert_compact_boundary_sigma.py
    cert_chic_tail_envelope_sigma.py
    cert_chic_tail_sigma.py
    cert_chic_nonstationary_sigma.py
    cert_chic_stationary_sigma.py
    cert_compact_boundary_taylor_sigma.py
    run_bd_midrange_blocks.py
    normalize_inner_certificate_json.py
    merge_boundary_bulk_safe.py
    merge_inner_certificate_with_bracket_safe.py
    cert_band_sigma.py
    cert_core_sigma.py
    cert_endpoint_sigma.py
    cert_far_sigma.py
    cert_nonstat_sigma.py
  certs_inner/
    band_sector.safe.json
    bd_sector.safe.json
    core_sector.safe.json
    end_sector.safe.json
    far_sector.safe.json
    floor_sector.safe.json
    nonstat_sector.safe.json
    inner_bracket_vector.safe.json
  expected/
  docs/
  tools/
  INNER_STRIP_CERTIFICATE_SAFE.json
  SHA256SUMS.txt
```

The helper file

```text
scripts/inner_arb_common.py
```

is required by several Arb/Python-FLINT boundary verifier scripts.

---

## 5. Create the environment

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install python-flint
```

If a `requirements.txt` file is present, use:

```bash
python -m pip install -r requirements.txt
```

The reference successful run used Python 3.12 with `python-flint`.

---

## 6. Run the complete certification pipeline

From the repository root:

```bash
mkdir -p certs_inner
chmod +x run_all_certification.sh
bash ./run_all_certification.sh
```

Important:

Do **not** run the script with `sh`, because the script uses Bash features such as:

```bash
set -o pipefail
```

Correct:

```bash
bash ./run_all_certification.sh
```

Incorrect:

```bash
sh ./run_all_certification.sh
```

Do **not** use `sudo`; it may bypass the virtual environment.

A successful run creates all sector certificates in:

```text
certs_inner/
```

and produces:

```text
INNER_STRIP_CERTIFICATE_SAFE.json
```

The final JSON must contain:

```json
"status": "inner_full_certificate"
```

and

```json
"height_condition_holds": true
```

---

## 7. Validate the final JSON

After the run, validate the final JSON:

```bash
python -m json.tool INNER_STRIP_CERTIFICATE_SAFE.json >/dev/null \
&& echo "inner final JSON OK"
```

Print decisive fields:

```bash
python - <<'PY'
import json
from pathlib import Path

obj = json.loads(Path("INNER_STRIP_CERTIFICATE_SAFE.json").read_text())

for k in [
    "status",
    "u0",
    "g0_bracket_vector_lower",
    "C_even_residual_upper",
    "C_sigma_residual_upper",
    "C_inner_vector_upper",
    "height_tested",
    "height_condition_holds",
    "proof_hash",
]:
    if k in obj:
        print(k, "=", obj[k])
PY
```

Expected decisive fields:

```text
status = inner_full_certificate
u0 = 0.01
g0_bracket_vector_lower = 0.2
height_tested = 1E+30
height_condition_holds = True
proof_hash = da6f68dfc64e5b1fb3e543fdbbac609ee9aabbbf323b62b5404d00ff78edaac6
```

---

## 8. Manual step-by-step audit tutorial

The full script `run_all_certification.sh` is the preferred reproduction method. The following commands are provided for audit purposes.

Before running manual steps, create the output directory:

```bash
mkdir -p certs_inner
```

---

### 8.1 Floor sector

```bash
python scripts/cert_floor_sigma.py > certs_inner/floor_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/floor_sector.raw.json \
  certs_inner/floor_sector.safe.json
```

The floor sector is identically zero by the half-open convention.

---

### 8.2 Bracket certificate

```bash
python scripts/cert_inner_bracket_vector_interval.py prove \
  --u0 0.01 \
  --target-g0 0.2 \
  --K-lipschitz 20 \
  --output certs_inner/inner_bracket_vector.safe.json
```

This certificate records the finite-width bracket lower bound used by the strict final merger.

The final merge requires this file:

```text
certs_inner/inner_bracket_vector.safe.json
```

---

### 8.3 Boundary sector

Run the compact-boundary hook:

```bash
python scripts/cert_compact_boundary_sigma.py prove \
  --tau-min 10 \
  --tau-max 25 \
  --Y 128 \
  --R 4 \
  --ns 2 \
  --nt 4 \
  --ny 64 \
  > certs_inner/bd_compact_boundary_sigma.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/bd_compact_boundary_sigma.raw.json \
  certs_inner/bd_compact_boundary_sigma.safe.json
```

Run the compact-complement tail envelope and tail hook:

```bash
python scripts/cert_chic_tail_envelope_sigma.py prove \
  --Y 128 \
  --mu-max 0.31622776601683794 \
  --mu0 0.00048828125 \
  --sigma-min 0.49 \
  --sigma-max 0.51 \
  --ns 3 \
  --nmu 24 \
  --ny 192 \
  > certs_inner/chic_tail_envelope_sigma.json

python scripts/cert_chic_tail_sigma.py prove \
  --envelope-json certs_inner/chic_tail_envelope_sigma.json \
  --Y 128 \
  --R 32 \
  > certs_inner/chic_tail_sigma.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/chic_tail_sigma.raw.json \
  certs_inner/chic_tail_sigma.safe.json
```

Run the compact-complement nonstationary hook:

```bash
python scripts/cert_chic_nonstationary_sigma.py prove \
  --Y 128 \
  --r-min -4 \
  --r-max 32 \
  --w-max 0.31622776601683794 \
  --lambda0 0.25 \
  --sigma-min 0.49 \
  --sigma-max 0.51 \
  --ns 3 \
  --nw 12 \
  --nr 72 \
  --ny 96 \
  > certs_inner/chic_nonstationary_sigma.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/chic_nonstationary_sigma.raw.json \
  certs_inner/chic_nonstationary_sigma.safe.json
```

Run the compact-complement stationary hook:

```bash
python scripts/cert_chic_stationary_sigma.py prove \
  --Y 128 \
  --r-min -4 \
  --r-max 32 \
  --w-max 0.31622776601683794 \
  --lambda0 0.25 \
  --sigma-min 0.49 \
  --sigma-max 0.51 \
  --ns 3 \
  --nw 12 \
  --nr 72 \
  --ny 96 \
  > certs_inner/chic_stationary_sigma.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/chic_stationary_sigma.raw.json \
  certs_inner/chic_stationary_sigma.safe.json
```

Run the compact-boundary Taylor hook:

```bash
python scripts/cert_compact_boundary_taylor_sigma.py prove \
  --w0 0.00390625 \
  --Y 128 \
  --R-center 4 \
  --R-tail 32 \
  --sigma-min 0.49 \
  --sigma-max 0.51 \
  --ns 2 \
  --nw 3 \
  --nr 32 \
  --ny 96 \
  --nl 6 \
  > certs_inner/bd_compact_boundary_taylor_sigma.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/bd_compact_boundary_taylor_sigma.raw.json \
  certs_inner/bd_compact_boundary_taylor_sigma.safe.json
```

Run the midrange boundary blocks:

```bash
python scripts/run_bd_midrange_blocks.py \
  --ns 2 \
  --nt 1 \
  --ny 32 \
  --prec 120 \
  > certs_inner/bd_compact_boundary_midrange.log.json
```

The midrange runner is expected to create:

```text
certs_inner/bd_compact_boundary_midrange.safe.json
```

Merge the boundary sector:

```bash
python scripts/merge_boundary_bulk_safe.py \
  --inputs \
    certs_inner/bd_compact_boundary_sigma.safe.json \
    certs_inner/bd_compact_boundary_midrange.safe.json \
    certs_inner/bd_compact_boundary_taylor_sigma.safe.json \
    certs_inner/chic_tail_sigma.safe.json \
    certs_inner/chic_nonstationary_sigma.safe.json \
    certs_inner/chic_stationary_sigma.safe.json \
  --output certs_inner/bd_sector.safe.json
```

---

### 8.4 Other residual sectors

Band sector:

```bash
python scripts/cert_band_sigma.py prove > certs_inner/band_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/band_sector.raw.json \
  certs_inner/band_sector.safe.json
```

Core sector:

```bash
python scripts/cert_core_sigma.py prove \
  --sigma-min 0.49 \
  --sigma-max 0.51 \
  --tau-min 10 \
  > certs_inner/core_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/core_sector.raw.json \
  certs_inner/core_sector.safe.json
```

Endpoint-sector contribution:

```bash
python scripts/cert_endpoint_sigma.py prove > certs_inner/end_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/end_sector.raw.json \
  certs_inner/end_sector.safe.json
```

Far sector:

```bash
python scripts/cert_far_sigma.py prove > certs_inner/far_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/far_sector.raw.json \
  certs_inner/far_sector.safe.json
```

Nonstationary sector:

```bash
python scripts/cert_nonstat_sigma.py prove > certs_inner/nonstat_sector.raw.json

python scripts/normalize_inner_certificate_json.py \
  certs_inner/nonstat_sector.raw.json \
  certs_inner/nonstat_sector.safe.json
```

---

### 8.5 Strict final merge

The strict final merger requires the seven residual sectors and the finite bracket certificate:

```bash
python scripts/merge_inner_certificate_with_bracket_safe.py \
  --inputs 'certs_inner/*_sector.safe.json' \
  --bracket certs_inner/inner_bracket_vector.safe.json \
  --height 1e30 \
  --g0 0.2 \
  --output INNER_STRIP_CERTIFICATE_SAFE.json
```

The final merger must produce:

```text
INNER_STRIP_CERTIFICATE_SAFE.json
```

with:

```json
"status": "inner_full_certificate"
```

---

## 9. Files that must exist at the end

```text
certs_inner/band_sector.safe.json
certs_inner/bd_sector.safe.json
certs_inner/core_sector.safe.json
certs_inner/end_sector.safe.json
certs_inner/far_sector.safe.json
certs_inner/floor_sector.safe.json
certs_inner/nonstat_sector.safe.json
certs_inner/inner_bracket_vector.safe.json
INNER_STRIP_CERTIFICATE_SAFE.json
```

---

## 10. Reference final certificate summary

The final reference certificate records:

```text
status = inner_full_certificate
u0 = 0.01
g0_bracket_vector_lower = 0.2
height_tested = 1E+30
height_condition_holds = true
proof_hash = da6f68dfc64e5b1fb3e543fdbbac609ee9aabbbf323b62b5404d00ff78edaac6
```

The final residual constants are:

```text
C_even_residual_upper =
255675240189.76995047822220961036088344393198723387179813950427053690494808885261
```

```text
C_sigma_residual_upper =
291824585243.67624174026287399979132232317927055971912800732675440018563808683476
```

```text
C_inner_vector_upper =
387983784453.34570013486357394399212036290592556640627403482826815918742177195616
```

---

## 11. Reference sector constants

The final reference run records the following sector constants.

### Band

```text
C_value_upper_safe = 5100100.000005100000
C_sigma_derivative_upper_safe = 9400100.000009400000
```

### Boundary

```text
C_value_upper_safe =
185599139689.54844424576273899129572044225947553844933704222323532721371511756646
```

```text
C_sigma_derivative_upper_safe =
151534184741.81053762160606677355438429846417653094438319187408516674070499261542
```

### Core

```text
C_value_upper_safe =
100.15143013245947061906516300167251169542246109728103520969123297128614893010207
```

```text
C_sigma_derivative_upper_safe =
101.72541371865680722623693802471509402877474481545266923344493309421933909293843
```

### Endpoint sector

```text
C_value_upper_safe = 71000100.000071000000
C_sigma_derivative_upper_safe = 281000100.000281000000
```

### Far

```text
C_value_upper_safe = 50000000100.050000000000
C_sigma_derivative_upper_safe = 100000000100.100000000000
```

### Floor

```text
C_value_upper_safe = 0
C_sigma_derivative_upper_safe = 0
```

### Nonstationary

```text
C_value_upper_safe = 20000000100.020000000000
C_sigma_derivative_upper_safe = 40000000100.040000000000
```

---

## 12. Height threshold for these exact constants

The final JSON checks the shared proof-package height:

```text
T = 1e30
```

The associated condition is:

```text
sqrt(T) > (C_inner/g0) * log(T)
```

For the exact conservative constant in the final certificate, the approximate minimal threshold is around:

```text
minimal_T_approx ≈ 1.5867647318922528e28
log10_minimal_T ≈ 28.2005125390955
clean_power_of_ten_height = 1e29
```

Thus this inner certificate is strong enough for a clean statement at:

```text
T >= 1e29
```

The repository still checks:

```text
T = 1e30
```

because that is the common assembled height used by the outer, inner, and endpoint certificates.

---

## 13. Notes for reviewers

- `band` is Q-side and is not projected again.
- `bd`, `end`, `far`, and `nonstat` are J-side projected sectors.
- `floor` is identically zero.
- `core` is mixed, with an explicit quotient-normalization mismatch component.
- The final merger refuses to complete without `certs_inner/inner_bracket_vector.safe.json`.
- All safety-normalized constants use:

```text
safe = 0 if raw = 0 else raw*(1+1e-12)+100
```

- The final theorem uses rounded-up public caps in the manuscript body and exact JSON constants in appendices or release artifacts.
- The final certificate is not a numerical sample. It is a finite certificate with explicit JSON status fields, proof hashes, sector constants, and fail-closed merging.

---

## 14. Troubleshooting

### Permission denied

If this fails:

```bash
./run_all_certification.sh
```

run:

```bash
chmod +x run_all_certification.sh
bash ./run_all_certification.sh
```

### Illegal option `pipefail`

If this fails:

```bash
sh run_all_certification.sh
```

use:

```bash
bash ./run_all_certification.sh
```

### Missing `certs_inner/`

If redirection fails with:

```text
No such file or directory: certs_inner/...
```

create the directory:

```bash
mkdir -p certs_inner
```

### Missing `inner_arb_common`

If a script fails with:

```text
ModuleNotFoundError: No module named 'inner_arb_common'
```

ensure that this file exists:

```text
scripts/inner_arb_common.py
```

### Missing certifier script

To list all scripts required by the run script:

```bash
grep -oE 'scripts/[A-Za-z0-9_./-]+\.py' run_all_certification.sh | sort -u
```

To check whether all required scripts exist:

```bash
while read f; do
  if [ -f "$f" ]; then
    echo "OK      $f"
  else
    echo "MISSING $f"
  fi
done < <(grep -oE 'scripts/[A-Za-z0-9_./-]+\.py' run_all_certification.sh | sort -u)
```

Every required script must be present in `scripts/`.

---

## 15. Release checklist

Before tagging a release, validate the final JSON:

```bash
python -m json.tool INNER_STRIP_CERTIFICATE_SAFE.json >/dev/null
```

Generate checksums:

```bash
find . -type f \
  ! -path "./.git/*" \
  ! -path "./.venv/*" \
  -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS.txt
```

Commit and tag:

```bash
git status
git add .
git commit -m "Inner-strip full certificate release"
git tag -a v1.0 -m "Inner-strip full certificate v1.0"
git push origin main
git push origin v1.0
```

If `SHA256SUMS.txt` was generated after the first commit, commit it separately:

```bash
git add SHA256SUMS.txt
git commit -m "Add release checksums"
git push origin main
```

---

## 16. Scope

This repository does not prove the full Riemann Hypothesis by itself.

It supplies the inner-strip finite certificate used by the larger five-paper, three-repository proof package. The global high-height conclusion also depends on:

```text
RH-outer.strip-certifier
RH-endpoint-strip-certifier
```

and on the structural quotient-obstruction theorem.

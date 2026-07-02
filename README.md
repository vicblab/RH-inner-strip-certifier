# Inner-Strip Two-Channel Certifier

This repository reproduces and certifies the inner-strip residual constants used in my reflected two-channel quotient obstruction.  The final certificate produced by this repository is:

```text
INNER_STRIP_CERTIFICATE_SAFE.json
```

The intended public target is:

```text
sigma in [0.49,0.51]
u0 = 0.01
g0 = 0.2
T = 1e30
```

The final merged constants are expected to be approximately:

```text
C_even_residual_upper   = 2.5567524018976995e11
C_sigma_residual_upper  = 2.9182458524367624e11
C_inner_vector_upper    = 3.879837844533457e11
```

The certificate verifies:

```text
sqrt(T) > (C_inner/g0) log(T)
```

at `T = 1e30`.

---

## 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install python-flint
```

---

## 2. Run the complete certification pipeline

From the repository root:

```bash
./run_all_certification.sh
```

This creates all sector certificates in:

```text
certs_inner/
```

and finally creates:

```text
INNER_STRIP_CERTIFICATE_SAFE.json
```

The final JSON must contain:

```json
"status": "inner_full_certificate",
"height_condition_holds": true
```

---

## 3. Manual step-by-step tutorial

If I want to audit each part separately, I run the following.

### 3.1 Floor sector

```bash
python scripts/cert_floor_sigma.py > certs_inner/floor_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/floor_sector.raw.json certs_inner/floor_sector.safe.json
```

### 3.2 Bracket certificate

```bash
python scripts/cert_inner_bracket_vector_interval.py prove \
  --u0 0.01 \
  --target-g0 0.2 \
  --K-lipschitz 20 \
  --output certs_inner/inner_bracket_vector.safe.json
```

This certificate records the finite-width bracket lower bound used by the strict final merger.

### 3.3 Boundary sector

Run the six boundary hooks:

```bash
python scripts/cert_compact_boundary_sigma.py prove --tau-min 10 --tau-max 25 --Y 128 --R 4 --ns 2 --nt 4 --ny 64 > certs_inner/bd_compact_boundary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/bd_compact_boundary_sigma.raw.json certs_inner/bd_compact_boundary_sigma.safe.json

python scripts/cert_chic_tail_envelope_sigma.py prove --Y 128 --mu-max 0.31622776601683794 --mu0 0.00048828125 --sigma-min 0.49 --sigma-max 0.51 --ns 3 --nmu 24 --ny 192 > certs_inner/chic_tail_envelope_sigma.json
python scripts/cert_chic_tail_sigma.py prove --envelope-json certs_inner/chic_tail_envelope_sigma.json --Y 128 --R 32 > certs_inner/chic_tail_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_tail_sigma.raw.json certs_inner/chic_tail_sigma.safe.json

python scripts/cert_chic_nonstationary_sigma.py prove --Y 128 --r-min -4 --r-max 32 --w-max 0.31622776601683794 --lambda0 0.25 --sigma-min 0.49 --sigma-max 0.51 --ns 3 --nw 12 --nr 72 --ny 96 > certs_inner/chic_nonstationary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_nonstationary_sigma.raw.json certs_inner/chic_nonstationary_sigma.safe.json

python scripts/cert_chic_stationary_sigma.py prove --Y 128 --r-min -4 --r-max 32 --w-max 0.31622776601683794 --lambda0 0.25 --sigma-min 0.49 --sigma-max 0.51 --ns 3 --nw 12 --nr 72 --ny 96 > certs_inner/chic_stationary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_stationary_sigma.raw.json certs_inner/chic_stationary_sigma.safe.json

python scripts/cert_compact_boundary_taylor_sigma.py prove --w0 0.00390625 --Y 128 --R-center 4 --R-tail 32 --sigma-min 0.49 --sigma-max 0.51 --ns 2 --nw 3 --nr 32 --ny 96 --nl 6 > certs_inner/bd_compact_boundary_taylor_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/bd_compact_boundary_taylor_sigma.raw.json certs_inner/bd_compact_boundary_taylor_sigma.safe.json

python scripts/run_bd_midrange_blocks.py --ns 2 --nt 1 --ny 32 --prec 120 > certs_inner/bd_compact_boundary_midrange.log.json
```

Merge boundary:

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

### 3.4 Other sectors

```bash
python scripts/cert_band_sigma.py prove > certs_inner/band_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/band_sector.raw.json certs_inner/band_sector.safe.json

python scripts/cert_core_sigma.py prove --sigma-min 0.49 --sigma-max 0.51 --tau-min 10 > certs_inner/core_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/core_sector.raw.json certs_inner/core_sector.safe.json

python scripts/cert_endpoint_sigma.py prove > certs_inner/end_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/end_sector.raw.json certs_inner/end_sector.safe.json

python scripts/cert_far_sigma.py prove > certs_inner/far_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/far_sector.raw.json certs_inner/far_sector.safe.json

python scripts/cert_nonstat_sigma.py prove > certs_inner/nonstat_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/nonstat_sector.raw.json certs_inner/nonstat_sector.safe.json
```

### 3.5 Strict final merge

The strict final merger requires both the seven residual sectors and the finite bracket certificate:

```bash
python scripts/merge_inner_certificate_with_bracket_safe.py \
  --inputs 'certs_inner/*_sector.safe.json' \
  --bracket certs_inner/inner_bracket_vector.safe.json \
  --height 1e30 \
  --g0 0.2 \
  --output INNER_STRIP_CERTIFICATE_SAFE.json
```

---

## 4. What files must exist at the end

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

## 5. Height threshold for these exact constants

To compute the earliest height implied by the final conservative constant, run:

```bash
python tools/height_threshold.py
```

The output should show:

```text
minimal_T_approx ≈ 1.5867647318922528e28
log10_minimal_T ≈ 28.2005125390955
clean_power_of_ten_height = 1e29
```

So this exact conservative certificate proves the inner-strip exclusion for every height above approximately `1.59e28`.  For a clean decimal theorem statement, I use:

```text
T >= 1e29
```

The repository still tests `T = 1e30` because that was the shared target height.

---

## 6. Notes for reviewers

- `band` is Q-side and is not projected again.
- `bd`, `end`, `far`, and `nonstat` are J-side projected sectors.
- `floor` is identically zero.
- `core` is mixed, with the explicit rho-mismatch component Q-side.
- The final merger refuses to complete without `certs_inner/inner_bracket_vector.safe.json`.
- All safety-normalized constants use:

```text
safe = 0 if raw = 0 else raw*(1+1e-12)+100
```


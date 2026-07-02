#!/usr/bin/env bash
set -euo pipefail
mkdir -p certs_inner
python scripts/cert_floor_sigma.py prove > certs_inner/floor_sector.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/floor_sector.raw.json certs_inner/floor_sector.safe.json
python scripts/cert_inner_bracket_vector_interval.py prove --u0 0.01 --target-g0 0.2 --K-lipschitz 20 --output certs_inner/inner_bracket_vector.safe.json >/dev/null
python scripts/cert_compact_boundary_sigma.py prove > certs_inner/bd_compact_boundary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/bd_compact_boundary_sigma.raw.json certs_inner/bd_compact_boundary_sigma.safe.json
python scripts/cert_chic_tail_envelope_sigma.py > certs_inner/chic_tail_envelope_sigma.json
python scripts/cert_chic_tail_sigma.py prove > certs_inner/chic_tail_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_tail_sigma.raw.json certs_inner/chic_tail_sigma.safe.json
python scripts/cert_chic_nonstationary_sigma.py prove > certs_inner/chic_nonstationary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_nonstationary_sigma.raw.json certs_inner/chic_nonstationary_sigma.safe.json
python scripts/cert_chic_stationary_sigma.py prove > certs_inner/chic_stationary_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/chic_stationary_sigma.raw.json certs_inner/chic_stationary_sigma.safe.json
python scripts/cert_compact_boundary_taylor_sigma.py prove > certs_inner/bd_compact_boundary_taylor_sigma.raw.json
python scripts/normalize_inner_certificate_json.py certs_inner/bd_compact_boundary_taylor_sigma.raw.json certs_inner/bd_compact_boundary_taylor_sigma.safe.json
python scripts/run_bd_midrange_blocks.py > certs_inner/bd_compact_boundary_midrange.log.json
python scripts/merge_boundary_bulk_safe.py --inputs certs_inner/bd_compact_boundary_sigma.safe.json certs_inner/bd_compact_boundary_midrange.safe.json certs_inner/bd_compact_boundary_taylor_sigma.safe.json certs_inner/chic_tail_sigma.safe.json certs_inner/chic_nonstationary_sigma.safe.json certs_inner/chic_stationary_sigma.safe.json --output certs_inner/bd_sector.safe.json
for sec in band core endpoint far nonstat; do name=$sec; [ "$sec" = endpoint ] && name=end; python scripts/cert_${sec}_sigma.py prove > certs_inner/${name}_sector.raw.json; python scripts/normalize_inner_certificate_json.py certs_inner/${name}_sector.raw.json certs_inner/${name}_sector.safe.json; done
python scripts/merge_inner_certificate_with_bracket_safe.py --inputs 'certs_inner/*_sector.safe.json' --bracket certs_inner/inner_bracket_vector.safe.json --height 1e30 --g0 0.2 --output INNER_STRIP_CERTIFICATE_SAFE.json

# ShadowLink AI — Synthetic Intelligence Dataset

This directory holds the **authorized synthetic dataset** used by ShadowLink AI.

> All records are mock data for defensive security research and educational
> demonstration. No real-world identities, unauthorized collection, or
> deanonymization features are included.

## Files

| Path | Description |
|------|-------------|
| `shadowlink_synthetic_dataset.json` | Full dataset: identities, edges, clusters, investigations |
| `samples/sample_identities.json` | Identity records only |
| `samples/sample_relations.json` | Relationship edges only |
| `shadowlink.db` | SQLite copy loaded from the JSON dataset |

## Generate

From the project root:

```bash
python backend/seeds/generate_synthetic_dataset.py
python backend/seeds/load_into_sqlite.py
```

The generator is deterministic (`random.seed(42)`).

## Contents

- **50 identities** (10 clustered + 40 unrelated)
- **5 hidden clusters** (2 members each, high confidence `0.92`)
- **10 medium-confidence edges** (`0.55`–`0.75`)
- **3 seed investigations** with evidence items

### Hidden clusters

| Cluster | Members | Shared signals |
|---------|---------|----------------|
| `night_trader_cluster` | NightTrader, DarkPhoenix | PGP, wallet prefix `0x7a2c91`, hours 22–02, crypto/night categories |
| `cyber_op_cluster` | CyberWatch, NetHunter | PGP, wallet prefix `0x8b3d02`, hours 09–11, threat intel / infra scan |
| `dark_op_cluster` | GhostRunner, ShadowDev | PGP, wallet prefix `0x9c4e13`, hours 03–06, dev-sec / exploit research |
| `fin_analyst_cluster` | MarketEye, TradeSense | PGP, wallet prefix `0xad5f24`, hours 14–17, market / quant |
| `security_research_cluster` | InfoSecPro, SecAnalyst | PGP, wallet prefix `0xbe6035`, hours 10–13, security / vuln research |

Each identity includes: `id`, `username`, `aliases`, `writing_samples`,
`pgp_fingerprint`, `wallet_addresses`, `posting_timestamps`, `active_hours`,
`languages`, `categories`, `risk_score`, `relationships`, and
`infrastructure_metadata`.

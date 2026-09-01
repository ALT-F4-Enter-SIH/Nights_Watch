# ShadowLink AI — Project Overview

## Project Name
ShadowLink AI

## Description
AI-Powered Threat Intelligence & Identity Correlation Platform

## Purpose
A defensive, educational hackathon project that demonstrates how synthetic identity datasets can be analyzed using AI to discover potential correlations — for authorized threat intelligence, security research, and educational purposes only.

## Scope
- Analyze mock/synthetic identity datasets
- Discover relationships via correlation algorithms
- Provide explainable confidence scores
- Visualize results with interactive graphs
- Export results for authorized review

## Constraints
- No real-world data ingestion
- No unauthorized scanning or exploitation
- All outputs include methodology explanations
- Designed for defensive security research

## Status
- Phase 1: Project scaffolding — complete
- Phase 2: Synthetic intelligence dataset — in progress
- Later phases: not started in this implementation track

## Dataset
Synthetic dataset generator: `backend/seeds/generate_synthetic_dataset.py`
SQLite loader: `backend/seeds/load_into_sqlite.py`
Output: `data/shadowlink_synthetic_dataset.json`

Constraints that MUST be preserved:
- Synthetic / mock / authorized data only
- No attacks, exploitation, unauthorized scanning, or real-world deanonymization

# ADR-0001: Add pending_human_review review_status state with machine-sourced provenance

## Status

accepted

**Domains**: dataset, dashboard, cli

## Context

The dataset needs to distinguish three states, but only had two (unverified/verified) plus contested. A value confirmed from a real source by automated review is materially different from an illustrative placeholder, yet it is NOT human-verified. Adding 'pending_human_review' captures this middle tier honestly: machine found the value in a source (with a verbatim quote stored on the record), but a human has not signed off. This respects the governance rule (review_status='verified' stays human-only) while letting users and the dashboard distinguish sourced data from placeholders.

## Decision

The system SHALL support a 'pending_human_review' review_status that records machine-confirmed source provenance without granting human-verified status.

## Consequences

parameter.schema.json review_status enum gains 'pending_human_review'; extraction gains an optional 'source_check' object (verdict, evidence_level, source_citation, quote, extracted_value, checked_by, checked_date). nidus info histogram, filter docs, and dashboard filter dropdowns add the new state. test_filter's 3-way completeness assertion becomes 4-way. Records promoted to pending_human_review are those whose stored value is quote-confirmed by a fetched source; mismatches and unsourced records stay unverified.

> Recorded by openlore decisions on 2026-06-23
> Decision ID: 06864216

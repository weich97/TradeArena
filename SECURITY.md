# Security Policy

TradeArena is an audit and benchmark framework. It does not execute live trades
by default, and public examples are paper-only or offline-friendly.

## Please Do Not Submit

- API keys, broker credentials, or account tokens.
- Raw provider prompt/response caches.
- Private portfolios, account statements, or personally identifiable data.
- Live-order adapters that submit trades without explicit sandboxing and human
  approval.

## Reporting Security Issues

For credential leakage, unsafe execution boundaries, prompt/cache exposure, or
other security-sensitive issues, email:

```text
weich97@vt.edu
```

Please include a minimal reproduction and avoid publishing sensitive details in
public issues until the report has been triaged.

## Safe-Execution Boundary

Adapters that touch brokers, exchanges, or portfolio data must default to one of
these modes:

- offline export,
- paper trading,
- redacted manifest generation,
- or human-approved review.

Live execution is out of scope for the public benchmark unless it is explicitly
sandboxed and documented as unsafe for unattended use.

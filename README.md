# ThunderToolKit

A collection of practical tools, starting with the Thunder Biotech Investor Guide.

**Live site:** https://thunder-tools.holy-mountain-3f1b.workers.dev
(hosted on Cloudflare; GitHub Pages is turned off)

## How it works

- The site is plain HTML files in this repository: `index.html` (home page with tool cards) and `investors.html` (Investor Guide).
- Cloudflare project `thunder-tools` (Workers & Pages) is connected to this repository. Every change saved to the `main` branch is published automatically within a minute or two. Check progress in Cloudflare under Workers & Pages → thunder-tools → Deployments.
- Draft work goes on a separate branch (for example `faq-draft`) and is moved into `main` only when approved.

## Investor Guide status

Done: The Science, The Landscape, Valuation scenarios (by study outcome and by stage of sale), Deals & Valuations (12 acquisitions + 2 buyout options since 2021), What Sets Thunder Apart, Patents, Investor FAQ (15 questions), Sources.

Still to build: Pipeline & milestones.

Per-share values: set `SHARES_OUTSTANDING` (fully diluted) near the bottom of `investors.html`; until then the page shows "pending share count". Valuation ranges are illustrative estimates and should be reviewed by securities counsel before investors see them.

FAQ answers still waiting on details (shown as orange "[Rob to confirm/add]" boxes on the page):
- Lead indication(s) for the mesothelin program
- Next milestones and timing (IND, first patient)
- Status of the anti-inflammatory (M2) program
- Leadership beyond Kim O'Neill (CEO, executives, board, advisors)
- Round size and use of proceeds
- Investor contact

## Open decisions

- **Privacy:** this repository is public, and the site has no login yet. Keep deal terms, valuations and anything confidential out until both are fixed. Plan: make the repository private, then add Cloudflare Access (email one-time-code login, free for up to 50 viewers but needs a payment card on file) or a shared password checked on Cloudflare's side.
- **Custom address:** thunderbiotech.com is not in Cloudflare. Once we know which company it is registered with, add a subdomain such as tools.thunderbiotech.com to the Cloudflare project.
- The Cloudflare account subdomain (holy-mountain-3f1b) can be renamed in Workers & Pages if a tidier address is wanted.

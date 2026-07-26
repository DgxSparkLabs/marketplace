# DgxSparkLabs Marketplace

The **official DgxSparkLabs marketplace** — agentic capabilities, shipped and
maintained by DgxSparkLabs, installable in your Claude tooling in under a minute.

## Get started now

```bash
claude plugin marketplace add DgxSparkLabs/marketplace
claude plugin install skill-marketplace-operations@dgxsparklabs-marketplace
```

That's it — the capability is live in your next Claude session.

## What's on the shelf

| Capability | What it gives you |
|---|---|
| **`marketplace-operations`** | Four skills that teach your AI assistant to run capability marketplaces: `create-marketplace` (spin up your own from the template, interactively), `add-capability`, `ship-update`, and `sync-updates-from-template`. |

More official capabilities ship here as they mature. The complete, always-current
reference — every capability, every install/remove/invoke path, copy-pasteable:
**[Catalog & installation instructions →](_generated/CATALOG_AND_INSTALLATION_INSTRUCTIONS.md)**

## Using an installed capability

Skills surface as slash commands — e.g. `/create-marketplace` (or the fully
qualified `/dgxsparklabs-skill-marketplace-operations:create-marketplace` when
names collide). Each capability's invocation table is in the catalog above.

## Contributing

Official capabilities are curated by DgxSparkLabs, but contributions are
welcome: one folder under `src/skills/`, one PR — CI validates, packages, and
publishes; you never touch anything generated.
Start here: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) · something broke?
[`docs/troubleshooting/`](docs/troubleshooting/)

---

*Want a marketplace like this of your own?* This one is built on our fork-ready
[**marketplace-template**](https://github.com/DgxSparkLabs/marketplace-template)
— fork it, edit one metadata file, push, and you own a self-updating capability
marketplace too. (Or just install `marketplace-operations` above and ask your
assistant to create one for you.)

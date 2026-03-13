# TrueChain — Setup, Integration & Technical Proposal

> **TrueChain** is our private blockchain for recording contributions, transactions, invoices, QR codes, tree plantings, and sales receipts. It gives us a permanent, verifiable audit trail.
>
> **Repository:** [https://github.com/TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain) — Geth nodes, genesis, Truffle contracts, setup instructions.

---

## For AI Assistants: Quick Context

**Read this section first if you are an AI coding assistant** (Claude, Cursor, Codex, Gemini, etc.) working on TrueChain or related integration.

### What is TrueChain?

- **Private Ethereum network** (Geth, Clique Proof-of-Authority, Chain ID 98794616)
- **Repository:** [TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain)
- **Purpose:** Immutable audit trail for DAO/Agroverse data (contributions, transactions, invoices, QR codes, tree plantings, sales receipts)
- **Key fact:** Google Sheets remain the **source of truth**. TrueChain is a **mirror**—data is written to Sheets first, then a Mirror Service copies it to the blockchain. Members do **not** interact with the chain directly.

### Architecture in One Sentence

**DApp / Edgar / Telegram → Google Sheets → Mirror Service → TrueChain (Geth + Smart Contracts).**

### Key Components

| Component | Role |
|-----------|------|
| **TrueChain (Geth)** | Private blockchain; stores events via smart contracts |
| **Mirror Service** | Reads from Sheets, submits transactions to TrueChain; writes **transaction hash** back to a `TrueChain Tx` column |
| **GAS (read API)** | Returns transaction/block data as JSON; DApp calls GAS (not Edgar) for read-only viewing |
| **DApp** | **"View on TrueChain"** — new page that fetches tx data from GAS and renders it; no wallet required |
| **Edgar** | DAO API; does **not** serve block explorer traffic |

### Smart Contracts (Append-Only)

- `ContributionRegistry`, `OffchainTransactionRegistry`, `LedgerTransactionRegistry`, `InvoiceRegistry`, `QRCodeRegistry`, `TreePlantingRegistry`, `SalesReceiptRegistry`, `ShipmentRegistry`, `FarmRegistry`, `ProductRegistry`
- **Schema evolution:** Use `payloadHash` (keccak256 of canonical JSON) + `schemaVersion` so contracts stay unchanged when Sheets add/remove columns.

### Write Security (Must Adhere)

- **Only authorized keys can write.** Private key held only by Mirror Service; contracts use allowlist (`addWriter` / `removeWriter`) for revocation; no IP restriction. See [§8 Write Security Protocol](#8-write-security-protocol).

### Existing Records

- **Do not backfill** initially. Mirror **new records only** going forward.

### Where to Find More

- **TrueChain repo:** [github.com/TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain) — `README.md`, `genesis.json`, `truffle_actual/contracts/`
- **Sheets schema:** `tokenomics/SCHEMA.md`
- **Workspace context:** `WORKSPACE_CONTEXT.md`, `PROJECT_INDEX.md`

---

## Table of Contents

1. [For Everyone](#1-for-everyone)
2. [What is TrueChain? (Plain Language)](#2-what-is-truechain-plain-language)
3. [Why Are We Using It?](#3-why-are-we-using-it)
4. [How Does It Fit With What We Already Have?](#4-how-does-it-fit-with-what-we-already-have)
5. [What Data Gets Recorded on TrueChain?](#5-what-data-gets-recorded-on-truechain)
6. [How Members Experience It](#6-how-members-experience-it)
7. [Setup: Local → AWS → Production](#7-setup-local--aws--production)
8. [Write Security Protocol](#8-write-security-protocol)
9. [Viewing Transactions (DApp + GAS)](#9-viewing-transactions-dapp--gas)
10. [Handling Changes to Our Data (Schema Evolution)](#10-handling-changes-to-our-data-schema-evolution)
11. [Products, Shipments, and Farms](#11-products-shipments-and-farms)
12. [What About Our Existing Records?](#12-what-about-our-existing-records)
13. [Technical Proposal: Scenario Mapping & Contracts](#13-technical-proposal-scenario-mapping--contracts)
14. [Implementation Phases](#14-implementation-phases)
15. [References](#15-references)

---

## 1. For Everyone

### What is it?

TrueChain is like a shared, tamper-proof ledger. When we record something (a contribution, a sale, an invoice), it gets written to the blockchain and cannot be changed. That helps us:

- **Verify** that records are correct
- **Build trust** with customers (e.g. cacao provenance)
- **Support governance** (contributions for voting rights)

### Do I need to do anything different?

**No.** You keep using the DApp, Telegram, and Edgar exactly as you do today. The blockchain recording happens in the background. You don't need a wallet or any blockchain knowledge.

### What might I see later?

- A **"Verified on TrueChain"** badge on product or QR pages
- A **"View on TrueChain"** link in the DApp — opens a transaction view (no wallet required)

### Repository

The TrueChain codebase (Geth nodes, smart contracts, setup) lives at: **[https://github.com/TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain)**

---

## 2. What is TrueChain? (Plain Language)

**TrueChain** is a **private blockchain** that TrueSight DAO runs. Think of it like a shared, tamper-proof ledger that multiple computers maintain together.

### Simple Analogy

Imagine a shared notebook where every time someone records something (a contribution, a sale, an invoice), that entry is written in ink and cannot be erased or changed. Everyone can look back and verify that the record is correct. That notebook is TrueChain.

### Technical Details (For Implementers)

- **Software:** Geth (Go Ethereum)—the same software that runs the public Ethereum network
- **Consensus:** Proof of Authority (Clique)—a small set of trusted nodes (signers) produce blocks
- **Chain ID:** 98794616
- **Block time:** About 5 seconds
- **Currency:** TRUE (used for gas; we set gas price to 0, so there are no per-transaction fees)
- **Repository:** [https://github.com/TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain)

---

## 3. Why Are We Using It?

We use TrueChain to create an **immutable audit trail** for important DAO and Agroverse data.

### Benefits

| Benefit | What It Means |
|---------|---------------|
| **Verifiable** | Anyone can check that a contribution, sale, or invoice was recorded at a specific time |
| **Tamper-proof** | Once written, records cannot be altered or deleted |
| **Trust** | Customers can see that their cacao bag's provenance (farm, shipment, tree planting) is recorded on a blockchain |
| **Governance** | Contributors can prove their contributions for voting rights |

### What We Are *Not* Doing

- We are **not** replacing Google Sheets. Sheets remain where we do our day-to-day work.
- We are **not** asking members to use wallets or understand blockchain. They keep using the DApp, Telegram, and Edgar as they do today.
- We are **not** storing sensitive personal data on the chain. We use hashes (fingerprints) instead of raw names where appropriate.

---

## 4. How Does It Fit With What We Already Have?

### Current Stack (Before TrueChain)

- **Google Sheets** — Main Ledger, Telegram & Submissions, AGL ledgers
- **Edgar** (edgar.truesight.me) — Rails API for contributions, proposals, etc.
- **Google Apps Script** — Tokenomics, expense processing, sales, QR codes, tree planting
- **DApp** — Web forms for signatures, expenses, scanner
- **Telegram** — Submissions (expenses, sales, movements, tree planting)

### With TrueChain Added

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  DApp / Edgar   │────▶│  Google Sheets   │◀────│  GAS / Telegram │
│  (submit, API)  │     │  (source of      │     │  (expenses,     │
└─────────────────┘     │   truth)         │     │   sales, etc.)   │
                        └────────┬─────────┘     └─────────────────┘
                                 │
                                 │  Mirror Service (reads new rows,
                                 │  submits to TrueChain)
                                 ▼
                        ┌──────────────────┐
                        │  TrueChain       │
                        │  (Geth + Smart   │
                        │   Contracts)     │
                        └──────────────────┘
```

**In plain language:** Data still goes into Google Sheets first. A background service (the **Mirror Service**) watches for new rows and copies them to TrueChain. Sheets stay the source of truth; TrueChain is the permanent record.

---

## 5. What Data Gets Recorded on TrueChain?

We mirror these types of data:

| Data Type | Where It Lives Today | What Gets Recorded on TrueChain |
|-----------|----------------------|----------------------------------|
| **Contributions** (for voting rights) | Contribution submission, Ledger history | Contribution record (contributor, project, TDGs, date) |
| **Offchain transactions** | offchain transactions sheet | Transaction (date, description, amount, currency) |
| **Managed ledger transactions** | AGL ledgers (AGL1, AGL15, etc.) | Ledger transaction (ledger, date, amount, sender, recipient) |
| **Invoices** | Expense submissions, freight, lab reports | Invoice hash + metadata (vendor type, amount, date) |
| **QR codes / bags** | Agroverse QR codes | QR registration, bag transfers, bag sales |
| **Tree plantings** | SunMint Tree Planting | Tree pledge (on sale), tree planted (on submission) |
| **Sales receipts** | Venmo, PIX, Stripe | Receipt hash (payment method, amount, reference) |
| **Products, shipments, farms** | Product pages, Shipment Ledger Listing | Product → Shipment → Farm linkage |

Each record is **append-only**—we never update or delete. If we need to change something, we add a new record.

### Transaction Hash Column

Each mirrored sheet has a **`TrueChain Tx`** column (at the end of the sheet). When the Mirror Service successfully records a row on TrueChain, it writes the **transaction hash** back to that column. This provides:

- **Bidirectional linkage** — Sheet row ↔ TrueChain transaction
- **Idempotency** — If the column already has a hash, skip re-mirroring
- **"View on TrueChain"** — DApp links use this hash to fetch and display the transaction

---

## 6. How Members Experience It

### Day-to-Day: No Change

Members keep using: **DApp**, **Telegram**, **Edgar**. They do **not** need MetaMask, TRUE tokens, or any blockchain knowledge.

### What They Might See Later

- **"Verified on TrueChain"** badge on product pages or QR code landing pages
- **"View on TrueChain"** link — opens a **DApp page** that shows the transaction (no wallet required; DApp fetches from GAS)
- **Provenance timeline** — e.g. "Bag registered → Sold → Tree pledged" with links to each record

---

## 7. Setup: Local → AWS → Production

| Phase | TrueChain | Mirror Service | Edgar |
|-------|-----------|---------------|-------|
| **Local** | Geth on your machine | Points to localhost:8545 | Run locally |
| **AWS test** | Geth on EC2 | Points to EC2 RPC URL | Local or test Edgar → EC2 |
| **Production** | Geth on EC2 | Points to production RPC | Production Edgar → production RPC |

### Phase 1: Local Setup

1. **Clone and run TrueChain** — Clone [TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain), follow `README.md` to start node1–4, deploy contracts with Truffle to `localhost:8545`
2. **Run Mirror Service** — Point to `http://127.0.0.1:8545`, use staging Sheets
3. **Run Edgar locally** — Set `TRUECHAIN_RPC_URL=http://127.0.0.1:8545`

### Phase 2: AWS EC2

1. Provision EC2, install Geth, copy `genesis.json` and `static-nodes.json`
2. Update `static-nodes.json` with EC2 IPs
3. Deploy contracts, save addresses
4. Point Mirror Service to `http://<ec2-ip>:8545`

### Phase 3: Production

Production TrueChain on EC2, production Edgar, production Mirror Service.

### Configuration

```
TRUECHAIN_RPC_URL=http://127.0.0.1:8545          # Local
TRUECHAIN_RPC_URL=http://<ec2-ip>:8545           # AWS
TRUECHAIN_RPC_URL=http://truechain.internal:8545 # Production
```

---

## 8. Write Security Protocol

**Only authorized private keys can write to TrueChain.** This protocol must be adhered to in all deployments.

### Requirements

| Control | Requirement |
|---------|-------------|
| **Private key** | Only the Mirror Service (and any other authorized writers) hold the private key(s) that sign write transactions. Store keys in a secrets manager (e.g. AWS Secrets Manager), not in code or config. Never expose keys to unauthorized parties. |
| **Contract access control** | All registry contracts must restrict write functions (e.g. `recordContribution`, `recordInvoice`) to authorized addresses via an allowlist with `addWriter` and `removeWriter`. The owner (e.g. multisig) manages the allowlist; writers are the Mirror Service key addresses. |

We do **not** restrict RPC by IP address. Write authorization is enforced solely by the private key and contract access control. Anyone can reach the RPC; only transactions signed by an authorized key will succeed. This is the standard Ethereum model—the key is the credential.

### Contract Pattern: Allowlist with Revocation

Use an allowlist so we can add writers (e.g. new Mirror Service instances) and revoke them (e.g. exposed key):

```solidity
mapping(address => bool) public authorizedWriters;

function addWriter(address writer) external onlyOwner {
    authorizedWriters[writer] = true;
}

function removeWriter(address writer) external onlyOwner {
    authorizedWriters[writer] = false;
}

modifier onlyAuthorizedWriter() {
    require(authorizedWriters[msg.sender], "Not authorized");
    _;
}
```

- **Owner:** Separate from writers; used only for `addWriter` / `removeWriter`. Prefer multisig.
- **Writers:** Mirror Service address(es). Each instance can have its own key; all are in the allowlist.

### Key Revocation (Exposed Key)

If a private key is accidentally exposed:

1. **Revoke:** Call `removeWriter(compromisedAddress)` from the owner account.
2. **Rotate:** Create a new key, call `addWriter(newAddress)`, update Mirror Service to use it.
3. **Retire:** Remove the old key from secrets manager; stop using it.

After revocation, transactions signed by the old key will revert—the contract rejects them because the address is no longer authorized.

### Multiple Writers

- **Multiple Mirror Service instances:** Each can have its own key; add all addresses via `addWriter`. Use idempotency (e.g. queue, partitioning) so instances don't duplicate writes.
- **Shared key:** All instances use the same key. Simpler, but need coordination to avoid duplicate mirroring of the same row.

### Read vs Write

- **Read:** GAS reads from RPC to serve "View on TrueChain". The RPC URL is kept private (Script Properties); the DApp never sees it.
- **Write:** Only transactions signed by an authorized key. The contract rejects writes from any other address.

### Why No IP Restriction

- The private key is the credential. If someone has the key, they can write from anywhere; if they don't, they can't. IP restriction doesn't change that.
- No IP restriction simplifies operations: add/remove Mirror Service instances, run from different locations, avoid firewall management.
- This matches standard Ethereum practice: authorization by signature, not by network origin.

### Network Topology

Network topology (enodes, node IPs) can be **public or private**. If public, anyone can run a node and sync the chain; reads become more verifiable. Write security is unchanged—it depends on the key and contract, not topology.

### Checklist for New Deployments

- [ ] Key: Mirror Service key(s) in secrets manager; no other copies
- [ ] Contracts: Allowlist with `addWriter` / `removeWriter`; owner separate from writers
- [ ] GAS: Uses Script Properties for RPC URL; URL not in public source

---

## 9. Viewing Transactions (DApp + GAS)

When users click **"View on TrueChain"**, they see a **DApp page** (not a separate explorer). No wallet or key pair required.

### Flow

```
User clicks "View on TrueChain" in DApp
        │
        ▼
┌─────────────────────┐
│  DApp               │  fetch(GAS_URL + "?tx=0x...")
│  (view_transaction  │
│   .html)            │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  GAS Web App        │  doGet(e) → check cache → if miss, UrlFetchApp(TrueChain RPC)
│  (returns JSON)     │  → return { tx, receipt, decodedEvents }
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  TrueChain (EC2)    │
│  Geth JSON-RPC      │
└─────────────────────┘
```

### Why DApp + GAS?

- **DApp:** Unified experience; no wallet needed; consistent branding
- **GAS for reads:** Saves Edgar bandwidth; caching reduces RPC calls; no new server
- **GAS returns JSON:** DApp renders the transaction view with its own layout

### Local testing

GAS cannot reach localhost; use ngrok to expose local Geth for testing.

---

## 10. Handling Changes to Our Data (Schema Evolution)

Smart contracts are **immutable**. We design for evolution using:

1. **Core identifiers** — contributor hash, date, ledger ID (fixed)
2. **Payload hash** — `keccak256(canonical JSON of all fields)`
3. **Schema version** — 1, 2, 3… so we know how to decode the payload

When we add a new column: update Mirror Service encoding, bump schema version. The contract stays the same.

---

## 11. Products, Shipments, and Farms

Each Agroverse product (e.g. [Ceremonial Cacao – La do Sitio Farm](https://agroverse.shop/product-page/ceremonial-cacao-paulo-s-la-do-sitio-farm-2024-200g/index.html)) links to a **shipment batch** (e.g. AGL8) and a **farm** (e.g. La do Sitio).

### On-Chain Model

| Registry | Purpose |
|----------|---------|
| **ShipmentRegistry** | Shipment batches (AGL8, etc.) |
| **FarmRegistry** | Farms (La do Sitio, Paulo, CEPOTX) |
| **ProductRegistry** | Product = (product type + farm + year + shipment) |
| **QRCodeRegistry** | Each bag's QR code → Product → Shipment + Farm |

**Traceability:** QR code (bag) → Product → Shipment + Farm

---

## 12. What About Our Existing Records?

- **Recommendation:** Mirror **new records only**. Do not backfill historical data initially.
- **Why?** Volume (10,000+ rows), risk of inconsistencies, value is in forward audit trail.
- **If we backfill later:** Prioritize high-value records, use idempotency keys, run in batches.
- **Optional:** Single Merkle root of historical rows as one audit anchor.

---

## 13. Technical Proposal: Scenario Mapping & Contracts

### Scenario-to-TrueChain Mapping

| Data Type | Contract | Key Function |
|-----------|----------|--------------|
| Contributions | `ContributionRegistry` | `recordContribution(contributorHash, project, rubric, tdgsProvisioned, tdgsIssued, statusDate)` |
| Offchain transactions | `OffchainTransactionRegistry` | `recordTransaction`, `recordBalanceSnapshot` |
| Ledger transactions | `LedgerTransactionRegistry` | `recordLedgerTransaction`, `recordLedgerBalance` |
| Invoices | `InvoiceRegistry` | `recordInvoice`, `recordShipment` |
| QR codes / bags | `QRCodeRegistry` | `registerQRCode`, `recordBagTransfer`, `recordBagSale` |
| Tree plantings | `TreePlantingRegistry` | `recordTreePledge`, `recordTreePlanted` |
| Sales receipts | `SalesReceiptRegistry` | `recordReceipt` |
| Shipments, farms, products | `ShipmentRegistry`, `FarmRegistry`, `ProductRegistry` | `registerShipment`, `registerFarm`, `registerProduct` |

### Design Principles

- **Append-only:** No updates or deletes
- **Hashes for PII:** `keccak256(name)` instead of raw names
- **Events:** Emit rich events for indexing; minimal storage
- **Access control:** Allowlist with `addWriter` / `removeWriter`; owner manages allowlist; writers are Mirror Service addresses. See [§8 Write Security Protocol](#8-write-security-protocol).

### Mirror Service Responsibilities

1. Read from Google Sheets (API or webhook)
2. Transform row data into contract parameters
3. Submit via JSON-RPC using an authorized key (stored in secrets manager)
4. **Write transaction hash back** to the `TrueChain Tx` column on the sheet (bidirectional linkage)
5. Retry with idempotency (contributorHash + date + rowIndex)

### AWS Layout (Later Stage)

- EC2 node1, node2, node3 (signers) → Internal ALB → Mirror Service
- Geth `--datadir` on EBS; scale client nodes as needed

### Open Questions

1. Contributor → Ethereum address mapping?
2. Owner for `addWriter` / `removeWriter`: multisig vs single key?
3. Data retention / pruning?
4. Cost: gas=0, main cost is EC2 and engineering.

---

## 14. Implementation Phases

| Phase | Scope | Timeline |
|-------|-------|----------|
| 1. Local PoC | ContributionRegistry + OffchainTransactionRegistry; mirror 10–20 rows | 2–4 weeks |
| 2. Contract suite | All registries; unit tests | 4–6 weeks |
| 3. Mirror Service | Node or Rails; webhook/cron; idempotency | 2–3 weeks |
| 4. Single EC2 | Deploy TrueChain + Mirror; production Sheets | 2–3 weeks |
| 5. Block Explorer (GAS + DApp) | GAS API (returns JSON); DApp view_transaction page; "View on TrueChain" links | 1–2 weeks |
| 6. Full mirror | All data types; txHash columns | 2–4 weeks |
| 7. Scale & polish | Multi-EC2; provenance badges; monitoring | Ongoing |

---

## 15. References

| Resource | Purpose |
|----------|---------|
| **[TrueSightDAO/TrueChain](https://github.com/TrueSightDAO/TrueChain)** | TrueChain repository — Geth setup, genesis, Truffle contracts, node config |
| **tokenomics/SCHEMA.md** | Google Sheets schema (columns, sheet names, IDs) |
| **WORKSPACE_CONTEXT.md** | Workspace overview, project relationships |
| **PROJECT_INDEX.md** | Per-project summary, entry points, credentials |
| **GOOGLE_API_CREDENTIALS.md** | Service accounts, spreadsheet IDs |
| **Edgar** | sentiment_importer (edgar.truesight.me) |

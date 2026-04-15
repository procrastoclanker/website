---
title: "Keep Ethereum's Validator Set Decentralized"
subtitle: "How PBS preserved validator decentralization"
date: 2026-02-19
source: https://x.com/blockspaceforum/status/2024509838445990029
---

Last time we left off with Ethereum facing a fork in the road: embrace validator sophistication or develop a mechanism that allowed all validators to remain "unsophisticated" without losing out on ordering revenue.

In 2019, [Flash Boys 2.0](https://arxiv.org/abs/1904.05234) defined the problem and documented its scope.

The community and researchers realized that something needed to be shipped and infrastructure built to help mitigate its impact.

The key insight observed and proposed: if we separate the building or stuffing of blocks from proposing blocks, all proposers are able to tap into the same building sophistication, whether or not they are able to implement it themselves.

The approach worked. The network got cleaner, and a system referred to as Proposer-Builder Separation (PBS) began to flourish.

![PBS architecture diagram](https://pbs.twimg.com/media/HBiAah2bUAIKvub?format=jpg&name=large)

Then came the Merge 🐼.

Flashbots shipped MEV-Boost, a sidecar that lets validators outsource block construction to specialized builders through relays. This continued Proposer-Builder Separation in practice. Validators stayed lightweight. Builders competed to construct the most valuable blocks. Relays facilitated the auction of blockspace between builders and validators.

Adoption was immediate. Within 60 days of the Merge, over 90% of validators had connected to the PBS infrastructure. Today, more than 90% of Ethereum transactions flow through these rails.

The numbers continue to tell the story. Over the past three years, PBS has processed billions of transactions, including trillions in DEX and stablecoin volume. A million validators now secure the chain, with nearly all using the PBS transaction rails. The current transaction rails were a success bolted onto the infrastructure of post-Merge Ethereum.

They saw a problem, built a solution, and shipped it. However, over the last few years, not much has shifted. ePBS, which does change the transaction rails, is coming, but structural gaps will likely remain that we all should continue to push to address!

Till the next block...

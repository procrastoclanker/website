---
title: "A Counterparty Without Counterparty Risk"
subtitle: "Ethereum's robustness and where the rails fall short"
date: 2026-03-09
source: https://x.com/blockspaceforum/status/2031019543020163080
---

Ethereum provides the most robust blockspace on earth. Users. Apps. L2s. Stablecoin issuers. Institutions. Degens. It acts as a counterparty without introducing counterparty risk. Its uptime outcompetes any other network. It will survive wars and give opportunities where current opportunities can't be provided.

However, the transaction rails to access this network lack the same strength and robustness.

But what does robustness even mean? We see robustness across three properties: **liveness, fair access, and proposer agency**. All of which are critical.

## Liveness

**Liveness** can be described as Ethereum's ability to continuously chug along processing transactions and stacking blocks, 24/7, 365 days a year, no matter what is happening in the world. The core protocol is designed for this with hundreds of thousands of validators, multiple client implementations, geographic distribution, and many other safeguards.

But the current transaction rails are narrower. [Two builders produce roughly 80% of blocks. Three relays handle 86% of traffic.](https://x.com/blockspaceforum/status/2027040326980948391) They share data centers, software, hardware dependencies, and legal risks. A hardware outage or issue doesn't stay local; it can impact a significant share of transactions trying to reach blocks.

This concentration isn't accidental. [Research shows geographic clustering among operators emerges from economic incentives in the protocol's architecture](https://arxiv.org/abs/2312.09654), locations with favorable latency attract more operators, and the cycle reinforces itself. As a result, validators are heavily clustered around the Atlantic corridor, where latency is most favorable.

![Validator distribution and inter-region internet latency](https://pbs.twimg.com/media/HC-eEqRXsAA8UTj?format=png&name=large)

Validator distribution and inter-region internet latency, from Yang et al. (2026) using data from Chainbound (2024).

In summary, not only is the transaction journey not as robust as Ethereum, but its incentives actually degrade Ethereum's robustness by leaving its validator set concentrated.

## Fair Access

**Fair access** means equal access for all to blockspace. No matter your jurisdiction, who does and doesn't like you, or what your transaction does. Ethereum aims to provide full fair access. However, in the current transaction rails, there is a small operator set supporting the transaction rails that are in key jurisdictions vulnerable to legal and regulatory pressure that can disrupt this fair access.

:::stat 78% | of blocks were OFAC-compliant in the months following the Merge. Transactions involving sanctioned addresses were systematically excluded.:::

This has already happened. In the months following the merge, up to 78% of blocks were OFAC-compliant. Transactions involving sanctioned addresses were systematically excluded from the chain.

![OFAC compliance data from mevWatch.info](https://pbs.twimg.com/media/HC-eM7lakAEYi2t?format=png&name=large)

Source: [mevWatch.info](https://mevwatch.info/)

That number has improved since. But the episode showed: when the operator set is small enough, external pressure can shape what gets included in Ethereum blocks.

While multiple teams are exploring cryptographic enforcement tools (TEEs, MPC, FHE) and we believe they can help, the structural fix isn't forcing everyone into a single solution. Instead, we should be creating incentives and rails that encourage a more distributed operator set.

## Proposer Agency

**Proposer agency** is the third dimension. The Ethereum validator set is large, with over 1,000,000 active validators. In principle, they could enforce preferences: choosing relays that don't censor, favoring builders that include more transactions, and offering services like preconfirmations. In essence, the transaction journey would be more robust if each validator could express some view over some of the operators and operations in that pipeline. But, in practice, they can't... at least not without paying for it or teams coming together to change the way blocks are built.

As we [previously showed](https://x.com/blockspaceforum/status/2027037604332384379), builders are incentivized to get exclusive flow. This concentrates block construction among a small set of builders. While this has a unique impact on Ethereum and the network, it also impacts anyone who wants to locally build. Building blocks locally or excluding builders or relays leads to a material opportunity cost in revenue.

:::stat 400% | more value in PBS blocks vs locally built blocks, trending to 7.65x in volatile periods. Opting out of PBS is economically punitive.:::

A 2024 analysis from [@nero_eth](https://x.com/nero_eth) demonstrated that blocks procured via the PBS pipeline pay a median 400% more than locally built blocks:

![PBS vs local block value comparison](https://pbs.twimg.com/media/HC-eWsQW4AAzN-U?format=png&name=large)

Source: Toni Wahrstätter

This has been trending upwards and scales with volatility. In the last 30 days, [PBS blocks have had a value surplus of 7.65x versus locally built blocks](https://explorer.rated.network/relays?network=mainnet&timeWindow=30d).

The pipeline also gates functionality. Services like preconfirmations (where a proposer commits to including a transaction ahead of a slot) expand Ethereum's capabilities. Or, even the ability to run software that has [out-of-protocol mechanisms](https://github.com/eserilev/il-boost) like FOCIL could improve the robustness of Ethereum. However, without changes to the current transaction rails, proposers can't offer these guarantees.

These three dynamics are connected; many a function of the same economic incentives driving concentration we previously wrote on. The infrastructure that processes most of Ethereum's blocks should match the resilience of the protocol itself, and certainly not degrade the actual network.

Getting there means rethinking the incentives.

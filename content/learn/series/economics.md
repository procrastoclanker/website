---
title: "Align the Incentives"
subtitle: "Economics: Align the incentives to align the outcome"
date: 2026-02-26
source: https://x.com/blockspaceforum/status/2027037604332384379
---

As Charlie Munger put it: "Show me the incentive, and I'll show you the outcome."

Ethereum's transaction journey relies on a set of economic incentives. Those incentives shape who builds, who profits, and who pays; ultimately, these forces are foundational to the rails they support and not only impact Ethereum but also its users.

Last, we outlined four structural gaps in today's blockspace market: economics, robustness, performance, and services. Economics underpins most of this, so let's dive in on some of these gaps.

## Exclusive Order Flow and Its Impact

The way the system works today, builders gather transactions, assemble blocks, and bid for the right to propose them. Highest bid wins. For proposers, this is ideal; builders compete to pay them the most. For builders, this becomes a competition to see who can bid the most versus the next best builder.

So what do builders do? Exactly what the incentives push them and anyone competing to do... look for an edge.

:::stat 84% | exclusive transactions account for up to 84% of the fees in winning blocks:::

Three years since the merge, it's clear that builders' edge to outcompete the next builder comes down to exclusive flow, distribution, technology, and team. But of these factors, exclusive order flow is far and away the most dominant (exclusive flow is when users only send their transactions to one party, i.e., a wallet or RPC may send transactions directly and exclusively to one builder). To put this concretely, exclusive transactions account for up to 84% of the fees in winning blocks.

The auction isn't rewarding builders for the best block for Ethereum. It's selecting the best-connected builder.

![Exclusive order flow analysis showing 84% of fees from exclusive transactions](https://pbs.twimg.com/media/HCF7IuaXsAAdLg1?format=png&name=large)

Source: [arxiv.org/pdf/2509.16052](https://arxiv.org/pdf/2509.16052)

Furthermore, users have strong incentives to send exclusively to one builder. When a transaction goes to every builder, the current system drives its value to proposers while none flows back to the user. Sending to a single builder lets the user retain more value (i.e., fee rebates).

See the flywheel? Win more auctions, attract more exclusive flow. Both sides are feeding it.

![Builder market share from bids.pics](https://pbs.twimg.com/media/HCF7WsMWkAAGS5U?format=png&name=large)

Source: [bids.pics](https://bids.pics/)

Today, roughly 80% of blocks are built by just two or three entities. Barriers to entry are high, and new builders need long-term subsidies just to reach the scale where exclusive flow becomes available.

The impact on users? These dynamics mean users pay roughly 15% more than needed as they can't predict when their transactions will land, leading to overpayment to cover the uncertainty cost of waiting. Then, in some cases, users just end up having to wait seconds longer.

:::stat 19% | the median block is 19% underutilized, leaving hundreds of millions of fees on the table:::

The impact on Ethereum? We find that the median block is 19% underutilized, leaving hundreds of millions of fees on the table, not to mention the opportunity cost of blockspace that could have been used is never able to be utilized again.

Some will argue we need to fix the builders. But really, that's just treating the symptom, not the disease. What we as a community should focus on is fixing the incentives that drive this outcome.

## How the System (Fails To) Incentivize Relays

Relays sit between builders and proposers. They run the auction, verify blocks, and ensure fair exchange. Critical infrastructure, but with no defined business model. The system depends on them, but doesn't pay them.

The result is economic fragility and a degraded Ethereum: relay shutdowns that reduce the active set to a handful of operators, underinvestment in performance and robustness, increased concentration risk, weaker geographic and network coverage, and slower iteration on monitoring and transparency.

![Relay market data from ethPandaOps](https://pbs.twimg.com/media/HCF7h1LXQAE5As2?format=png&name=large)

Source: [ethpandaops.io/data/xatu/](https://ethpandaops.io/data/xatu/)

Without built-in incentives, relays unsurprisingly have resorted to designs of their own. Some charge a subscription while others implement a feature called a "bid-adjustment," taking a cut between what the builder offers and what the proposer is willing to take. These adjustments typically run 0.5-1% of block value. Great for relays, bad for Ethereum.

For instance, when a relay adjusts too aggressively, the best block loses to an inferior one. :::stat ~5% | of slots are affected by relay bid adjustments selecting inferior blocks. In 2026, blocks worth $8.6M combined were impacted.:::

This currently happens in roughly 5% of slots. Only in 2026 so far, blocks worth as much as a combined $8.6m have been affected by failed adjustments, incurring an opportunity cost of around 2% relative to the best block. Not to mention all those blocks that weren't optimal for Ethereum.

![Impact of relay bid adjustments](https://pbs.twimg.com/media/HCF7rjIXAAA_NyK?format=png&name=large)

Some will argue we should get rid of relays entirely. ePBS takes a step in that direction, and it's an important one. But removing relays doesn't remove the dynamics that shaped them. New infrastructure will meet the same economic forces, and gaps will surface. The problem isn't relays; it's the incentive vacuum they were left to fill.

## Where the Incentives Leave Us

The economic incentives of exclusive order flow drive multiple forces profoundly counterproductive to Ethereum: concentrated builders, counterproductive relays, underutilized blocks, fees being left on the table, and users paying more and waiting longer. The impact from relays is similar where we see a fundamental lack of incentives leading to counterproductive behavior.

Incentives for critical infrastructure surrounding Ethereum should be supporting and pushing Ethereum forward, not hindering it. Addressing this means rethinking the system, and therefore the incentives.

"Align the incentive, align the outcome."

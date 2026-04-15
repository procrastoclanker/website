---
title: "Three Years of PBS"
subtitle: "A survey of the structural gaps"
date: 2026-02-25
source: https://x.com/blockspaceforum/status/2026671024348054009
---

The next set of articles and threads will start diving into the intricacies of the transaction rabbit hole. The first is a survey of structural gaps, with follow-on articles focused on the details across each gap. Keep with us on this train to make Ethereum faster, cheaper, and more robust.

Last time, we covered how the research community shipped Proposer-Builder Separation. Today, over 90% of Ethereum blocks leverage its framework.

:::stat 90% | of Ethereum blocks flow through the PBS pipeline. Three years at production scale have surfaced structural gaps.:::

The system works. But three years at production scale have surfaced structural gaps in the design. Specifically, as we outlined in our first [ETH Research post](https://ethresear.ch/t/an-observation-on-ethereum-s-blockspace-market/23669), these gaps span Ethereum's economics, robustness, performance, and services. We believe each can be improved, and some rethought entirely, to help Ethereum better serve its core product: blockspace.

## Economics

Incentives across the transaction and block construction rails are misaligned or missing entirely. Key economic gaps include:- Multiple forces cause the current rails to incentivize exclusive order flow.- The current block auction lacks effective price discovery.- Exclusive order flow fragments transactions across builders, increasing costs and wait times for everyday Ethereum users.- The current pipeline and designs mostly force users unnecessarily to absorb all the volatility and uncertainty risk tied to payment and inclusion in blockspace.- Some key actors, such as relays, lack economic incentives entirely, leading to counterproductive behavior as they seek to develop sustainable business models.

![Exclusive order flow chart showing majority of fees from exclusive transactions](https://pbs.twimg.com/media/HCArqE1XQAEQ7va?format=png&name=large)

Exclusive transactions make up a small fraction of total volume, but consistently account for a majority of fees paid. The highest-value activity on Ethereum routes through private channels, not the public mempool.

## Robustness

Ethereum's core protocol guarantees liveness, but the out-of-protocol rails that Ethereum depends on do not match this guarantee. Key robustness gaps include:- Today's rails don't support strong liveness due to incentives that drive concentrated operators, shared infrastructure dependencies, and geographic clustering.- Fair access mechanisms don't support originators who need privacy or censorship resistance.- Ethereum's 1M+ validators have lost autonomy over block construction, leading to their inability to create constraints around how their blocks are constructed.

![OFAC compliance chart showing censorship levels post-Merge](https://pbs.twimg.com/media/HCAr5NWXkAAbKqb?format=png&name=large)

This is not a theoretical risk; in the wake of the merge, up to 78% of blocks were censored. Source: [mevwatch.info](https://mevwatch.info/)

## Performance

Ethereum itself should be the bottleneck in speed and performance, and not the block construction pipeline. Today, performance bottlenecks in the supporting infrastructure are leading to reduced blockspace utilization. Key performance gaps include:- Block construction has no formal capacity planning, such as minimum fullness targets or mechanisms for handling demand surges.- Proximity advantages go largely unmeasured and, therefore, unchecked, impacting robustness and other aspects of the block construction pipeline.

Consider the example of the October 2025 crash. We see a clear increase in low gas blocks in this time of high volatility (exactly a time when we need full blocks) as builders optimize latency instead of network throughput.

![Low gas blocks during October 2025 volatility](https://pbs.twimg.com/media/HCAsFaVXsAAUoPh?format=png&name=large)

## Services

Validators adopted PBS to stay lightweight, but gave up control over block construction entirely. Key gaps from loss of validator autonomy and no blockspace services include:- Users all get the same experience when accessing blockspace.- There's no way to pay for faster confirmations, priority access, or any differentiated service (beyond tips, often too blunt an instrument for the job).- Builders and relays control what's possible, and no open rails exist to offer better alternatives.

In practice, just over 60% of validators use software that doesn't allow them to express constraints over their blocks.

![Validator software distribution from commit-boost.org](https://pbs.twimg.com/media/HCAsXhiW4AAaISy?format=png&name=large)

Source: [commit-boost.org](https://commit-boost.org/)

These four categories frame the structural gaps. Economics. Robustness. Performance. Services.

Diving into economics next.

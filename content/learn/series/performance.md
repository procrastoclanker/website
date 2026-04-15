---
title: "Wait"
subtitle: "Performance bottlenecks in the block construction pipeline"
date: 2026-03-20
source: https://x.com/blockspaceforum/status/2034999394555003080
---

The most valuable millisecond in Ethereum's block construction is the last one.

As each slot progresses, new transactions arrive, market conditions shift, and the information available to builders changes. Builders delay bids to capture more information. Validators delay header requests to capture higher-value bids. Users overbid because they can't predict when they'll land. Builders time their bids to be most competitive just before the proposer requests them.

Every participant in the pipeline faces the same incentive: wait.

![Bid value evolution over time during a slot](https://pbs.twimg.com/media/HD3DzfSWAAASX1h?format=png&name=large)

Bid value (vs maximum bid value) evolution over time during a slot. Source: Natale &amp; Moser (2023) - [arxiv.org/abs/2312.09654](https://arxiv.org/abs/2312.09654)

We've examined how the pipeline shapes economics and creates fragility. Performance is where these forces become measurable.

For the transaction pipeline, we believe three metrics can be used to help determine how well the system serves Ethereum: block value, capacity management, and time-to-inclusion. In plain terms, blockspace needs to be filled to capacity, fast, and predictably.

## Block Value

Block value measures how much of a block's potential is actually captured. When the auction works well, builders compete to bid competitively, and that value is distributed to proposers through competitive bidding. Builders, relays, and originators all take a share along the way. When competition narrows, less of that value reaches the proposer.

[We've covered the mechanics driving this in our economics thread](https://x.com/blockspaceforum/status/2027037604332384379): exclusive order flow concentrates building power, shrinking the competitive field. Fewer builders competing means less pressure to bid competitively. Relay bid adjustments siphon additional value between builder and proposer. The result is blocks that leave fees on the table and users who pay more than they should.

The effect is visible during periods of market stress, when the incentive to keep blocks lean and submit late is strongest:

![Block value during market stress periods](https://pbs.twimg.com/media/HD3ECQHboAMVJkN?format=png&name=large)

Data provided by Gattaca (2025)

The concentration is measurable. Today, 2-3 builders construct roughly 80% of blocks. The auction isn't selecting for the best block; it's selecting for the best-connected builder. That gap between potential and realized block value is the first efficiency cost the pipeline imposes on Ethereum.

## Capacity Management

Blocks should be full. They often aren't... even when they could be.

Builders have every incentive to keep blocks lean and submit as late as possible. The information available for block construction changes throughout the slot, new transactions entering the mempool, shifting prices, evolving arbitrage opportunities. A builder who waits a few hundred extra milliseconds can construct a meaningfully more profitable block. When prices are volatile, the rational strategy for any individual builder [works against the network's interest in filling every block to capacity](https://arxiv.org/abs/2312.09654).

Blobs compound this. Each blob adds to the physical size of a block. Larger blocks take longer to travel across the network, and validators that haven't received the block in time attest to the previous one instead. More blobs means more data to propagate within the same timing window, while the same incentives pull builders and validators toward publishing later.

The [ethPandaOps Fusaka analysis](https://ethpandaops.io/posts/fusaka-more-blobs-less-votes/) makes this tension visible. After Fusaka increased blob limits, attestation head votes began dropping as blob count rose. More data per block, fewer validators confirming it on time. At first glance, this looks like a scaling ceiling.

Segment the data by timing behavior, and the picture changes. Conservative entities that publish blocks promptly maintain roughly 99% head votes even at maximum blob counts. Entities operating at the margins of the timing window drive almost all of the degradation. The network can handle the data. The problem is when it arrives.

![ethPandaOps Fusaka blob analysis](https://pbs.twimg.com/media/HD3EJl1WkAAY7yI?format=png&name=large)

Source: [ethpandaops.io](https://ethpandaops.io/)

Fusaka didn't create this dynamic. It amplified it. More data to propagate in the same window, with the same incentives pulling in the opposite direction.

And the pressure only grows. Under the zkEVM, execution payloads need to reach provers quickly so they have time to generate validity proofs. If blocks continue to arrive at the margins of the timing window, proof generation time shrinks. The same dynamic that undermines attestation today will constrain Ethereum's ability to scale tomorrow.

## Time-to-Inclusion

Wait... so when will my transaction land? For most users, the honest answer is: nobody knows.

No public cutoff exists for transaction submission. Network latency varies unpredictably. Users bear this uncertainty directly, [overbidding defensively when conditions are volatile](https://arxiv.org/abs/2201.05574) to avoid waiting through additional blocks.

:::stat ~5% | additional weekly value captured by validators who strategically delay header requests. Solo stakers can't play this game.:::

Exploiting that uncertainty is rational. In the PBS auction, validators choose when to request a block header from relays. The later the request, the longer builders have to compete, and the higher the winning bid. Validators that strategically delay [capture roughly 5% additional value weekly](https://arxiv.org/abs/2312.09654). The tradeoff: wait too long and risk missing the slot entirely.

The costs don't stop with the proposer. Later bids consume more gas, inflating the base fee and burn rate for subsequent proposers. And the longer the auction runs, the more time for off-chain prices to move while on-chain prices remain stale. Liquidity providers bear this cost directly; traders exploit the price divergence, and arbitrage losses grow with every additional millisecond of delay.

![Burnt ETH increase as function of bid timing](https://pbs.twimg.com/media/HD3ESVsacAAKBZ3?format=png&name=large)

Burnt ETH increase for the subsequent block as a function of the eligibility of the bid (left) and bid value increase (right). Source: Natale &amp; Moser (2023) - [arxiv.org/abs/2312.09654](https://arxiv.org/abs/2312.09654)

Some proposers see the auction play out for over a second. Others see a fraction of it. The information gap between them compounds every other dynamic in the pipeline.

Large validators propose blocks frequently enough that the variance evens out. They accumulate data across thousands of proposals, refining their timing calibration with each one. Their risk is manageable, their returns predictable.

![Expected weekly block value increase by voting power](https://pbs.twimg.com/media/HD3EdL4boAYVkVi?format=png&name=large)

Expected weekly block value increase by voting power. Source: Natale &amp; Moser (2023)

Solo stakers propose rarely, perhaps once every few months. Each proposal carries outsized variance, and they lack the data to optimize their timing. The pipeline punishes them for a game they can't play.

Ethereum was designed to empower solo stakers, and yet solo stakers absorb the most cost from a dynamic they can't competitively exploit? There has to be a better way.

## The Common Thread

Underutilized blocks, unpredictable inclusion, escalating costs. These look like separate problems. They trace to the same force.

The pipeline incentivizes waiting. Builders wait for more information. Validators wait for higher bids. Users wait because they have no choice. Every participant optimizes their own timing, and the network pays for the collective delay.

Latency is an unavoidable consequence of decentralization; information takes time to propagate across a global network, and that's a physical constraint. Variance is different. A full second of spread between median and 95th percentile bid timing isn't a network constraint. It's the pipeline rewarding participants who can afford to optimize at the expense of those who can't.

However, we know small adjustments to the pipeline can address meaningful amounts of this variance, without requiring participants to act against their own interests. With these changes, you can wait all you want with the impact being minimal on the network, its users, and its decentralized validator set.

Wait...

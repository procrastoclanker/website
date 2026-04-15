---
title: "The Other Gwei"
subtitle: "A journey down the transaction rails of Ethereum"
date: 2026-02-17
source: https://x.com/blockspaceforum/status/2023761721622765728
---

Every 12 seconds, someone gets to build an Ethereum block.

That someone is a validator/proposer. They decide which transactions go in, in what order, and ultimately what that block is stuffed with.

When Ethereum was designed, it envisioned proposers would fill the blocks with transactions sorted by priority fee, highest first. Collect fees until the block is full. Simple.

![Block construction diagram](https://pbs.twimg.com/media/HBXXBDnbcAEHQUi?format=jpg&name=large)

However, as time passed, the network matured, and the activity on Ethereum moved from simple transfers to more complex operations and activities. People realized there were more profitable ways to construct a block. Validators discovered they could generate significantly more revenue by using sophisticated ordering rules rather than simply filling a block with the highest-paying transactions.

This resulted in two impacts on Ethereum and its users.

First, users and Dapp creators were experiencing degraded UX with activity and transactions leaking value to actors who could profit from organizing the transactions in a certain order.

Second, building optimizations that capture the value from a certain ordering aren't straightforward and require sophistication. The theory was that validators who could capture this value would out-earn everyone else. Over time, they'd accumulate more stake, earn a larger share of rewards, crowd out the rest, and create centralization pressures on Ethereum's validator set.

Ethereum had to make key choices: lean into validator sophistication or find another way.

Luckily, they found another gwei. More on that next.

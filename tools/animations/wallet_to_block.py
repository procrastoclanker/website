from manim import *

# Site palette: dark monochrome
BG = "#000000"
PRIMARY = "#e8e8e8"
SECONDARY = "#777777"
MUTED = "#3d3d3d"
SURFACE = "#0a0a0a"
MONO = "DejaVu Sans Mono"

# Stage colors - subtle differentiation
C_WALLET = "#8899aa"
C_PRIVATE = "#7788aa"
C_OFA = "#8899bb"
C_SEARCHER = "#aa8877"
C_BUILDER = "#88aa88"
C_RELAY = "#aa8888"
C_PROPOSER = "#9988aa"
C_CHAIN = "#e8e8e8"
C_VALUE = "#88bb99"


def make_node(label, color, width=1.8, height=0.7):
    """Create a labeled rounded rectangle node."""
    rect = RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        stroke_color=color, stroke_width=1.5, fill_color=BG, fill_opacity=1.0
    )
    txt = Text(label, font=MONO, font_size=14, color=color)
    return VGroup(rect, txt)


def make_arrow(start, end, color=MUTED):
    """Create a slim arrow between two mobjects."""
    return Arrow(
        start.get_right(), end.get_left(),
        buff=0.12, stroke_width=1.5, color=color,
        max_tip_length_to_length_ratio=0.15,
        max_stroke_width_to_length_ratio=2.0,
    )


def make_particle(color, radius=0.04):
    """Small circle representing a transaction/bundle/bid."""
    return Dot(radius=radius, color=color, fill_opacity=0.8)


class WalletToBlock(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ============================================================
        # Layout: 8 stages left to right
        # Wallet -> Private RPC -> OFA -> Searchers -> Builders -> Relay -> Proposer -> Chain
        # ============================================================
        wallet = make_node("Wallet", C_WALLET)
        private_rpc = make_node("Private RPC", C_PRIVATE, width=2.0)
        ofa = make_node("OFA", C_OFA, width=1.6)
        searcher = make_node("Searchers", C_SEARCHER, width=2.0)
        builder = make_node("Builders", C_BUILDER, width=1.8)
        relay = make_node("Relay", C_RELAY, width=1.6)
        proposer = make_node("Proposer", C_PROPOSER, width=1.8)
        chain = make_node("Chain", C_CHAIN, width=1.6)

        # Position horizontally
        nodes = [wallet, private_rpc, ofa, searcher, builder, relay, proposer, chain]
        spacing = 1.65
        start_x = -spacing * 3.5
        for i, node in enumerate(nodes):
            node.move_to(RIGHT * (start_x + i * spacing))

        # Arrows (all linear left-to-right)
        a_wallet_rpc = make_arrow(wallet, private_rpc, C_WALLET)
        a_rpc_ofa = make_arrow(private_rpc, ofa, C_PRIVATE)
        a_ofa_searcher = make_arrow(ofa, searcher, C_OFA)
        a_searcher_builder = make_arrow(searcher, builder, C_SEARCHER)
        a_builder_relay = make_arrow(builder, relay, C_BUILDER)
        a_relay_proposer = make_arrow(relay, proposer, C_RELAY)
        a_proposer_chain = make_arrow(proposer, chain, C_PROPOSER)

        # ============================================================
        # Title
        # ============================================================
        title = Text("From Wallet to Block", font=MONO, font_size=28,
                     color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.8)

        # ============================================================
        # Subtitle helper
        # ============================================================
        subtitle_bg = RoundedRectangle(
            corner_radius=0.08, width=12, height=0.55,
            fill_color="#0a0a0a", fill_opacity=0.92,
            stroke_width=0
        ).to_edge(DOWN, buff=0.25)

        def show_subtitle(text):
            sub = Text(text, font=MONO, font_size=13, color=SECONDARY)
            sub.move_to(subtitle_bg.get_center())
            return VGroup(subtitle_bg.copy(), sub)

        current_sub = None

        def swap_subtitle(text):
            nonlocal current_sub
            new_sub = show_subtitle(text)
            if current_sub:
                self.play(FadeOut(current_sub, run_time=0.3),
                          FadeIn(new_sub, run_time=0.3))
            else:
                self.play(FadeIn(new_sub, run_time=0.5))
            current_sub = new_sub

        # ============================================================
        # Stage 1: Wallet appears
        # ============================================================
        self.play(FadeIn(wallet, shift=UP * 0.2), run_time=0.8)
        swap_subtitle("You send a transaction from your wallet")
        self.wait(1.5)

        # ============================================================
        # Stage 2: Private RPC
        # ============================================================
        self.play(
            FadeIn(private_rpc, shift=UP * 0.2),
            GrowArrow(a_wallet_rpc),
            run_time=0.8
        )
        swap_subtitle("Your transaction is routed through a private RPC for privacy")
        self.wait(1.5)

        # Particle: wallet -> private RPC
        p1 = make_particle(C_WALLET, radius=0.05)
        p1.move_to(wallet.get_right())
        self.play(
            MoveAlongPath(p1, Line(wallet.get_right(), private_rpc.get_left())),
            run_time=0.6
        )
        self.play(FadeOut(p1), run_time=0.2)

        # ============================================================
        # Stage 3: OFA
        # ============================================================
        self.play(
            FadeIn(ofa, shift=UP * 0.2),
            GrowArrow(a_rpc_ofa),
            run_time=0.8
        )
        swap_subtitle("The OFA auctions rights to your transaction among searchers")
        self.wait(1.5)

        # Particle: private RPC -> OFA
        p2 = make_particle(C_PRIVATE, radius=0.05)
        p2.move_to(private_rpc.get_right())
        self.play(
            MoveAlongPath(p2, Line(private_rpc.get_right(), ofa.get_left())),
            run_time=0.6
        )
        self.play(FadeOut(p2), run_time=0.2)

        # Value flows back to wallet from OFA
        swap_subtitle("The OFA returns a share of the auction proceeds to the user")
        self.wait(0.5)

        value_particle = make_particle(C_VALUE, radius=0.045)
        value_particle.move_to(ofa.get_left())

        # Curved path back above the pipeline
        value_path = ArcBetweenPoints(
            ofa.get_top() + UP * 0.15,
            wallet.get_top() + UP * 0.15,
            angle=-TAU / 4,
        )
        value_label = Text("refund", font=MONO, font_size=10, color=C_VALUE)
        value_label.next_to(value_path.point_from_proportion(0.5), UP, buff=0.12)

        self.play(FadeIn(value_label, shift=DOWN * 0.1), run_time=0.4)
        value_particle.move_to(value_path.get_start())
        self.play(
            MoveAlongPath(value_particle, value_path),
            run_time=1.0,
        )
        self.play(FadeOut(value_particle), FadeOut(value_label), run_time=0.4)
        self.wait(0.8)

        # ============================================================
        # Stage 4: Searchers
        # ============================================================
        self.play(
            FadeIn(searcher, shift=UP * 0.2),
            GrowArrow(a_ofa_searcher),
            run_time=0.8
        )
        swap_subtitle("Searchers build optimized bundles with your transaction")
        self.wait(1.5)

        # Particle: OFA -> Searchers
        p3 = make_particle(C_OFA, radius=0.05)
        p3.move_to(ofa.get_right())
        self.play(
            MoveAlongPath(p3, Line(ofa.get_right(), searcher.get_left())),
            run_time=0.6
        )
        self.play(FadeOut(p3), run_time=0.2)

        # ============================================================
        # Stage 5: Builders
        # ============================================================
        self.play(
            FadeIn(builder, shift=UP * 0.2),
            GrowArrow(a_searcher_builder),
            run_time=0.8
        )
        swap_subtitle("Builders assemble transactions and bundles into a complete block")
        self.wait(1.0)

        # Multiple particles converging on builder
        particles = VGroup()
        for i in range(3):
            p = make_particle(C_SEARCHER, radius=0.035)
            p.move_to(searcher.get_right() + UP * (0.08 - i * 0.08))
            particles.add(p)

        self.play(
            *[MoveAlongPath(p, Line(p.get_center(), builder.get_left() + UP * (0.08 - i * 0.08)))
              for i, p in enumerate(particles)],
            run_time=0.8
        )
        self.play(FadeOut(particles), run_time=0.2)
        self.wait(0.8)

        # ============================================================
        # Stage 6: Relay auction
        # ============================================================
        self.play(
            FadeIn(relay, shift=UP * 0.2),
            GrowArrow(a_builder_relay),
            run_time=0.8
        )
        swap_subtitle("Builders submit blocks and bids to the relay. The relay runs an open auction.")
        self.wait(1.0)

        # Competing bids flowing to relay
        bid_colors = [C_BUILDER, "#77bb77", "#66aa99"]
        for j, bc in enumerate(bid_colors):
            bid = make_particle(bc, radius=0.04)
            bid.move_to(builder.get_right() + DOWN * (0.08 - j * 0.08))
            self.play(
                MoveAlongPath(bid, Line(bid.get_center(), relay.get_left())),
                run_time=0.35
            )
            self.remove(bid)

        # Bid value climbing
        bid_label = Text("Top bid: 0.042 ETH", font=MONO, font_size=11, color=C_RELAY)
        bid_label.next_to(relay, UP, buff=0.2)
        self.play(FadeIn(bid_label), run_time=0.4)
        self.wait(0.4)
        bid_label2 = Text("Top bid: 0.051 ETH", font=MONO, font_size=11, color=C_RELAY)
        bid_label2.next_to(relay, UP, buff=0.2)
        self.play(ReplacementTransform(bid_label, bid_label2), run_time=0.4)
        self.wait(0.4)
        bid_label3 = Text("Top bid: 0.063 ETH", font=MONO, font_size=11, color=C_RELAY)
        bid_label3.next_to(relay, UP, buff=0.2)
        self.play(ReplacementTransform(bid_label2, bid_label3), run_time=0.4)
        self.wait(1.0)

        # ============================================================
        # Stage 7: Proposer commits
        # ============================================================
        self.play(
            FadeIn(proposer, shift=UP * 0.2),
            GrowArrow(a_relay_proposer),
            run_time=0.8
        )
        swap_subtitle("The proposer selects the best bid and signs a commitment")

        # Bid flows to proposer
        winning_bid = make_particle(C_RELAY, radius=0.05)
        winning_bid.move_to(relay.get_right())
        self.play(
            MoveAlongPath(winning_bid, Line(relay.get_right(), proposer.get_left())),
            run_time=0.6
        )
        self.play(FadeOut(winning_bid), FadeOut(bid_label3), run_time=0.3)

        # Commitment flash
        commit_flash = RoundedRectangle(
            corner_radius=0.12, width=1.8, height=0.7,
            stroke_color=C_PROPOSER, stroke_width=3, fill_opacity=0
        ).move_to(proposer.get_center())
        self.play(Create(commit_flash), run_time=0.3)
        self.play(FadeOut(commit_flash), run_time=0.5)
        self.wait(1.0)

        # ============================================================
        # Stage 8: Block added to chain
        # ============================================================
        self.play(
            FadeIn(chain, shift=UP * 0.2),
            GrowArrow(a_proposer_chain),
            run_time=0.8
        )
        swap_subtitle("The relay reveals the block. Validators attest. It becomes part of the chain.")
        self.wait(0.5)

        # Block particle flows to chain
        block_p = make_particle(PRIMARY, radius=0.06)
        block_p.move_to(proposer.get_right())
        self.play(
            MoveAlongPath(block_p, Line(proposer.get_right(), chain.get_left())),
            run_time=0.6
        )

        # Chain glow
        chain_glow = chain[0].copy().set_stroke(PRIMARY, width=3, opacity=0.6)
        self.play(
            FadeOut(block_p),
            Create(chain_glow),
            run_time=0.5
        )
        self.play(FadeOut(chain_glow), run_time=0.8)
        self.wait(1.5)

        # ============================================================
        # Slot timer
        # ============================================================
        swap_subtitle("This entire flow happens within a single 12-second slot")

        slot_bar = RoundedRectangle(
            corner_radius=0.06, width=10, height=0.15,
            stroke_color=MUTED, stroke_width=0.5,
            fill_color=SURFACE, fill_opacity=1
        ).shift(DOWN * 2.1)

        slot_fill = RoundedRectangle(
            corner_radius=0.06, width=0.01, height=0.15,
            stroke_width=0, fill_color=SECONDARY, fill_opacity=0.5
        )
        slot_fill.align_to(slot_bar, LEFT).align_to(slot_bar, DOWN)

        slot_label_0 = Text("0s", font=MONO, font_size=10, color=MUTED)
        slot_label_0.next_to(slot_bar, LEFT, buff=0.15)
        slot_label_12 = Text("12s", font=MONO, font_size=10, color=MUTED)
        slot_label_12.next_to(slot_bar, RIGHT, buff=0.15)

        self.play(FadeIn(slot_bar), FadeIn(slot_label_0), FadeIn(slot_label_12), run_time=0.5)
        self.play(
            slot_fill.animate.stretch_to_fit_width(10).align_to(slot_bar, LEFT),
            run_time=3.0,
            rate_func=linear
        )
        self.wait(2.0)

        # ============================================================
        # Fade all
        # ============================================================
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.5)

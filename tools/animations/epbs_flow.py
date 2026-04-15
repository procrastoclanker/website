from manim import *
import numpy as np

BG = "#000000"
PRIMARY = "#e8e8e8"
SECONDARY = "#777777"
MUTED = "#3d3d3d"
MONO = "Monospace"

C_BUILDER = "#88aa88"
C_RELAY = "#aa8888"
C_PROPOSER = "#9988aa"
C_PTC = "#5588aa"
C_PROTOCOL = "#cc9966"
C_DANGER = "#aa5555"


def make_node(label, color, width=2.0, height=0.65):
    rect = RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        stroke_color=color, stroke_width=1.5, fill_color=BG, fill_opacity=1.0
    )
    txt = Text(label, font=MONO, font_size=13, color=color)
    return VGroup(rect, txt)


def make_arrow(start_pt, end_pt, color=MUTED):
    return Arrow(
        start_pt, end_pt,
        buff=0.1, stroke_width=1.5, color=color,
        max_tip_length_to_length_ratio=0.12,
        max_stroke_width_to_length_ratio=2.0,
    )


class EpbsFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Subtitle helper
        sub_bg = RoundedRectangle(
            corner_radius=0.08, width=12, height=0.55,
            fill_color="#0a0a0a", fill_opacity=0.92, stroke_width=0
        ).to_edge(DOWN, buff=0.25)
        current_sub = None

        def swap_sub(text):
            nonlocal current_sub
            sub = Text(text, font=MONO, font_size=12, color=SECONDARY)
            sub.move_to(sub_bg.get_center())
            new = VGroup(sub_bg.copy(), sub)
            if current_sub:
                self.play(FadeOut(current_sub, run_time=0.2),
                          FadeIn(new, run_time=0.2))
            else:
                self.play(FadeIn(new, run_time=0.4))
            current_sub = new

        # ============================================================
        # Part 1: PBS Today
        # ============================================================
        today_label = Text("PBS Today", font=MONO, font_size=22,
                           color=PRIMARY, weight=BOLD)
        today_label.to_edge(UP, buff=0.4)
        self.play(FadeIn(today_label, shift=DOWN * 0.1), run_time=0.7)

        builder1 = make_node("Builder", C_BUILDER)
        relay1 = make_node("Relay", C_RELAY)
        proposer1 = make_node("Proposer", C_PROPOSER)

        builder1.move_to(LEFT * 4)
        relay1.move_to(ORIGIN)
        proposer1.move_to(RIGHT * 4)

        trust_badge = Text("trusted escrow", font=MONO, font_size=9, color=C_RELAY)
        trust_badge.next_to(relay1, DOWN, buff=0.2)

        a1 = make_arrow(builder1.get_right(), relay1.get_left(), C_BUILDER)
        a2 = make_arrow(relay1.get_right(), proposer1.get_left(), C_RELAY)

        swap_sub("Today: relays validate blocks, hold them in escrow, and enforce fair exchange")

        self.play(
            FadeIn(builder1), FadeIn(relay1), FadeIn(proposer1),
            FadeIn(trust_badge),
            GrowArrow(a1), GrowArrow(a2),
            run_time=1.0
        )
        self.wait(2.0)

        # Show flow
        swap_sub("Builder submits block to relay. Relay forwards header + bid. Proposer signs blind.")

        p1 = Dot(radius=0.05, color=C_BUILDER)
        p1.move_to(builder1.get_right())
        block_label = Text("block", font=MONO, font_size=9, color=C_BUILDER)
        block_label.move_to((builder1.get_right() + relay1.get_left()) / 2 + UP * 0.3)
        self.play(
            FadeIn(block_label),
            MoveAlongPath(p1, Line(builder1.get_right(), relay1.get_left())),
            run_time=0.7
        )
        self.play(FadeOut(p1), FadeOut(block_label), run_time=0.2)

        p2 = Dot(radius=0.04, color=C_RELAY)
        p2.move_to(relay1.get_right())
        hdr_label = Text("header + bid", font=MONO, font_size=9, color=C_RELAY)
        hdr_label.move_to((relay1.get_right() + proposer1.get_left()) / 2 + UP * 0.3)
        self.play(
            FadeIn(hdr_label),
            MoveAlongPath(p2, Line(relay1.get_right(), proposer1.get_left())),
            run_time=0.7
        )
        self.play(FadeOut(p2), FadeOut(hdr_label), run_time=0.2)

        # Proposer signs
        sign_flash = proposer1[0].copy().set_stroke(C_PROPOSER, width=3, opacity=0.8)
        self.play(Create(sign_flash), run_time=0.3)
        self.play(FadeOut(sign_flash), run_time=0.4)

        swap_sub("If the relay fails or acts maliciously, the proposer can lose their slot")
        self.wait(2.0)

        # Single point of failure highlight
        fail_label = Text("single point of trust", font=MONO, font_size=10, color=C_RELAY)
        fail_label.next_to(relay1, UP, buff=0.25)
        fail_glow = relay1[0].copy().set_stroke(C_RELAY, width=2.5).set_fill(C_RELAY, opacity=0.12)
        self.play(FadeIn(fail_glow), FadeIn(fail_label), run_time=0.6)
        self.wait(2.0)

        # ============================================================
        # Transition
        # ============================================================
        today_group = Group(
            today_label, builder1, relay1, proposer1,
            trust_badge, a1, a2, fail_glow, fail_label
        )
        self.play(FadeOut(today_group), FadeOut(current_sub), run_time=0.8)
        current_sub = None
        self.wait(0.3)

        # ============================================================
        # Part 2: ePBS
        # ============================================================
        epbs_label = Text("ePBS: Protocol-Enforced", font=MONO, font_size=22,
                          color=PRIMARY, weight=BOLD)
        epbs_label.to_edge(UP, buff=0.4)
        self.play(FadeIn(epbs_label, shift=DOWN * 0.1), run_time=0.7)

        swap_sub("ePBS moves the block auction into the consensus layer")

        # Protocol boundary box
        protocol_box = RoundedRectangle(
            corner_radius=0.2, width=10, height=3.2,
            stroke_color=C_PROTOCOL, stroke_width=1.0, stroke_opacity=0.4,
            fill_color=BG, fill_opacity=0
        ).move_to(DOWN * 0.1)
        protocol_label = Text("consensus protocol", font=MONO, font_size=10,
                              color=C_PROTOCOL)
        protocol_label.next_to(protocol_box, UP, buff=0.08)

        # Nodes
        builder2 = make_node("Builder", C_BUILDER)
        proposer2 = make_node("Proposer", C_PROPOSER)
        ptc = make_node("Payload Timeliness\nCommittee (PTC)", C_PTC, width=3.0, height=0.75)

        builder2.move_to(LEFT * 3 + UP * 0.4)
        proposer2.move_to(RIGHT * 3 + UP * 0.4)
        ptc.move_to(DOWN * 1.0)

        # Two paths: gossip + direct query
        gossip_arrow = make_arrow(
            builder2.get_right() + UP * 0.1,
            proposer2.get_left() + UP * 0.1,
            C_BUILDER
        )
        gossip_label = Text("bids via p2p gossip", font=MONO, font_size=9, color=C_BUILDER)
        gossip_label.move_to(
            (builder2.get_right() + proposer2.get_left()) / 2 + UP * 0.55
        )

        direct_arrow = Arrow(
            proposer2.get_left() + DOWN * 0.1,
            builder2.get_right() + DOWN * 0.1,
            buff=0.1, stroke_width=1.0, color=C_PROPOSER,
            max_tip_length_to_length_ratio=0.12,
            max_stroke_width_to_length_ratio=2.0,
        )
        direct_label = Text("or direct query", font=MONO, font_size=9, color=C_PROPOSER)
        direct_label.move_to(
            (builder2.get_right() + proposer2.get_left()) / 2 + DOWN * 0.35
        )

        # PTC observation arrows
        ptc_arrow1 = DashedLine(
            ptc.get_left() + UP * 0.15, builder2.get_bottom(),
            stroke_width=1, color=C_PTC, dash_length=0.06
        ).add_tip(tip_length=0.12, tip_width=0.08)
        ptc_arrow2 = DashedLine(
            ptc.get_right() + UP * 0.15, proposer2.get_bottom(),
            stroke_width=1, color=C_PTC, dash_length=0.06
        ).add_tip(tip_length=0.12, tip_width=0.08)

        ptc_role = Text("observes + attests to payload delivery",
                        font=MONO, font_size=9, color=C_PTC)
        ptc_role.next_to(ptc, DOWN, buff=0.2)

        self.play(FadeIn(protocol_box), FadeIn(protocol_label), run_time=0.5)
        self.play(
            FadeIn(builder2), FadeIn(proposer2),
            GrowArrow(gossip_arrow), FadeIn(gossip_label),
            run_time=0.8
        )
        self.play(
            GrowArrow(direct_arrow), FadeIn(direct_label),
            run_time=0.5
        )
        self.wait(1.0)

        swap_sub("The Payload Timeliness Committee replaces relay trust")
        self.play(
            FadeIn(ptc), FadeIn(ptc_role),
            Create(ptc_arrow1), Create(ptc_arrow2),
            run_time=0.8
        )
        self.wait(2.0)

        # ============================================================
        # Show the happy path
        # ============================================================
        swap_sub("Builder submits bid. Proposer commits. Builder reveals payload on time.")

        bid = Dot(radius=0.05, color=C_BUILDER)
        bid.move_to(builder2.get_right() + UP * 0.1)
        self.play(
            MoveAlongPath(bid, Line(
                builder2.get_right() + UP * 0.1,
                proposer2.get_left() + UP * 0.1
            )),
            run_time=0.6
        )
        self.play(FadeOut(bid), run_time=0.15)

        # Proposer commits
        commit_flash = proposer2[0].copy().set_stroke(C_PROPOSER, width=3, opacity=0.8)
        self.play(Create(commit_flash), run_time=0.3)
        self.play(FadeOut(commit_flash), run_time=0.3)

        # PTC sees payload in time - checkmark
        ptc_check = Text("payload on time", font=MONO, font_size=10,
                         color=C_PTC, weight=BOLD)
        ptc_check.next_to(ptc, UP, buff=0.15)
        self.play(FadeIn(ptc_check), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(ptc_check), run_time=0.3)

        # ============================================================
        # Show the failure case: builder withholds
        # ============================================================
        swap_sub("What if the builder reveals too late or not at all?")
        self.wait(1.5)

        # X mark on builder
        fail_x1 = Text("payload missing", font=MONO, font_size=10,
                        color=C_DANGER, weight=BOLD)
        fail_x1.next_to(builder2, DOWN, buff=0.25)
        
        # Builder node flashes red
        builder_fail = builder2[0].copy().set_stroke(C_DANGER, width=2.5)
        self.play(FadeIn(fail_x1), Create(builder_fail), run_time=0.5)
        self.wait(1.0)

        swap_sub("The PTC attests: payload not seen. The proposer still gets paid.")

        # PTC attests "not seen"
        ptc_miss = Text("payload NOT seen", font=MONO, font_size=10,
                        color=C_DANGER, weight=BOLD)
        ptc_miss.next_to(ptc, UP, buff=0.15)
        self.play(FadeIn(ptc_miss), run_time=0.4)
        self.wait(1.0)

        # Unconditional payment highlight on proposer
        payment_label = Text("unconditional payment", font=MONO, font_size=12,
                             color=C_PROTOCOL, weight=BOLD)
        payment_label.next_to(proposer2, UP, buff=0.35)
        payment_box = SurroundingRectangle(
            payment_label, corner_radius=0.08, buff=0.1,
            stroke_color=C_PROTOCOL, stroke_width=1.5, fill_opacity=0
        )

        from_label = Text("from builder's on-chain balance", font=MONO, font_size=9,
                          color=C_PROTOCOL)
        from_label.next_to(payment_box, UP, buff=0.08)

        self.play(
            FadeIn(payment_label), Create(payment_box), FadeIn(from_label),
            run_time=0.6
        )
        self.wait(3.0)

        # ============================================================
        # Key takeaway
        # ============================================================
        self.play(
            FadeOut(fail_x1), FadeOut(builder_fail),
            FadeOut(ptc_miss),
            run_time=0.4
        )
        swap_sub("ePBS removes the relay as a trust bottleneck. The protocol enforces the auction.")
        self.wait(3.0)

        # Fade all
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.5)

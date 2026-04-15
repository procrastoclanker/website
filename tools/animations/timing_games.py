from manim import *
import numpy as np

BG = "#000000"
PRIMARY = "#e8e8e8"
SECONDARY = "#777777"
MUTED = "#3d3d3d"
MONO = "Monospace"

C_BID = "#88aa88"
C_DANGER = "#aa5555"
C_PROPOSER = "#9988aa"
C_PRO = "#cc9966"
C_ATTEST = "#5588aa"


class TimingGames(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ============================================================
        # Title
        # ============================================================
        title = Text("Timing Games", font=MONO, font_size=28,
                     color=PRIMARY, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.wait(0.5)

        # ============================================================
        # Subtitle helper
        # ============================================================
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
                self.play(FadeOut(current_sub, run_time=0.25),
                          FadeIn(new, run_time=0.25))
            else:
                self.play(FadeIn(new, run_time=0.4))
            current_sub = new

        # ============================================================
        # Layout: two rows
        # Top: bid curve with timeline
        # Bottom: propagation + attestation bar
        # ============================================================
        ax_left_x = -5.5
        ax_right_x = 5.5
        ax_width = ax_right_x - ax_left_x
        curve_y = 0.2  # baseline of bid curve
        prop_y = -2.2  # baseline of propagation row

        # Slot timeline
        timeline = Line(
            np.array([ax_left_x, curve_y, 0]),
            np.array([ax_right_x, curve_y, 0]),
            stroke_width=1.5, color=MUTED
        )

        # Time labels and ticks
        time_labels = VGroup()
        ticks = VGroup()
        for sec in [0, 2, 4, 8, 12]:
            frac = sec / 12.0
            x = ax_left_x + frac * ax_width
            lbl = Text(f"{sec}s", font=MONO, font_size=11, color=MUTED)
            lbl.move_to(np.array([x, curve_y - 0.3, 0]))
            time_labels.add(lbl)
            tick = Line(
                np.array([x, curve_y - 0.08, 0]),
                np.array([x, curve_y + 0.08, 0]),
                stroke_width=1, color=MUTED
            )
            ticks.add(tick)

        y_label = Text("Bid Value", font=MONO, font_size=11, color=SECONDARY)
        y_label.rotate(PI / 2)
        y_label.next_to(timeline, LEFT, buff=0.7).shift(UP * 1.0)

        self.play(
            Create(timeline), FadeIn(time_labels), FadeIn(ticks), FadeIn(y_label),
            run_time=0.8
        )

        swap_sub("Builders continuously bid throughout the 12-second slot")
        self.wait(1.0)

        # ============================================================
        # Bid value curve
        # ============================================================
        def bid_value(t):
            return 1.8 * (1 - np.exp(-3.5 * t)) + 0.3 * t * t

        def t_to_point(t):
            x = ax_left_x + t * ax_width
            y = curve_y + bid_value(t)
            return np.array([x, y, 0])

        bid_curve = VMobject(stroke_color=C_BID, stroke_width=2.5)
        bid_curve.set_points_smoothly(
            [t_to_point(t / 100.0) for t in range(101)]
        )

        self.play(Create(bid_curve, run_time=3.0, rate_func=linear))
        self.wait(0.5)

        # 4s deadline
        swap_sub("Blocks arriving after ~4s risk missing attestations")
        self.wait(0.3)

        deadline_x = ax_left_x + (4.0 / 12.0) * ax_width
        deadline_line = DashedLine(
            np.array([deadline_x, curve_y, 0]),
            np.array([deadline_x, curve_y + 2.3, 0]),
            stroke_width=1.5, color=C_DANGER, dash_length=0.08
        )
        deadline_label = Text("~4s soft deadline", font=MONO, font_size=10, color=C_DANGER)
        deadline_label.next_to(deadline_line, UP, buff=0.08)

        danger_zone = Polygon(
            np.array([deadline_x, curve_y, 0]),
            np.array([ax_right_x, curve_y, 0]),
            np.array([ax_right_x, curve_y + 2.3, 0]),
            np.array([deadline_x, curve_y + 2.3, 0]),
            fill_color=C_DANGER, fill_opacity=0.05, stroke_width=0
        )

        self.play(
            Create(deadline_line), FadeIn(deadline_label), FadeIn(danger_zone),
            run_time=0.8
        )
        self.wait(1.2)

        # ============================================================
        # Propagation row labels
        # ============================================================
        prop_label = Text("Block propagation + attestation window",
                          font=MONO, font_size=11, color=SECONDARY)
        prop_label.move_to(np.array([0, prop_y + 0.55, 0]))
        
        prop_timeline = Line(
            np.array([ax_left_x, prop_y, 0]),
            np.array([ax_right_x, prop_y, 0]),
            stroke_width=1, color=MUTED
        )

        # 12s end marker on propagation row
        end_marker = DashedLine(
            np.array([ax_right_x, prop_y - 0.15, 0]),
            np.array([ax_right_x, prop_y + 0.4, 0]),
            stroke_width=1, color=MUTED, dash_length=0.06
        )
        end_label = Text("12s", font=MONO, font_size=10, color=MUTED)
        end_label.next_to(end_marker, DOWN, buff=0.08)

        self.play(
            FadeIn(prop_label), Create(prop_timeline),
            Create(end_marker), FadeIn(end_label),
            run_time=0.6
        )
        self.wait(0.5)

        # ============================================================
        # Scenario 1: Solo validator at 1.5s
        # ============================================================
        swap_sub("A solo validator commits at 1.5s -- lower bid, but plenty of time to propagate")
        self.wait(0.5)

        solo_t = 1.5 / 12.0
        solo_x = ax_left_x + solo_t * ax_width
        solo_curve_y = curve_y + bid_value(solo_t)

        # Dot on bid curve
        solo_dot = Dot(np.array([solo_x, solo_curve_y, 0]),
                       radius=0.06, color=C_PROPOSER)
        solo_bid_label = Text("0.019 ETH", font=MONO, font_size=10, color=C_PROPOSER)
        solo_bid_label.next_to(solo_dot, UP + LEFT, buff=0.1)
        solo_name = Text("Solo validator", font=MONO, font_size=10, color=C_PROPOSER)
        solo_name.next_to(solo_dot, RIGHT, buff=0.12).shift(UP * 0.1)

        # Vertical guide line
        solo_guide = DashedLine(
            np.array([solo_x, curve_y, 0]),
            np.array([solo_x, solo_curve_y, 0]),
            stroke_width=1, color=C_PROPOSER, dash_length=0.06
        )

        self.play(
            Create(solo_guide), FadeIn(solo_dot),
            FadeIn(solo_bid_label), FadeIn(solo_name),
            run_time=0.7
        )

        # Propagation bar: from commit time to 12s (available window)
        solo_prop_start = solo_x
        solo_prop_width = ax_right_x - solo_x

        # Propagation segment (green = time for block to spread)
        prop_time = 2.0  # ~2 seconds to propagate
        prop_frac = prop_time / 12.0
        prop_bar_w = prop_frac * ax_width

        solo_prop_bar = Rectangle(
            width=prop_bar_w, height=0.2,
            fill_color=C_PROPOSER, fill_opacity=0.4, stroke_width=0.5,
            stroke_color=C_PROPOSER
        )
        solo_prop_bar.move_to(np.array([solo_prop_start + prop_bar_w / 2, prop_y + 0.2, 0]))
        solo_prop_lbl = Text("propagation", font=MONO, font_size=8, color=C_PROPOSER)
        solo_prop_lbl.move_to(solo_prop_bar.get_center())

        # Attestation window: remaining time after propagation
        attest_start_x = solo_prop_start + prop_bar_w
        attest_width = ax_right_x - attest_start_x

        solo_attest_bar = Rectangle(
            width=attest_width, height=0.2,
            fill_color=C_ATTEST, fill_opacity=0.3, stroke_width=0.5,
            stroke_color=C_ATTEST
        )
        solo_attest_bar.move_to(np.array([attest_start_x + attest_width / 2, prop_y + 0.2, 0]))
        solo_attest_lbl = Text("attestation window", font=MONO, font_size=8, color=C_ATTEST)
        solo_attest_lbl.move_to(solo_attest_bar.get_center())

        # Commit marker on prop row
        solo_commit_mark = Line(
            np.array([solo_x, prop_y - 0.1, 0]),
            np.array([solo_x, prop_y + 0.35, 0]),
            stroke_width=1.5, color=C_PROPOSER
        )

        self.play(
            Create(solo_commit_mark),
            FadeIn(solo_prop_bar), FadeIn(solo_prop_lbl),
            run_time=0.6
        )
        self.play(FadeIn(solo_attest_bar), FadeIn(solo_attest_lbl), run_time=0.5)
        self.wait(2.0)

        # ============================================================
        # Scenario 2: Professional operation at 3.8s
        # ============================================================
        swap_sub("A professional operation waits until 3.8s -- higher bid, but the window shrinks")
        self.wait(0.5)

        # Fade solo propagation bars (keep curve elements)
        solo_prop_group = VGroup(solo_prop_bar, solo_prop_lbl,
                                 solo_attest_bar, solo_attest_lbl,
                                 solo_commit_mark)
        self.play(solo_prop_group.animate.set_opacity(0.2), run_time=0.4)

        pro_t = 3.8 / 12.0
        pro_x = ax_left_x + pro_t * ax_width
        pro_curve_y = curve_y + bid_value(pro_t)

        pro_dot = Dot(np.array([pro_x, pro_curve_y, 0]),
                      radius=0.06, color=C_PRO)
        pro_bid_label = Text("0.048 ETH", font=MONO, font_size=10, color=C_PRO)
        pro_bid_label.next_to(pro_dot, UP + RIGHT, buff=0.1)
        pro_name = Text("Professional op", font=MONO, font_size=10, color=C_PRO)
        pro_name.next_to(pro_dot, RIGHT, buff=0.12).shift(DOWN * 0.15)

        pro_guide = DashedLine(
            np.array([pro_x, curve_y, 0]),
            np.array([pro_x, pro_curve_y, 0]),
            stroke_width=1, color=C_PRO, dash_length=0.06
        )

        self.play(
            Create(pro_guide), FadeIn(pro_dot),
            FadeIn(pro_bid_label), FadeIn(pro_name),
            run_time=0.7
        )

        # Pro propagation bar (same 2s propagation time)
        pro_prop_bar = Rectangle(
            width=prop_bar_w, height=0.2,
            fill_color=C_PRO, fill_opacity=0.4, stroke_width=0.5,
            stroke_color=C_PRO
        )
        pro_prop_bar.move_to(np.array([pro_x + prop_bar_w / 2, prop_y - 0.15, 0]))
        pro_prop_lbl = Text("propagation", font=MONO, font_size=8, color=C_PRO)
        pro_prop_lbl.move_to(pro_prop_bar.get_center())

        # Pro attestation window: much smaller
        pro_attest_start = pro_x + prop_bar_w
        pro_attest_w = ax_right_x - pro_attest_start

        pro_attest_bar = Rectangle(
            width=max(pro_attest_w, 0.01), height=0.2,
            fill_color=C_ATTEST, fill_opacity=0.3, stroke_width=0.5,
            stroke_color=C_ATTEST
        )
        pro_attest_bar.move_to(np.array([pro_attest_start + pro_attest_w / 2, prop_y - 0.15, 0]))
        pro_attest_lbl = Text("attestation", font=MONO, font_size=8, color=C_ATTEST)
        pro_attest_lbl.move_to(pro_attest_bar.get_center())

        pro_commit_mark = Line(
            np.array([pro_x, prop_y - 0.3, 0]),
            np.array([pro_x, prop_y + 0.05, 0]),
            stroke_width=1.5, color=C_PRO
        )

        self.play(
            Create(pro_commit_mark),
            FadeIn(pro_prop_bar), FadeIn(pro_prop_lbl),
            run_time=0.6
        )
        self.play(FadeIn(pro_attest_bar), FadeIn(pro_attest_lbl), run_time=0.5)
        self.wait(1.5)

        # ============================================================
        # Highlight the squeeze
        # ============================================================
        swap_sub("Later commits earn more, but leave less time for the network to finalize the block")
        self.wait(3.0)

        # ============================================================
        # Show the gap on bid curve
        # ============================================================
        swap_sub("This gap creates centralization pressure -- solo validators cannot safely wait as long")

        gap_arrow = DoubleArrow(
            np.array([solo_x - 0.6, solo_curve_y, 0]),
            np.array([solo_x - 0.6, pro_curve_y, 0]),
            buff=0.05, stroke_width=1.5, color=PRIMARY,
            max_tip_length_to_length_ratio=0.1,
        )
        gap_label = Text("2.5x", font=MONO, font_size=14, color=PRIMARY, weight=BOLD)
        gap_label.next_to(gap_arrow, LEFT, buff=0.12)

        self.play(GrowArrow(gap_arrow), FadeIn(gap_label), run_time=0.8)
        self.wait(3.5)

        # ============================================================
        # Fade all
        # ============================================================
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.5)

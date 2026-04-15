from manim import *

# Blockspace Forum monochrome palette
BG = "#000000"
COL_WHITE = "#e8e8e8"
COL_DIM = "#777777"
COL_MUTED = "#3d3d3d"
COL_BRIGHT = "#ffffff"
COL_BG_CARD = "#0a0a0a"
COL_SUB_TEXT = "#b1bac4"
MONO = "DejaVu Sans Mono"

# Builder-specific colors
COL_A = "#8899aa"   # Builder A: blue-grey
COL_B = "#aa8877"   # Builder B: warm brown
COL_B_MERGED = "#997766"  # Builder B txns after merge (slightly dimmer)

MC_BLACK = ManimColor("#000000")
MC_WHITE = ManimColor("#e8e8e8")


def brightness_color(b):
    return interpolate_color(MC_BLACK, MC_WHITE, b)


def make_txn(width, height, color):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.06,
        fill_color=color, fill_opacity=1.0,
        stroke_width=0
    )


def make_block_group(n_txns, width, txn_height, gap, color, label=None):
    txns = VGroup(*[make_txn(width, txn_height, color) for _ in range(n_txns)])
    txns.arrange(DOWN, buff=gap)
    border = SurroundingRectangle(
        txns, corner_radius=0.1, buff=0.08,
        stroke_color=COL_MUTED,
        stroke_width=0.8, fill_opacity=0
    )
    block = VGroup(border, txns)
    if label:
        lbl = Text(label, font_size=16, font=MONO, color=COL_DIM)
        lbl.next_to(block, UP, buff=0.15)
        return VGroup(lbl, block), txns
    return block, txns


def make_subtitle(text):
    txt = Text(text, font_size=16, font=MONO, color=COL_SUB_TEXT)
    if txt.width > 12.5:
        txt.scale(12.5 / txt.width)
    bg = RoundedRectangle(
        width=txt.width + 0.6, height=txt.height + 0.35,
        corner_radius=0.08,
        fill_color=COL_BG_CARD, fill_opacity=0.92,
        stroke_width=0
    )
    bg.move_to(txt.get_center())
    sub = VGroup(bg, txt)
    sub.to_edge(DOWN, buff=0.3)
    return sub


def make_actor_node(label_text, radius=0.45):
    """Circle with label, for operator and proposer."""
    circle = Circle(
        radius=radius, stroke_color=COL_DIM, stroke_width=1.0,
        fill_opacity=0
    )
    label = Text(label_text, font_size=13, font=MONO, color=COL_DIM)
    label.move_to(circle.get_center())
    return VGroup(circle, label)


def make_arrow(start, end, **kwargs):
    """Simple thin arrow."""
    return Arrow(
        start, end,
        stroke_color=kwargs.get("color", COL_MUTED),
        stroke_width=kwargs.get("width", 0.8),
        tip_length=0.15,
        max_tip_length_to_length_ratio=0.15,
        buff=0.1,
    )


class BlockMerging(Scene):
    def construct(self):
        self.camera.background_color = BG

        TXN_W = 1.6
        TXN_H = 0.26
        TXN_GAP = 0.05
        NUM_A = 8
        NUM_B = 6
        CONTENTIOUS_B = 2
        MERGEABLE = NUM_B - CONTENTIOUS_B  # 4

        # Positions
        BLOCK_X = -5.2
        A_Y = 1.6
        B_Y = -1.8
        RELAY_POS = ORIGIN
        PROPOSER_POS = RIGHT * 5.0

        # ══════════════════════════════════════════
        # Phase 1: Two builders assemble blocks
        # ══════════════════════════════════════════

        sub1 = make_subtitle("Two builders assemble blocks for the same slot")
        self.play(FadeIn(sub1), run_time=0.8)

        a_group, a_txns = make_block_group(NUM_A, TXN_W, TXN_H, TXN_GAP, COL_A, "Builder A")
        a_group.move_to(LEFT * abs(BLOCK_X) + UP * A_Y)

        b_group, b_txns = make_block_group(NUM_B, TXN_W, TXN_H, TXN_GAP, COL_B, "Builder B")
        b_group.move_to(LEFT * abs(BLOCK_X) + DOWN * abs(B_Y))

        # Values to the RIGHT of each block
        a_val = Text("0.485 ETH", font_size=13, font=MONO, color=COL_WHITE)
        a_val.next_to(a_group, RIGHT, buff=0.25)

        b_val = Text("0.148 ETH", font_size=13, font=MONO, color=COL_DIM)
        b_val.next_to(b_group, RIGHT, buff=0.25)

        self.play(
            FadeIn(a_group, shift=RIGHT * 0.3),
            FadeIn(a_val, shift=RIGHT * 0.3),
            run_time=1.2
        )
        self.play(
            FadeIn(b_group, shift=RIGHT * 0.3),
            FadeIn(b_val, shift=RIGHT * 0.3),
            run_time=1.2
        )
        self.wait(2.0)

        # ══════════════════════════════════════════
        # Phase 2: Both submit to operator
        # ══════════════════════════════════════════

        sub2 = make_subtitle("Both blocks are submitted to the operator")
        self.play(FadeOut(sub1), FadeIn(sub2), run_time=0.6)

        operator = make_actor_node("operator", radius=0.55)
        operator.move_to(RELAY_POS)
        self.play(FadeIn(operator), run_time=0.8)

        # Arrows from blocks to operator
        arr_a_op = make_arrow(a_group.get_right() + RIGHT * 0.1, operator.get_left() + UP * 0.15)
        arr_b_op = make_arrow(b_group.get_right() + RIGHT * 0.1, operator.get_left() + DOWN * 0.15)

        self.play(GrowArrow(arr_a_op), GrowArrow(arr_b_op), run_time=1.0)
        self.wait(1.5)

        # ══════════════════════════════════════════
        # Phase 3: Operator picks winner
        # ══════════════════════════════════════════

        sub3 = make_subtitle("Operator selects the highest bid")
        self.play(FadeOut(sub2), FadeIn(sub3), run_time=0.6)

        # Brighten operator
        op_circle = operator[0]
        op_label = operator[1]
        self.play(
            op_circle.animate.set_stroke(color=COL_WHITE, width=1.5),
            op_label.animate.set_color(COL_WHITE),
            run_time=0.8
        )

        # Winner badge on A
        winner_badge = Text("winner", font_size=12, font=MONO, color=COL_WHITE)
        winner_badge.next_to(a_val, DOWN, buff=0.15)

        self.play(FadeIn(winner_badge, shift=UP * 0.1), run_time=0.8)
        self.wait(2.0)

        # ══════════════════════════════════════════
        # Phase 4: Identify non-contentious in B
        # ══════════════════════════════════════════

        sub4 = make_subtitle("Non-contentious transactions in Builder B are identified")
        self.play(FadeOut(sub3), FadeIn(sub4), run_time=0.6)

        contentious_txns = [b_txns[i] for i in range(CONTENTIOUS_B)]
        mergeable_txns_list = [b_txns[i] for i in range(CONTENTIOUS_B, NUM_B)]
        mergeable_group = VGroup(*mergeable_txns_list)

        # Contentious fade out, mergeable brighten
        anims = []
        for txn in contentious_txns:
            anims.append(txn.animate.set_opacity(0.15))
        for txn in mergeable_txns_list:
            anims.append(txn.animate.set_fill(
                color=COL_B, opacity=1.0
            ).set_stroke(color=COL_WHITE, width=0.5))
        self.play(*anims, run_time=1.2)

        nc_label = Text("non-contentious", font_size=11, font=MONO, color=COL_DIM)
        nc_label.next_to(b_val, DOWN, buff=0.15)
        self.play(FadeIn(nc_label), run_time=0.6)
        self.wait(2.5)

        # ══════════════════════════════════════════
        # Phase 5: Merge -- operator builds the merged block
        # ══════════════════════════════════════════

        sub5 = make_subtitle("Operator appends non-contentious txns to the winning block")
        self.play(
            FadeOut(sub4), FadeIn(sub5),
            FadeOut(winner_badge), FadeOut(nc_label),
            FadeOut(arr_a_op), FadeOut(arr_b_op),
            run_time=0.6
        )

        # A block slides to right of operator
        merge_pos = RIGHT * 2.2 + UP * 0.8
        self.play(
            a_group.animate.move_to(merge_pos),
            FadeOut(a_val),
            run_time=1.2
        )

        # Swap label
        a_label_obj = a_group[0]
        merged_label = Text("merged block", font_size=16, font=MONO, color=COL_DIM)
        merged_label.move_to(a_label_obj.get_center())
        self.play(ReplacementTransform(a_label_obj, merged_label), run_time=0.7)

        # Arrow from operator to merged block
        arr_op_merge = make_arrow(
            operator.get_right(), a_group[1].get_left(),
            color=COL_DIM, width=1.0
        )
        self.play(GrowArrow(arr_op_merge), run_time=0.6)

        # Fly each mergeable txn from B to appended position
        last_a_txn = a_txns[-1]
        base_y = last_a_txn.get_center()[1] - TXN_H - TXN_GAP

        for i, txn in enumerate(mergeable_txns_list):
            target_y = base_y - i * (TXN_H + TXN_GAP)
            target_pos = np.array([merge_pos[0], target_y, 0])
            self.play(
                txn.animate.move_to(target_pos).set_fill(
                    color=COL_B_MERGED, opacity=1.0
                ).set_stroke(width=0),
                run_time=0.3
            )

        self.wait(0.4)

        # Fade B remains (contentious txns + label + border)
        b_label_obj = b_group[0]
        b_border_obj = b_group[1][0]
        self.play(
            *[FadeOut(t) for t in contentious_txns],
            FadeOut(b_label_obj),
            FadeOut(b_border_obj), FadeOut(b_val),
            run_time=0.7
        )

        # Expand border
        all_merged = VGroup(a_txns, mergeable_group)
        new_border = SurroundingRectangle(
            all_merged, corner_radius=0.1, buff=0.08,
            stroke_color=brightness_color(0.25),
            stroke_width=0.8, fill_opacity=0
        )
        old_border = a_group[1][0]
        self.play(ReplacementTransform(old_border, new_border), run_time=0.8)

        append_label = Text(
            "+" + str(MERGEABLE) + " txns appended",
            font_size=11, font=MONO, color=COL_DIM
        )
        append_label.next_to(new_border, RIGHT, buff=0.2)
        self.play(FadeIn(append_label), run_time=0.5)
        self.wait(1.5)

        # ══════════════════════════════════════════
        # Phase 6: Proposer receives merged block
        # ══════════════════════════════════════════

        sub6 = make_subtitle("Operator delivers the merged block to the proposer")
        self.play(FadeOut(sub5), FadeIn(sub6), FadeOut(append_label), run_time=0.6)

        # Dim operator
        self.play(
            op_circle.animate.set_stroke(color=COL_MUTED, width=0.8),
            op_label.animate.set_color(COL_MUTED),
            FadeOut(arr_op_merge),
            run_time=0.5
        )

        # Proposer appears
        proposer = make_actor_node("proposer", radius=0.55)
        proposer.move_to(PROPOSER_POS)
        self.play(FadeIn(proposer, shift=LEFT * 0.3), run_time=0.8)

        # Arrow from merged block to proposer
        arr_to_proposer = make_arrow(
            new_border.get_right() + RIGHT * 0.05,
            proposer.get_left(),
            color=COL_DIM, width=1.0
        )
        self.play(GrowArrow(arr_to_proposer), run_time=0.8)
        self.wait(1.5)

        # ══════════════════════════════════════════
        # Phase 7: Benefit
        # ══════════════════════════════════════════

        sub7 = make_subtitle("Multiple builders contribute to the same block")
        self.play(FadeOut(sub6), FadeIn(sub7), run_time=0.6)

        self.wait(1.5)

        # User benefit message
        sub8 = make_subtitle("Transactions that would have waited get included this slot")
        self.play(FadeOut(sub7), FadeIn(sub8), run_time=0.6)

        # Highlight the appended txns with a brief pulse
        pulse_anims = []
        for txn in mergeable_txns_list:
            pulse_anims.append(txn.animate.set_fill(
                color=COL_B, opacity=1.0
            ))
        self.play(*pulse_anims, run_time=0.6)

        user_label = Text("faster inclusion for users", font_size=13, font=MONO, color=COL_WHITE)
        user_label.next_to(new_border, DOWN, buff=0.25)
        self.play(FadeIn(user_label, shift=UP * 0.1), run_time=1.0)

        self.wait(1.5)

        # Settle the pulse back
        settle_anims = []
        for txn in mergeable_txns_list:
            settle_anims.append(txn.animate.set_fill(
                color=COL_B_MERGED, opacity=1.0
            ))
        self.play(*settle_anims, run_time=0.5)

        self.wait(3.0)

        # ══════════════════════════════════════════
        # Fade out
        # ══════════════════════════════════════════
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.5)


# STORYBOARD: "What a Log Actually Is" (16:9, 1920x1080, 30 fps)

Take ids (t01..t42) match `script.json`. Anchor every cue to a take start/end from `voice/timing.json`, plus an offset, or to a spoken word from `out/words/full.json`. Never use absolute seconds.

## 0. Global rules (apply to every section)

**Frame.** Manim default 16:9 frame (14.222 x 8 units). Keep content inside x in [-6.4, 6.4], y in [-2.8, 3.7]. The band y < -2.9 is reserved for burned-in captions: keep it EMPTY.

**Colors (consistent meaning, teach the viewer the language).**
- YELLOW = the log value / the answer / key highlight
- BLUE = base 2, "x2" doubling marks, paper layers
- GREEN = results, "+1", "x10"
- RED/ORANGE = the huge-number side
- WHITE = normal text, GRAY = minor/helper
- Background black.

**Text.** Font "Segoe UI" (fallback "Arial"), bold for headlines. Only `Text` objects, no LaTeX. Sizes: main words/equations 64 to 120, labels 40 minimum, NOTHING below 36. Subscripts and exponents are built with the helpers `log_label(base, arg)` and `pow_label(base, exp)` (small separate Text objects), never with unicode sub/superscript characters. The characters x (as "×"), "≈", "→" are allowed. "≈" must always be shown where a value is approximate.

**Motion.** Something visibly changes at least every 1.5 s. No frozen picture longer than 2.0 s (exception: the last 1.0 s). Reveal items as they are spoken, use small pulses, slow 3% zooms on long still moments. Use smooth transitions between sections (0.4 s crossfade or slide), never hard cuts. No decorative clutter, no music, no external assets (draw every icon from primitives).

**On-screen text rule.** ONLY the text in quotes below may appear. Nothing else, no extra numbers or claims. No mention of binary search, merge sort, sorting, or "subscribe".

**Recurring objects (build once in `common.py`, reuse):**
- `PaperStack(n_layers)`: stack of thin blue rectangles (layers) next to a white sheet. Its height grows with layers (scaled, exaggerated, not to scale).
- `MoonIcon()`: gray circle with 3 darker craters.
- `ruler(...)` and `bar_chart(...)` helpers.

---

## S1 HOOK (t01 to t04). Goal: the viewer must NEED the answer.

**t01** "How many times would you have to fold a sheet of paper to reach the Moon?"
- Start with a white sheet (2.2 x 3.0) at (-4.5, 0.4), the MoonIcon at (5.2, 2.0), a dotted line between them.
- Top-left counters: "Folds: 0" (white, 56) and "Thickness: 0.1 mm" (white, 48).
- At the word "fold": the sheet folds in half and becomes a stack. Counter steps from 1 to 7, one step every ~0.45 s, with thickness 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8 mm (see F16). Show "mm" always.
- The stack grows visibly and the dotted line to the Moon stays long.

**t02** "Take a guess. Thousands? Millions?"
- Counters change to "Folds: ?" and "Thickness: ?" (pulse).
- At "Thousands": chip "1,000?" pops in near the dotted line (orange rounded box). At "Millions": chip "1,000,000?" pops in.

**t03** "The real answer is far smaller, and finding it takes one tool: a log."
- At "far smaller": both chips shrink and slide away (0.3 s).
- At "a log": big yellow "log" pops at (0, 0.4), font 140, with a small pulse.

**t04** "By the end of this video, you'll work it out in your head. No calculator."
- At "work it out": yellow "log" shrinks to the top-left corner, the stack and Moon fade.
- At "No calculator": a calculator icon (rounded rectangle + 6 small key squares) appears with a red X over it and the text "No calculator" (white, 64). Hold under 1.5 s, then crossfade out at the end of the take.

---

## S2 IDEA (t05 to t15)

**t05** "A sheet of paper is about a tenth of a millimeter thick."
- Side view: one thin blue rectangle (the sheet) in the middle. A bracket beside it labeled "0.1 mm" (white, 56). Slow 3% zoom.

**t06** "Fold it once... two layers. Fold again, four. Then eight, sixteen, thirty-two."
- Layers double on screen one per spoken number: 2, 4, 8, 16, 32 (the stack widens into a grid of thin blue bars or tiles). Big counter "2", "4", "8", "16", "32" pops at each spoken number (blue, 100), previous number fades.

**t07** "Every fold doubles the thickness. After any number of folds, the stack is two multiplied by itself that many times."
- At "doubles": arrow "×2" (blue, 72) between two stack sizes. At "two multiplied by itself": the row "2 × 2 × 2 × 2" (blue tiles) builds one tile per spoken "two"/beat, then the label "folds" under it with a bracket.

**t08** "Now flip the question... ask how many doublings it takes to reach a target."
- Left: "How thick?" (white, 72) crossed through with a swipe; right: "How many doublings?" (yellow, 72) wipes in. A target flag icon at the right end of a doubling row of tiles.

**t09** "That's a log. A log answers one question: how many times do I multiply?"
- Big yellow "log" (140) at center, then at "how many times do I multiply" the line "How many times do I multiply?" writes under it (white, 72). Pulse the "×" in a small tile.

**t10** "Take eight... Two times two times two. Three twos. So log base two of eight is three."
- At "Take eight": big white "8" (200) at (0, 2.3).
- At "How many twos": the row of tiles starts: blue tile "2" at (-3, -0.2).
- At each "two" in "Two times two times two": the tiles pop in one by one: "2" "×" "2" "×" "2" (each pop 0.25 s). The "8" shrinks into a green tile "= 8" at the right end of the row.
- At "Three twos": a yellow bracket under the three 2-tiles and a big yellow "3" below.
- At "log base two of eight is three": equation `log_label(2, 8)` + " = 3" at (0, -2.0), above the caption band; the "3" is yellow. Each part flashes as spoken.

**t11** "Same idea with tens. A thousand is ten times ten times ten, so log base ten of a thousand is three."
- Previous row fades. New row (orange/red tiles) "10 × 10 × 10 = 1,000" builds one tile per "ten". Then equation `log_label(10, 1,000)` + " = 3" (the "3" yellow) with the base "10" in blue like the "2" before.

**t12** "That's the whole definition. A log counts multiplications. It's the exponent."
- Show `pow_label(2, 3)` + " = 8" and below `log_label(2, 8)` + " = 3" with a double arrow between, both 3s highlighted yellow. At "the exponent": yellow label "the exponent" with an arrow to the 3.

**t13 (CHALLENGE, pause 1.6 s)** "Pause and try one. What is log base two of thirty-two?"
- Clear to black. At "What is": big `log_label(2, 32)` + " = ?" (yellow "?") at (0, 1.2), font 120.
- At the take end and during its 1.6 s pause: a countdown ring (circle outline that drains) with "3", "2", "1" (one per ~0.5 s) at (0, -1.0). This keeps motion during the pause.

**t14** "Five. Two times two times two times two times two is thirty-two."
- "?" turns into yellow "5" (pulse). Row of five blue tiles pops in one per spoken "two": "2 × 2 × 2 × 2 × 2" then "= 32" green tile. Scale the row to fit width 12.

**t15** "So our paper problem is a log. How many doublings make the stack reach the Moon? Hold that thought."
- Crossfade back to the hook scene: the stack + MoonIcon + dotted line, counters "Folds: ?". At "Hold that thought": the yellow "log" pulses once and a "?" tile pulses near the Moon. End of section: 0.4 s crossfade to the graph scene.

---

## S3 GRAPH (t16 to t21). All axes are square: `Axes(x_range=[0,8,1], y_range=[0,8,1], x_length=6, y_length=6)`, `include_numbers=False`, tick labels written with Text (size 40).

**t16** "Let's draw it. Folds along the bottom, layers up the side..."
- Axes at center-left. Axis labels "folds" (x) and "layers" (y). Ticks 0, 1, 2, 3 on x; 1, 2, 4, 8 on y.
- Plot y = 2^x for x in [0, 3] (blue, stroke 8), drawn over the take. Dots at (0,1), (1,2), (2,4), (3,8) appear one at a time as the curve passes them. Label "exponential growth" (white, 48) appears at "That's exponential growth".

**t17** "Now swap the axes... This is the graph of a log."
- At "swap the axes": axis labels swap ("layers" bottom, "folds" side) with a quick flip animation. A dashed gray diagonal line y = x draws in.
- The curve is reflected: use `curve.copy().apply_function(lambda p: axes.c2p(*axes.p2c(p)[::-1]))` into a yellow curve, y = log2(x) for x in [1, 8]. At "the graph of a log": label `log_label(2, "x")` (yellow, 64) appears near the curve.

**t18** "Watch how it behaves. It shoots up at first, then flattens. And every time the number doubles, the log goes up by exactly one."
- Re-draw the yellow curve slowly (a tracer dot runs along it). The dot speeds visually up then flattens (it is just the curve). At "exactly one": a green "+1" appears beside the y-axis.

**t19** "One to two, one step. Two to four... Eight to sixteen, one more."
- Extend axes to x_range [0, 17, 4] (smoothly rescale; keep square-ish). Dots at x = 1, 2, 4, 8, 16 (y = 0, 1, 2, 3, 4) appear one per spoken pair; tick labels "1", "2", "4", "8", "16" under the axis and "0".."4" on the side. Between consecutive dots: a blue "×2" under the x-axis and a green "+1" beside the y-axis (4 steps, ~1 s each, synced to the spoken pairs).

**t20** "It never stops climbing, but it climbs incredibly slowly... one to a million... about twenty."
- Rescale view: Axes x_range [0, 1_000_000], y_range [0, 22]. Draw the curve parametric: `axes.c2p(2**u, u)` for u in [0, log2(1_000_000)] (do NOT sample evenly in x). Dots at x = 16, 1,024 and 1,000,000 with labels "16 → 4", "1,024 → 10", "1,000,000 → ≈ 20" (keep inside the frame, labels near the end placed left of the dot). The last dot pulses at "about twenty".

**t21** "The two curves are mirror images across a diagonal line. A log is the undo button for an exponent."
- Back to the square axes (0 to 8). Both curves visible (blue exponential, yellow log) with the dashed diagonal. At "mirror images": the blue curve flips onto the yellow one (replay the reflection, 1.5 s). At "undo button": text "undo" (white, 72) with a curved arrow from the yellow curve back to the blue. Crossfade out.

---

## S4 PATTERN (t22 to t29)

**t22** "Now here's something strange... Look at just the first digit of each one."
- A scrolling grid of real-looking numbers (white, 56): populations, lengths, prices written as plain numbers such as 8,336,817 / 6,650 / 19.99 / 1,412,600. No units text. The first digit of each number is highlighted yellow as the narrator says "first digit".

**t23** "You'd expect the digits one through nine to show up about equally, roughly eleven percent each."
- A bar chart: digits 1..9 on the x-axis (labels white 48), nine equal bars (gray) at 11.1%. One label "11%" (white, 56) above the bars. (No other numbers.)

**t24** "But they don't. The digit one leads about thirty percent of the time. The digit nine? Under five."
- The bars morph to Benford heights (values from F06) with a spring. At "one": bar 1 turns yellow with the label "30%" (see F06: 30.1). At "nine": bar 9 turns red with the label "under 5%" (F06: 4.6). Pulse each as spoken.

**t25** "In 1881, an astronomer named Simon Newcomb... first pages were far more worn than the last."
- Draw a closed book from primitives (rectangle with spine). At "1881": text "1881" (yellow, 100). At "Simon Newcomb": text "Simon Newcomb" (white, 64). At "first pages... far more worn": the book opens; the first pages are tinted brown/gray and darker (worn), the last pages stay clean white. A small label "logarithm tables" (white, 48).

**t26** "He guessed that people were looking up numbers starting with one far more often. And the reason is hiding in a log."
- A finger-pointer (primitive hand = circle + rectangle) taps the early pages repeatedly (dots appear on them). At "hiding in a log": the yellow word "log" glows and pulses.

**t27** "Picture a log ruler... from one to two takes up about thirty percent... from nine to ten? Under five percent."
- Horizontal ruler from 1 to 10 (width 11) with ticks at 1,2,...,10 placed at log10 positions. Label "log ruler" (white, 56). At "one to two": the 1→2 segment lights up yellow and a bracket labeled "30%" (F07: 30.1). At "nine to ten": the 9→10 segment lights up red (tiny) and the bracket labeled "under 5%" (F07: 4.6).

**t28** "Think of something growing by a steady percentage each year. Going from a thousand to two thousand takes more than six times as long..."
- Exponential growth curve (green) with y-axis ticks 1,000, 2,000, 9,000, 10,000 (labels size 40). Two horizontal time bars below the axis: a long bar for "1,000 → 2,000" and a short bar for "9,000 → 10,000". At "more than six times": the long bar is shown 6.6x the short bar (draw to scale, F08) with the label "≈ 6.6×" (green, 72). At "starting with a one": the numbers 1,000 ... 1,999 highlight in yellow along the curve.

**t29** "Auditors use this to spot fake data... it can't prove fraud. It just raises a flag."
- Two bar charts side by side: left "real data" follows the Benford shape (yellow bar 1 tall), right "invented data" is flat-ish (gray bars). A red flag icon (triangle on a pole) pops on the right chart. At "can't prove fraud": text "a flag, not proof" (white, 64) with a small gray "?" — no other claims. Crossfade out.

---

## S5 SCALES (t30 to t34)

**t30** "That log ruler shows up wherever we need to squash a huge range into small numbers."
- The log ruler from t27 returns; at "squash": two inward arrows press a long orange bar (labeled "1,000,000") into a small yellow tile "≈ 20" with a bounce. (Not to scale; do not claim it is.)

**t31** "Earthquakes... ten times bigger waves on a seismograph, and about thirty-two times more energy. So a magnitude seven is a hundred times bigger than a five."
- Two seismograph traces (np.random.seed(7), deterministic), each width 6.4: "Magnitude 5" with max amplitude exactly 0.15 and "Magnitude 6" with max amplitude exactly 1.5 (ratio 10, F17), drawn left to right. At "ten times bigger": a green brace between them labeled "10× bigger". At "thirty-two times more energy": small green text "≈ 32× energy". At "seven is a hundred times bigger than a five": the traces fade and a ladder replaces them: three tiles "5", "6", "7" with arrows "×10" between each pair and a bracket from "5" to "7" labeled "×100" (green).

**t32** "Acidity. On the pH scale, each step down is ten times more acidic. A pH of three is a thousand times more acidic than a pH of six."
- Label "pH" (white, 72). A row of tiles "6", "5", "4", "3" colored green to red, left to right. At "each step down": an arrow slides along the row, with "×10" (green) popping between each pair. At "a thousand times": a bracket from "6" to "3" labeled "1,000×" (red).

**t33** "And sound. Every ten decibels means ten times more sound intensity. A whisper is about thirty decibels, a jet engine up close about one hundred forty..."
- Label "Sound" with a small "decibels" under it. A vertical dB bar with two markers: "30 dB" (whisper icon: small circle + a thin wave) and "140 dB" (jet icon: simple triangle plane silhouette). At "ten decibels": a ladder step "+10 dB = ×10". At "a hundred billion": the text "100,000,000,000×" (orange, 72) appears between the markers with a bracket (F11).

**t34** "Same trick every time. A step on the ruler isn't adding. It's multiplying."
- Montage: the three scales stack as three mini-rulers (quake, pH, sound) with tiles. At "isn't adding": a gray "+" is crossed out; at "multiplying": a blue "×" pulses on every ruler. Crossfade out.

---

## S6 PAYOFF (t35 to t42). Reveal the answer slowly; "42" is hidden until t40.

**t35** "Now let's pay off that promise. How many folds to reach the Moon?"
- Return to the hook scene look: stack + Moon, counters "Folds: ?". The yellow "log" tile appears and pulses. Question text "Folds to the Moon?" (white, 72) at the top.

**t36** "The Moon is about three hundred eighty-four thousand kilometers away... about three point eight trillion times thicker."
- Text "Moon: ≈ 384,400 km" (white, 64) with the Moon icon; "Paper: ≈ 0.1 mm" with the sheet. Then "stack must grow ≈ 3.8 trillion ×" (orange, 80). Always write it as "≈ 3.8 trillion ×".

**t37** "Here's the mental trick. Two to the power of ten is one thousand twenty-four. Call it a thousand."
- `pow_label(2, 10)` + " = 1,024" (white/blue), then "≈ 1,000" (orange) appears with a rounding animation.

**t38** "So ten doublings is about a thousand. Twenty is about a million. Thirty, a billion. Forty, about a trillion."
- A ladder builds upward, one row per spoken number: "10 folds ≈ 1,000", "20 folds ≈ 1,000,000", "30 folds ≈ 1,000,000,000", "40 folds ≈ 1,000,000,000,000" (the "≈" is always shown). Beside each row the REAL stack height from F14 (small gray, size 40): "10 cm", "105 m", "107 km", "110,000 km" (matches 102.4 mm, 104.9 m, 107.4 km, 109,951 km).

**t39** "Forty doublings gets us about a trillion, still short. Forty-one isn't enough. But forty-two is a little over four trillion, and that's enough."
- Moon marker bar at "384,400 km" on a vertical distance scale (log-style, no claim of linear scale). At "still short": the 40-fold marker (110,000 km) stops under the Moon line (red "short"). At "Forty-one isn't enough": a marker at 220,000 km, still under the line. At "forty-two": the marker jumps to 440,000 km above the Moon line, turns green. Do NOT show the number 42 yet as a big word; show only the marker values "110,000 km", "220,000 km", "440,000 km" (F14, F15).

**t40** "Forty-two folds. The same answer a calculator gives, worked out in your head."
- Big yellow "42" (200) slams in at the center with a pulse; below it "folds" (white, 72). The stack and Moon animate as the stack passes the Moon.

**t41** "Of course, a normal sheet only folds about seven or eight times by hand. The record is twelve... Britney Gallivan... over a kilometer of toilet paper. But the math doesn't care..."
- Left: a small paper icon with the text "by hand: about 7 to 8" (white, 56). Middle: at "The record is twelve": big "12" (yellow, 140) and the text "Britney Gallivan" (white, 64), "2002". At "over a kilometer of toilet paper": a long thin paper roll drawn as a spiral/strip with the label "over 1 km" (white, 56). At "the math doesn't care": the yellow "log" appears at the right with a pulse.

**t42** "A log just counts how many times you multiply. Forty-two doublings, and a sheet of paper reaches the Moon."
- Final frame: top row tiles "2 × 2 × 2 = 8", below `log_label(2, 8)` + " = 3", and the Moon icon with the "42" tile near it. At each spoken "multiply" and at the end, the "×" signs pulse in sequence. Hold the last frame 1.0 s (the `extra_hold_s`). No subscribe text, no end card.

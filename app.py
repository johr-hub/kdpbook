"""
KDP Activity Book Generator - Interactive Web App
File: app.py
"""

import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import random
import io

# ============================================================
# 1. PAGE SETTINGS & THEMES
# ============================================================
PAGE_W, PAGE_H = letter
MARGIN_X = 0.75 * inch  # KDP safe margin
GRID_SIZE = 15

THEMES = {
    "Nostalgia": [
        "RADIO", "RECORD", "TELEVISION", "DANCE", "MUSIC", "FAMILY", "FRIENDS",
        "SCHOOL", "PICNIC", "SUMMER", "HOLIDAY", "POSTCARD", "LETTER", "CAMERA",
        "MEMORY", "DINNER", "NEIGHBOR", "SMILE", "LAUGHTER", "HOME", "ANTIQUE",
        "PHONOGRAPH", "SCRAPBOOK", "KEEPSAKE", "PORCH", "GARDEN", "BAKING", "SUNDAY"
    ],
    "1950s": [
        "JUKEBOX", "DINER", "VINYL", "ROCKNROLL", "TELEVISION", "DRIVEIN",
        "MILKSHAKE", "RADIO", "DANCE", "MUSIC", "CAR", "SODA", "BASEBALL",
        "PICNIC", "SCHOOL", "BOWLING", "HOTROD", "BOBBYSOX", "SOCKHOP"
    ],
    "1960s": [
        "BEATLES", "FLOWERPOWER", "VINYL", "RADIO", "DANCE", "MUSIC", "TELEVISION",
        "CAMERA", "SUMMER", "PICNIC", "SCHOOL", "FAMILY", "FRIENDS", "RECORD",
        "GUITAR", "CONCERT", "POSTCARD", "HOLIDAY", "CAR", "MEMORY"
    ],
    "Classic Cars": [
        "MUSTANG", "CORVETTE", "CAMARO", "CADILLAC", "CHEVY", "FORD", "PONTIAC",
        "DODGE", "BUICK", "CHRYSLER", "MERCURY", "LINCOLN", "OLDSMOBILE", "PLYMOUTH",
        "COUPE", "SEDAN", "CONVERTIBLE", "ENGINE", "GARAGE", "ROADSTER"
    ],
    "Gardening": [
        "GARDEN", "FLOWER", "ROSE", "TULIP", "DAISY", "SUNFLOWER", "LAVENDER",
        "BASIL", "MINT", "TOMATO", "CARROT", "PEPPER", "POTATO", "SEED",
        "SOIL", "WATER", "SHOVEL", "TROWEL", "PRUNER", "HARVEST", "BLOSSOM"
    ],
    "Travel": [
        "TRAVEL", "VACATION", "AIRPORT", "TRAIN", "HOTEL", "BEACH", "MOUNTAIN",
        "MAP", "CAMERA", "SUITCASE", "PASSPORT", "TICKET", "CRUISE", "ROAD",
        "HIGHWAY", "JOURNEY", "TRIP", "POSTCARD", "TOUR", "ADVENTURE"
    ],
    "Food & Cooking": [
        "APPLE", "BREAD", "BUTTER", "CHEESE", "COFFEE", "COOKIE", "DINNER",
        "SOUP", "SALAD", "PIZZA", "PASTA", "CHICKEN", "POTATO", "CARROT",
        "CAKE", "PIE", "CANDY", "LEMON", "ORANGE", "BREAKFAST", "PANCAKE"
    ],
    "Family & Home": [
        "FAMILY", "MOTHER", "FATHER", "SISTER", "BROTHER", "GRANDMA", "GRANDPA",
        "COUSIN", "UNCLE", "AUNT", "BABY", "CHILD", "HOME", "DINNER",
        "HOLIDAY", "BIRTHDAY", "MEMORY", "LAUGHTER", "SMILE", "LOVE"
    ]
}

SCRAMBLE_WORDS_POOL = [
    "GARDEN", "FLOWER", "RADIO", "CAMERA", "FAMILY", "HOLIDAY", "COFFEE",
    "MUSIC", "TRAVEL", "MEMORY", "SUMMER", "DINNER", "FRIEND", "SPRING",
    "WINTER", "AUTUMN", "NATURE", "SUNDAY", "PICNIC", "RECORD", "SCHOOL",
    "CASTLE", "ISLAND", "SUNSHINE", "STREAM", "VALLEY", "FOREST", "MEADOW",
    "COTTAGE", "HARBOR", "SUNSET", "MORNING", "TEAPOT", "LANTERN", "GUITAR"
]

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]

# ============================================================
# 2. GENERATION ENGINES
# ============================================================
def can_place(grid, word, row, col, dr, dc):
    for i, char in enumerate(word):
        r, c = row + dr * i, col + dc * i
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE): return False
        if grid[r][c] not in ("", char): return False
    return True

def generate_word_search(words_pool):
    words = list(dict.fromkeys(words_pool))
    if len(words) > 15:
        words = random.sample(words, 15)
    words = sorted(words, key=len, reverse=True)

    for _ in range(1500):
        grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        placements = []
        success = True

        for word in words:
            candidates = []
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    for dr, dc in DIRECTIONS:
                        if can_place(grid, word, row, col, dr, dc):
                            overlap = sum(grid[row + dr * i][col + dc * i] == char for i, char in enumerate(word))
                            candidates.append((overlap, random.random(), row, col, dr, dc))
            if not candidates:
                success = False
                break
            candidates.sort(reverse=True)
            best = candidates[:min(40, len(candidates))]
            _, _, row, col, dr, dc = random.choice(best)
            for i, char in enumerate(word):
                grid[row + dr * i][col + dc * i] = char
            placements.append((word, row, col, dr, dc))

        if success:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if not grid[r][c]:
                        grid[r][c] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            return grid, placements
    raise RuntimeError("Word Search generation failed.")

def generate_sudoku(difficulty="easy"):
    base, side = 3, 9
    pattern = lambda r, c: (base * (r % base) + r // base + c) % side
    rows = [g * base + x for g in random.sample(range(base), base) for x in random.sample(range(base), base)]
    cols = [g * base + x for g in random.sample(range(base), base) for x in random.sample(range(base), base)]
    nums = random.sample(range(1, 10), 9)

    solved = [[nums[pattern(r, c)] for c in cols] for r in rows]
    puzzle = [row[:] for row in solved]

    removals = {"easy": 38, "medium": 46, "hard": 54}.get(difficulty.lower(), 38)
    cells = [(r, c) for r in range(9) for c in range(9)]
    for r, c in random.sample(cells, removals):
        puzzle[r][c] = 0
    return puzzle, solved

def scramble_word(word):
    chars = list(word)
    for _ in range(50):
        random.shuffle(chars)
        res = "".join(chars)
        if res != word: return res
    return word[::-1]

# ============================================================
# 3. DRAWING HELPERS
# ============================================================
def start_page(c, page_number, title, subtitle, book_title):
    c.setFont("Helvetica-Bold", 19)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.65 * inch, title)
    if subtitle:
        c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 1.00 * inch, subtitle)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(PAGE_W / 2, 0.42 * inch, f"{book_title}  •  Page {page_number}")

def draw_cover(c, page_number, book_title):
    start_page(c, page_number, book_title.upper(), "LARGE PRINT ACTIVITY BOOK", book_title)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.8 * inch, "Brain Games & Puzzles")
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.2 * inch, "Specially formatted for seniors & adults")
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 0.3 * inch, "Word Search • Sudoku • Word Scramble")

def draw_section_divider(c, page_number, title, subtitle, book_title):
    start_page(c, page_number, title.upper(), subtitle, book_title)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.2 * inch, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 0.25 * inch, subtitle)

def draw_word_search_page(c, page_number, pnum, theme, grid, placements, book_title):
    start_page(c, page_number, f"WORD SEARCH {pnum:02d}", f"THEME: {theme.upper()}", book_title)
    left, bottom, size = 0.85 * inch, 3.35 * inch, 6.80 * inch
    cell = size / GRID_SIZE
    c.setLineWidth(0.65)
    c.rect(left, bottom, size, size)
    for i in range(1, GRID_SIZE):
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)
    c.setFont("Helvetica-Bold", 14)
    for r in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (GRID_SIZE - 1 - r) * cell + cell / 2 - 4.5, grid[r][col])
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN_X, 3.00 * inch, "FIND THESE WORDS:")
    c.setFont("Helvetica", 10.5)
    words = sorted([item[0] for item in placements])
    columns = [MARGIN_X, 3.25 * inch, 5.75 * inch]
    for i, w in enumerate(words):
        c.drawString(columns[i // 5], 2.70 * inch - (i % 5) * 0.32 * inch, w)

def draw_word_search_answer(c, page_number, pnum, theme, grid, placements, book_title):
    start_page(c, page_number, f"ANSWER KEY: WORD SEARCH {pnum:02d}", theme.upper(), book_title)
    left, bottom, size = 1.0 * inch, 3.15 * inch, 6.50 * inch
    cell = size / GRID_SIZE
    c.setLineWidth(0.5)
    c.rect(left, bottom, size, size)
    for i in range(1, GRID_SIZE):
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)
    # Highlight
    c.saveState()
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(cell * 0.72)
    c.setLineCap(1)
    for word, r, col, dr, dc in placements:
        er, ec = r + dr * (len(word) - 1), col + dc * (len(word) - 1)
        c.line(left + col * cell + cell / 2, bottom + (GRID_SIZE - 1 - r) * cell + cell / 2,
               left + ec * cell + cell / 2, bottom + (GRID_SIZE - 1 - er) * cell + cell / 2)
    c.restoreState()
    c.setFont("Helvetica-Bold", 11)
    for r in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (GRID_SIZE - 1 - r) * cell + cell / 2 - 4, grid[r][col])

def draw_sudoku_page(c, page_number, pnum, puzzle, diff, book_title):
    start_page(c, page_number, f"SUDOKU {pnum:02d}", f"{diff.upper()} • LARGE PRINT", book_title)
    left, bottom, size = 1.05 * inch, 3.05 * inch, 6.40 * inch
    cell = size / 9
    c.setLineWidth(1.4)
    c.rect(left, bottom, size, size)
    for i in range(1, 9):
        c.setLineWidth(1.4 if i % 3 == 0 else 0.5)
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)
    c.setFont("Helvetica-Bold", 18)
    for r in range(9):
        for col in range(9):
            if puzzle[r][col]:
                c.drawCentredString(left + col * cell + cell / 2, bottom + (8 - r) * cell + cell / 2 - 6, str(puzzle[r][col]))

def draw_sudoku_answer(c, page_number, pnum, sol, book_title):
    start_page(c, page_number, f"ANSWER KEY: SUDOKU {pnum:02d}", "COMPLETED SOLUTION", book_title)
    left, bottom, size = 1.05 * inch, 3.05 * inch, 6.40 * inch
    cell = size / 9
    c.setLineWidth(1.0)
    c.rect(left, bottom, size, size)
    for i in range(1, 9):
        c.setLineWidth(1.4 if i % 3 == 0 else 0.5)
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)
    c.setFont("Helvetica-Bold", 14)
    for r in range(9):
        for col in range(9):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (8 - r) * cell + cell / 2 - 5, str(sol[r][col]))

def draw_scramble_page(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"WORD SCRAMBLE {pnum:02d}", "UNSCRAMBLE EACH WORD", book_title)
    y = PAGE_H - 1.50 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Unscramble the letters to find the word:")
    y -= 0.50 * inch
    c.setFont("Helvetica", 14)
    for idx, w in enumerate(words):
        c.drawString(MARGIN_X + 0.25 * inch, y, f"{idx + 1}.   {scramble_word(w)}")
        c.line(MARGIN_X + 2.5 * inch, y - 2, PAGE_W - MARGIN_X - 0.5 * inch, y - 2)
        y -= 0.50 * inch

def draw_scramble_answer(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"ANSWER KEY: SCRAMBLE {pnum:02d}", "SOLUTIONS", book_title)
    y = PAGE_H - 1.50 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Unscrambled Solutions:")
    y -= 0.50 * inch
    c.setFont("Helvetica", 13)
    for idx, w in enumerate(words):
        c.drawString(MARGIN_X + 0.25 * inch, y, f"{idx + 1}.   {w}")
        y -= 0.45 * inch

# ============================================================
# 4. STREAMLIT USER INTERFACE
# ============================================================
st.set_page_config(page_title="KDP Activity Book Generator", page_icon="📚", layout="centered")

st.title("📚 KDP Activity Book Generator")
st.write("Amazon KDP के लिए लार्ज प्रिंट पज़ल बुक्स (50, 100, 150+ पेजेस) एक क्लिक में जनरेट करें।")

with st.sidebar:
    st.header("⚙️ Book Settings")
    book_title = st.text_input("Book Title", value="The Good Old Days")
    
    puzzle_type = st.selectbox(
        "Book Category / Type",
        options=["mixed", "word_search", "sudoku", "scramble"],
        format_func=lambda x: {
            "mixed": "🔀 Mixed (Word Search + Sudoku + Scramble)",
            "word_search": "🔍 Word Search Only",
            "sudoku": "🔢 Sudoku Only",
            "scramble": "✏️ Word Scramble Only"
        }[x]
    )

    num_puzzles = st.select_slider(
        "Total Number of Puzzles",
        options=[25, 50, 75, 100, 150],
        value=50,
        help="Answer keys के साथ किताब के कुल पेज लगभग इसके दोगुने होंगे।"
    )

    difficulty = st.selectbox("Difficulty (Sudoku)", ["easy", "medium", "hard"], index=0)
    
    theme_choice = st.selectbox(
        "Word Search Theme",
        options=["All Themes (Mix)"] + list(THEMES.keys())
    )

    include_answers = st.checkbox("Include Answer Keys at the End", value=True)

# Generate Button
if st.button("🚀 Generate KDP Book PDF", type="primary"):
    with st.spinner("Generating book pages & puzzles... Please wait"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setTitle(book_title)

        page_num = 1
        draw_cover(c, page_num, book_title)

        answer_callbacks = []
        types = ["word_search", "sudoku", "scramble"] if puzzle_type == "mixed" else [puzzle_type]
        theme_keys = list(THEMES.keys())

        for i in range(1, num_puzzles + 1):
            ptype = types[(i - 1) % len(types)]
            page_num += 1
            c.showPage()

            cur_theme = theme_keys[(i - 1) % len(theme_keys)] if theme_choice == "All Themes (Mix)" else theme_choice

            if ptype == "word_search":
                grid, placements = generate_word_search(THEMES[cur_theme])
                draw_word_search_page(c, page_num, i, cur_theme, grid, placements, book_title)
                if include_answers:
                    answer_callbacks.append(
                        lambda cv, pn, idx=i, th=cur_theme, gr=grid, pl=placements:
                            draw_word_search_answer(cv, pn, idx, th, gr, pl, book_title)
                    )
            elif ptype == "sudoku":
                puz, sol = generate_sudoku(difficulty)
                draw_sudoku_page(c, page_num, i, puz, difficulty, book_title)
                if include_answers:
                    answer_callbacks.append(
                        lambda cv, pn, idx=i, s=sol:
                            draw_sudoku_answer(cv, pn, idx, s, book_title)
                    )
            elif ptype == "scramble":
                sample = random.sample(SCRAMBLE_WORDS_POOL, min(10, len(SCRAMBLE_WORDS_POOL)))
                draw_scramble_page(c, page_num, i, sample, book_title)
                if include_answers:
                    answer_callbacks.append(
                        lambda cv, pn, idx=i, w=sample:
                            draw_scramble_answer(cv, pn, idx, w, book_title)
                    )

        if include_answers and answer_callbacks:
            page_num += 1
            c.showPage()
            draw_section_divider(c, page_num, "Solutions & Answers", "Answer keys for all puzzles", book_title)
            for cb in answer_callbacks:
                page_num += 1
                c.showPage()
                cb(c, page_num)

        c.save()
        pdf_buffer.seek(0)

        st.success(f"✅ पुस्तक सफलतापूर्वक तैयार हो गई! (कुल पेज: {page_num})")
        st.download_button(
            label="📥 Download Ready-to-Publish PDF",
            data=pdf_buffer,
            file_name=f"{book_title.replace(' ', '_')}_{num_puzzles}_puzzles.pdf",
            mime="application/pdf"
        )

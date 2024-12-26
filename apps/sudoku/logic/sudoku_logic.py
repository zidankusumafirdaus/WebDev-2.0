import random

def generate_sudoku():
    """Fungsi untuk membuat board Sudoku."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_diagonal_blocks(board)
    solve_sudoku(board)
    remove_cells(board, difficulty=40)  # Difficulty: 40 kosong untuk tingkat medium
    return board

def fill_diagonal_blocks(board):
    """Mengisi diagonal blok 3x3."""
    for i in range(0, 9, 3):
        fill_block(board, i, i)

def fill_block(board, row, col):
    nums = list(range(1, 10))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def solve_sudoku(board):
    """Solusi untuk Sudoku menggunakan backtracking."""
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_safe(board, row, col, num):
    return (num not in board[row] and  # Baris
            num not in [board[i][col] for i in range(9)] and  # Kolom
            num not in [board[row//3*3 + i][col//3*3 + j] for i in range(3) for j in range(3)])  # Blok 3x3

def remove_cells(board, difficulty):
    """Menghapus beberapa angka untuk membuat permainan."""
    for _ in range(difficulty):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

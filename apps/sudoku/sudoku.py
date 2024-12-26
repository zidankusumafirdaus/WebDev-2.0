from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from apps.sudoku.logic.sudoku_logic import generate_sudoku, solve_sudoku

sudoku_bp = Blueprint('sudoku', __name__, template_folder='templates', static_folder='static')

@sudoku_bp.route("/", methods=["GET", "POST"])
def sudoku():
    if "sudoku_board" not in session:
        session["sudoku_board"] = generate_sudoku()
        session["original_board"] = [row[:] for row in session["sudoku_board"]]
        session["solved_board"] = [row[:] for row in session["original_board"]]
        solve_sudoku(session["solved_board"])  # Simpan solusi sejak awal

    if request.method == "POST":
        action = request.form.get("action")
        if action == "new_game":
            session["sudoku_board"] = generate_sudoku()
            session["original_board"] = [row[:] for row in session["sudoku_board"]]
            session["solved_board"] = [row[:] for row in session["original_board"]]
            solve_sudoku(session["solved_board"])

        elif action == "solve":
            session["sudoku_board"] = [row[:] for row in session["solved_board"]]
        elif action == "submit":
            user_board = extract_user_board(request.form)
            time_taken = request.form.get("time_taken", "0")
            if check_solution(user_board, session["solved_board"]):
                flash(f"Selamat! Jawaban benar. Waktu yang diambil: {time_taken} detik.", "success")
            else:
                flash("Blok! Salah.", "error")

    return render_template("sudoku.html", sudoku_board=session["sudoku_board"])

def extract_user_board(form_data):
    """Mengambil data inputan dari form Sudoku."""
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            value = form_data.get(f"cell-{i}-{j}")
            row.append(int(value) if value else 0)
        board.append(row)
    return board

def check_solution(user_board, solved_board):
    """Membandingkan jawaban pengguna dengan solusi yang benar."""
    return user_board == solved_board
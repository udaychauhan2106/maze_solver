from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import matplotlib

matplotlib.use("TkAgg", force=True)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from maze_solver.algorithms import bfs_shortest_path, dfs_explore_path
from maze_solver.maze import generate_random_maze, get_predefined_mazes, validate_maze_inputs
from maze_solver.visualization import draw_comparison, draw_maze_overview, draw_search_result


class MazeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Maze Solver / Path Finder")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)

        self.maze_catalog = get_predefined_mazes()
        self.maze_names = list(self.maze_catalog)
        self.current_maze = self.maze_catalog[self.maze_names[0]].copy()
        self.bfs_result = None
        self.dfs_result = None

        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.controls = ttk.Frame(self.main_frame)
        self.controls.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        ttk.Label(self.controls, text="Select Maze", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        self.maze_var = tk.StringVar(value=self.maze_names[0])
        self.maze_combo = ttk.Combobox(self.controls, textvariable=self.maze_var, values=self.maze_names, state="readonly", width=28)
        self.maze_combo.bind("<<ComboboxSelected>>", self.select_maze)
        self.maze_combo.pack(fill=tk.X, pady=(0, 12))

        ttk.Button(self.controls, text="Generate Random Maze", command=self.generate_random_maze).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(self.controls, text="Show Maze", command=self.show_maze).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(self.controls, text="Run BFS", command=self.run_bfs).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(self.controls, text="Run DFS", command=self.run_dfs).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(self.controls, text="Compare BFS vs DFS", command=self.compare_algorithms).pack(fill=tk.X, pady=(0, 8))

        self.output_box = tk.Text(self.controls, width=38, height=18, wrap=tk.WORD, font=("Segoe UI", 10))
        self.output_box.pack(fill=tk.BOTH, expand=True)
        self.output_box.insert(tk.END, "Select a maze and run an algorithm to begin.\n")

        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.render_visual()

    def select_maze(self, _event=None) -> None:
        selected_name = self.maze_var.get()
        if selected_name in self.maze_catalog:
            self.current_maze = self.maze_catalog[selected_name].copy()
            self._write_output(f"Selected maze: {selected_name}\nDescription: {self.current_maze.description}\n")
            self.render_visual(title=f"Maze Overview: {selected_name}")

    def _write_output(self, text: str) -> None:
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)

    def _show_figure(self, fig) -> None:
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def render_visual(self, *, title: str | None = None) -> None:
        fig = draw_maze_overview(self.current_maze, title=title or f"Maze Overview: {self.current_maze.name}")
        self._show_figure(fig)

    def generate_random_maze(self) -> None:
        try:
            rows = simpledialog.askinteger("Random Maze", "Rows:", minvalue=2, maxvalue=20, initialvalue=8)
            if rows is None:
                return
            cols = simpledialog.askinteger("Random Maze", "Columns:", minvalue=2, maxvalue=20, initialvalue=8)
            if cols is None:
                return
            seed_value = simpledialog.askinteger("Random Maze", "Optional seed (leave blank for random seed):", minvalue=0, maxvalue=999999, initialvalue=0)
            seed = None if seed_value is None or seed_value == 0 else seed_value
            self.current_maze = generate_random_maze(rows, cols, seed=seed)
            self.maze_var.set("Random Maze")
            self._write_output(
                f"Generated random maze: {self.current_maze.rows}x{self.current_maze.cols}\n"
                f"Start: {self.current_maze.start}\nGoal: {self.current_maze.goal}\n"
            )
            self.render_visual(title=f"Random Maze: {self.current_maze.rows}x{self.current_maze.cols}")
        except ValueError as exc:
            messagebox.showerror("Maze Error", str(exc))

    def show_maze(self) -> None:
        try:
            validate_maze_inputs(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            self._write_output(
                f"Maze: {self.current_maze.name}\n"
                f"Size: {self.current_maze.rows}x{self.current_maze.cols}\n"
                f"Start: {self.current_maze.start}\nGoal: {self.current_maze.goal}\n\n"
                + "\n".join(" ".join(str(cell) for cell in row) for row in self.current_maze.matrix)
            )
            self.render_visual(title=f"Maze Overview: {self.current_maze.name}")
        except ValueError as exc:
            messagebox.showerror("Maze Error", str(exc))

    def run_bfs(self) -> None:
        try:
            validate_maze_inputs(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            self.bfs_result = bfs_shortest_path(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            result = self.bfs_result
            self._write_output(
                f"BFS Summary\n"
                f"Path found: {result.path_found}\n"
                f"Path length: {result.path_length}\n"
                f"Nodes visited: {result.visited_nodes}\n"
                f"Nodes expanded: {result.expanded_nodes}\n"
                f"Execution time: {result.execution_time:.6f}s\n"
                f"Path: {result.path}\n"
            )
            self.render_visual(title=f"BFS Result: {self.current_maze.name}")
            fig = draw_search_result(self.current_maze, result, title=f"BFS Result: {self.current_maze.name}")
            self._show_figure(fig)
        except ValueError as exc:
            messagebox.showerror("BFS Error", str(exc))

    def run_dfs(self) -> None:
        try:
            validate_maze_inputs(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            self.dfs_result = dfs_explore_path(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            result = self.dfs_result
            self._write_output(
                f"DFS Summary\n"
                f"Path found: {result.path_found}\n"
                f"Path length: {result.path_length}\n"
                f"Nodes visited: {result.visited_nodes}\n"
                f"Nodes expanded: {result.expanded_nodes}\n"
                f"Execution time: {result.execution_time:.6f}s\n"
                f"Path: {result.path}\n"
            )
            fig = draw_search_result(self.current_maze, result, title=f"DFS Result: {self.current_maze.name}")
            self._show_figure(fig)
        except ValueError as exc:
            messagebox.showerror("DFS Error", str(exc))

    def compare_algorithms(self) -> None:
        try:
            validate_maze_inputs(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            bfs_result = bfs_shortest_path(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            dfs_result = dfs_explore_path(self.current_maze.matrix, self.current_maze.start, self.current_maze.goal)
            self.bfs_result = bfs_result
            self.dfs_result = dfs_result
            comparison = (
                f"BFS Summary\n"
                f"Path found: {bfs_result.path_found}\n"
                f"Path length: {bfs_result.path_length}\n"
                f"Visited: {bfs_result.visited_nodes}\n"
                f"Expanded: {bfs_result.expanded_nodes}\n"
                f"Time: {bfs_result.execution_time:.6f}s\n\n"
                f"DFS Summary\n"
                f"Path found: {dfs_result.path_found}\n"
                f"Path length: {dfs_result.path_length}\n"
                f"Visited: {dfs_result.visited_nodes}\n"
                f"Expanded: {dfs_result.expanded_nodes}\n"
                f"Time: {dfs_result.execution_time:.6f}s\n"
            )
            self._write_output(comparison)
            fig = draw_comparison(self.current_maze, bfs_result, dfs_result)
            self._show_figure(fig)
        except ValueError as exc:
            messagebox.showerror("Comparison Error", str(exc))


def main() -> None:
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

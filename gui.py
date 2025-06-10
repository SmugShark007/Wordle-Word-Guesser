import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Dict
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
from algorithms import best_first_search, astar_search, aostar_search, dfs_search
from word_utils import get_feedback

class WordleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Solver")
        self.root.geometry("1000x900")  # Increased window size for better layout
        self.root.configure(padx=30, pady=30, bg="#121212")  # Darker background with more padding

        try:
            with open('five_letter_words.txt') as f:
                self.words = [line.strip().lower() for line in f.readlines() if len(line.strip()) == 5]
            if not self.words:
                raise ValueError("No valid 5-letter words found in the file")
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find five_letter_words.txt")
            self.root.destroy()
            return

        self.algorithms = {
            "Best First Search": best_first_search,
            "A* Search": astar_search,
            "AO* Search": aostar_search,
            "Depth First Search": dfs_search
        }
        self._setup_styles()
        self.create_widgets()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure(".", background="#121212")  # Global darker background
        
        # Enhanced notebook and tab styles
        style.configure("TNotebook", 
                       background="#121212", 
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure("TNotebook.Tab", 
                       background="#1E1E1E",
                       foreground="#00008B",  # Changed to dark blue
                       padding=[15, 5],
                       borderwidth=0,
                       font=("Arial", 10, "bold"))
                       
        style.map("TNotebook.Tab",
                 background=[("selected", "#2D2D2D"), ("!selected", "#1E1E1E"), ("active", "#2D2D2D")],
                 foreground=[("selected", "#000080"), ("!selected", "#00008B"), ("active", "#000080")])  # Dark blue variants
        
        style.configure("TFrame", background="#121212")
        style.configure("TLabelframe", 
                       background="#121212",
                       bordercolor="#2D2D2D",
                       relief="solid")
        
        style.configure("TLabelframe.Label", 
                       background="#121212", 
                       foreground="#00FFB3",
                       font=("Arial", 11, "bold"))
        
        style.configure("TEntry",
                       fieldbackground="#FFFFFF",  # Changed to white background
                       foreground="#000000",       # Changed to black text
                       insertcolor="#000000",      # Changed cursor color to black
                       borderwidth=1,
                       relief="solid",
                       font=("Arial", 10))

        style.configure("TButton",
                       background="#1E1E1E",
                       foreground="#00FFB3",
                       font=("Arial", 10, "bold"),
                       padding=8,
                       borderwidth=1,
                       relief="solid")
        
        style.map("TButton",
                  foreground=[("active", "#00FFD1")],
                  background=[("active", "#2D2D2D")])

        style.configure("Custom.TButton",
                       background="#1E1E1E",
                       foreground="#00FFB3",
                       font=("Arial", 10, "bold"),
                       padding=8)
        
        style.map("Custom.TButton",
                  foreground=[("active", "#00FFD1")],
                  background=[("active", "#2D2D2D")])

        style.configure("NeonPink.TLabel", 
                       background="#121212", 
                       foreground="#FF1493", 
                       font=("Arial", 11, "bold"))
        
        style.configure("NeonBlue.TLabel", 
                       background="#121212", 
                       foreground="#00BFFF", 
                       font=("Arial", 11, "bold"))
        
        style.configure("NeonGreen.TLabel", 
                       background="#121212", 
                       foreground="#00FFB3", 
                       font=("Arial", 11, "bold"))

        style.configure("Treeview",
                       background="#1E1E1E",
                       fieldbackground="#1E1E1E",
                       foreground="#FFFFFF",
                       font=("Arial", 10),
                       rowheight=25)
        
        style.configure("Treeview.Heading",
                       font=("Arial", 10, "bold"),
                       background="#2D2D2D",
                       foreground="#FF0000",  # Changed to red
                       relief="flat",
                       padding=5)
        
        style.map("Treeview",
                  background=[("selected", "#2D2D2D")],
                  foreground=[("selected", "#00FFB3")])

        style.configure("Vertical.TScrollbar",
                       background="#1E1E1E",
                       arrowcolor="#00FFB3",
                       bordercolor="#2D2D2D",
                       troughcolor="#121212",
                       width=16)
        
        style.map("Vertical.TScrollbar",
                  background=[("active", "#2D2D2D"), ("disabled", "#1E1E1E")])

    def create_widgets(self):
        # Main input frame with more padding and rounded corners
        input_frame = ttk.LabelFrame(self.root, text="Input", padding=15, style="TLabelframe")
        input_frame.pack(fill='x', pady=(0, 15))

        word_frame = ttk.Frame(input_frame, style="TFrame")
        word_frame.pack(fill='x', pady=(5, 10))

        title_label = ttk.Label(word_frame, text="Enter secret word:", style="NeonPink.TLabel")
        title_label.pack(side='left', padx=(0, 10))

        self.secret_word_entry = ttk.Entry(word_frame, 
                                         font=("Arial", 11),
                                         style="TEntry",
                                         width=20)
        self.secret_word_entry.pack(side='left', padx=5)

        button_frame = ttk.Frame(input_frame, style="TFrame")
        button_frame.pack(fill='x', pady=(10, 0))

        compare_button = tk.Button(button_frame,
                                   text="Compare Algorithms",
                                   command=self.solve,
                                   font=("Arial", 11, "bold"),
                                   fg="#00FFB3",
                                   bg="#1E1E1E",
                                   activebackground="#2D2D2D",
                                   activeforeground="#00FFD1",
                                   relief="solid",
                                   bd=1,
                                   padx=15,
                                   pady=8)
        compare_button.pack(side='left', padx=(0, 10))

        clear_button = tk.Button(button_frame,
                                 text="Clear",
                                 command=self.clear,
                                 font=("Arial", 11, "bold"),
                                 fg="#00FFB3",
                                 bg="#1E1E1E",
                                 activebackground="#2D2D2D",
                                 activeforeground="#00FFD1",
                                 relief="solid",
                                 bd=1,
                                 padx=15,
                                 pady=8)
        clear_button.pack(side='left')

        # Notebook with improved styling
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill='both', expand=True, pady=(0, 15))

        self.tree_tabs = {}
        for name in self.algorithms:
            tab = ttk.Frame(self.notebook, style="TFrame", padding=10)
            self.notebook.add(tab, text=name)
            
            tree = ttk.Treeview(tab, 
                               columns=('Guess', 'Feedback'),
                               show='headings',
                               style="Treeview",
                               height=10)
            
            tree.heading('Guess', text='Guess')
            tree.heading('Feedback', text='Feedback')
            tree.column('Guess', width=150, anchor='center')
            tree.column('Feedback', width=200, anchor='center')
            
            tree.pack(side='left', fill='both', expand=True)
            
            scrollbar = ttk.Scrollbar(tab, 
                                    orient='vertical',
                                    command=tree.yview,
                                    style="Vertical.TScrollbar")
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            self.tree_tabs[name] = tree

        # Statistics frame with enhanced styling
        self.stats_frame = ttk.LabelFrame(self.root, 
                                        text="Statistics",
                                        padding=15,
                                        style="TLabelframe")
        self.stats_frame.pack(fill='x')

        self.time_label = ttk.Label(self.stats_frame,
                                  text="Time taken: -",
                                  style="NeonBlue.TLabel")
        self.time_label.pack(pady=3)

        self.guesses_label = ttk.Label(self.stats_frame,
                                     text="Total guesses tried: -",
                                     style="NeonGreen.TLabel")
        self.guesses_label.pack(pady=3)

        self.length_label = ttk.Label(self.stats_frame,
                                    text="Solution length: -",
                                    style="NeonPink.TLabel")
        self.length_label.pack(pady=3)

    def clear(self):
        self.secret_word_entry.delete(0, tk.END)
        for tree in self.tree_tabs.values():
            tree.delete(*tree.get_children())
        self.time_label.config(text="Time taken: -")
        self.guesses_label.config(text="Total guesses tried: -")
        self.length_label.config(text="Solution length: -")

    def feedback_to_emoji(self, feedback: str) -> str:
        emoji_map = {'g': '🟩', 'y': '🟨', 'b': '⬛'}
        return ''.join(emoji_map[c] for c in feedback)

    def solve(self):
        secret_word = self.secret_word_entry.get().strip().lower()
        if len(secret_word) != 5 or secret_word not in self.words:
            messagebox.showerror("Error", "Invalid 5-letter word")
            return

        results = {}
        for name, algo_func in self.algorithms.items():
            tree = self.tree_tabs[name]
            tree.delete(*tree.get_children())
            start = time.time()
            guesses, _ = algo_func(self.words, secret_word)
            end = time.time()
            if guesses:
                results[name] = {
                    'time': end - start,
                    'guesses': len(guesses)
                }
                for guess in guesses:
                    feedback = get_feedback(secret_word, guess)
                    emoji_feedback = self.feedback_to_emoji(feedback)
                    tree.insert('', 'end', values=(guess.upper(), emoji_feedback))
        if results:
            self.time_label.config(text=f"Time taken: {sum(r['time'] for r in results.values()):.2f} s")
            self.guesses_label.config(text=f"Total guesses tried: {sum(r['guesses'] for r in results.values())}")
            self.length_label.config(text=f"Average solution length: {sum(r['guesses'] for r in results.values()) // len(results)}")
            self.show_comparison_chart(results)
        else:
            messagebox.showinfo("Result", "No solution found for any algorithm")

    def show_comparison_chart(self, results: Dict[str, Dict[str, float]]):
        popup = tk.Toplevel(self.root)
        popup.title("Algorithm Comparison")
        popup.geometry("1400x800")  # Increased height for better visualization
        popup.configure(bg="#121212")
        
        # Add a title at the top
        title_frame = ttk.Frame(popup, style="TFrame")
        title_frame.pack(fill='x', padx=20, pady=(20,10))
        
        title_label = ttk.Label(title_frame, 
                              text="Algorithm Performance Comparison",
                              style="TLabel",
                              font=("Arial", 16, "bold"),
                              foreground="#00FFB3")
        title_label.pack()

        container = ttk.Frame(popup, style="TFrame")
        container.pack(fill='both', expand=True, padx=20, pady=(0,20))

        # Enhanced feedback frame
        feedback_frame = ttk.LabelFrame(container, 
                                      text="Detailed Results",
                                      style="TLabelframe",
                                      padding=15)
        feedback_frame.pack(side='left', fill='both', expand=True, padx=(0,10))

        # Enhanced treeview
        feedback_tree = ttk.Treeview(feedback_frame, 
                                   columns=('Algorithm', 'Time', 'Guesses'),
                                   show='headings',
                                   style="Treeview",
                                   height=8)
        
        feedback_tree.heading('Algorithm', text='Algorithm')
        feedback_tree.heading('Time', text='Time (s)')
        feedback_tree.heading('Guesses', text='Guesses')
        
        # Set column widths and alignment
        feedback_tree.column('Algorithm', width=150, anchor='center')
        feedback_tree.column('Time', width=100, anchor='center')
        feedback_tree.column('Guesses', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(feedback_frame,
                                orient='vertical',
                                command=feedback_tree.yview,
                                style="Vertical.TScrollbar")
        scrollbar.pack(side='right', fill='y')
        feedback_tree.configure(yscrollcommand=scrollbar.set)
        feedback_tree.pack(fill='both', expand=True)

        for algo in results:
            feedback_tree.insert('', 'end', values=(
                algo,
                f"{results[algo]['time']:.2f}",
                results[algo]['guesses']
            ))

        # Enhanced graph frame
        graph_frame = ttk.LabelFrame(container,
                                   text="Visual Analysis",
                                   style="TLabelframe",
                                   padding=15)
        graph_frame.pack(side='right', fill='both', expand=True)

        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
        fig.patch.set_facecolor('#121212')
        
        algorithms = list(results.keys())
        times = [results[algo]['time'] for algo in algorithms]
        guesses = [results[algo]['guesses'] for algo in algorithms]
        
        # Enhanced color palette
        colors = ['#00FFB3', '#FF1493', '#00BFFF', '#FFD700']
        
        # Style for both plots
        for ax in [ax1, ax2]:
            ax.set_facecolor('#1E1E1E')
            ax.grid(True, linestyle='--', alpha=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#2D2D2D')
            ax.spines['left'].set_color('#2D2D2D')

        # Time comparison plot
        bars1 = ax1.bar(algorithms, times, color=colors)
        ax1.set_title("Time Taken (seconds)", 
                     color='#00FFB3',
                     fontsize=12,
                     pad=15,
                     font='Arial')
        ax1.set_ylabel("Time (s)",
                      color='#00BFFF',
                      fontsize=10,
                      font='Arial')
        ax1.tick_params(axis='both', colors='#00BFFF')
        
        # Add value labels on the bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}s',
                    ha='center',
                    va='bottom',
                    color='#FFFFFF',
                    font='Arial')

        # Guesses comparison plot
        bars2 = ax2.bar(algorithms, guesses, color=colors)
        ax2.set_title("Number of Guesses",
                     color='#00FFB3',
                     fontsize=12,
                     pad=15,
                     font='Arial')
        ax2.set_ylabel("Guesses",
                      color='#00BFFF',
                      fontsize=10,
                      font='Arial')
        ax2.tick_params(axis='both', colors='#00BFFF')
        
        # Add value labels on the bars
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center',
                    va='bottom',
                    color='#FFFFFF',
                    font='Arial')

        # Rotate x-axis labels for better readability
        for ax in [ax1, ax2]:
            ax.set_xticklabels(algorithms,
                              rotation=15,
                              ha='right',
                              color='#00BFFF',
                              font='Arial')

        fig.tight_layout(pad=5.0)
        
        # Create and pack the canvas with proper styling
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(bg="#121212",
                              highlightthickness=0)
        canvas_widget.pack(fill='both',
                          expand=True,
                          padx=5,
                          pady=5)

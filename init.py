import tkinter as tk
import math

node_positions = {
    1: (100, 100),
    2: (200, 100),
    3: (300, 100),
    4: (100, 200),
    5: (200, 200),
    6: (300, 200),
    7: (100, 300),
    8: (200, 300)
}

class CarMovementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Movement")
        self.geometry("400x400")
        self.node_positions = node_positions
        self.current_node = 1
        self.total_cost = 0
        self.current_cost = 0
        self.current_position = node_positions[self.current_node]
        self.target_node = None
        self.car = None
        self.timer = None 
        self.create_widgets()
        self.bind("<KeyPress>", self.on_key_press)

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        self.current_cost_label = tk.Label(self, text=f"Current Cost: {self.current_cost:.3f}")
        self.current_cost_label.pack()

        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        for (node, (x, y)) in self.node_positions.items():
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue") 
            self.canvas.create_text(x, y-25, text=str(node))

        for i in range(1, 9):
            for j in range(i + 1, 9):
                x1, y1 = self.node_positions[i]
                x2, y2 = self.node_positions[j]
                self.canvas.create_line(x1, y1, x2, y2)

        if self.car is None:
            x, y = self.current_position
            self.car = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")

    def on_key_press(self, event):
        direction = {'Up': (0, -1), 'Down': (0, 1), 'Left': (-1, 0), 'Right': (1, 0)}
        if event.keysym in direction:
            dx, dy = direction[event.keysym]
            self.move_car(dx, dy)
            if self.current_node != self.target_node:  
                self.start_timer()

    def start_timer(self):
        if self.timer is None:
            self.timer = self.after(100, self.update_current_cost) 

    def update_current_cost(self):
        if self.current_node != self.target_node: 
            if not self.is_inside_node(self.current_position): 
                self.current_cost += 0.1 
                self.total_cost += 0.1
                self.current_cost_label.config(text=f"Current Cost: {self.current_cost:.3f}")
        else:
            if self.is_inside_node(self.current_position): 
                self.current_cost = 0  
                self.current_cost_label.config(text=f"Current Cost: {self.current_cost:.3f}")
            else:
                self.current_cost = 0 
                self.current_cost_label.config(text=f"Current Cost: {self.current_cost:.3f}")
        self.timer = self.after(100, self.update_current_cost) 


    def move_car(self, dx, dy):
        step_size = 5
        prev_x, prev_y = self.current_position
        new_x = prev_x + dx * step_size
        new_y = prev_y + dy * step_size

        if self.is_valid_move(new_x, new_y):
            self.current_position = (new_x, new_y)
            self.canvas.coords(self.car, new_x - 5, new_y - 5, new_x + 5, new_y + 5)

            for node, (nx, ny) in self.node_positions.items():
                if math.isclose(new_x, nx, abs_tol=10) and math.isclose(new_y, ny, abs_tol=10):
                    self.current_node = node
                    if node in [1, 2, 3, 4, 5, 6, 7, 8]:
                        self.current_cost = 0 
                        self.current_cost_label.config(text=f"Current Cost: {self.current_cost:.3f}")
                    break


    def is_valid_move(self, x, y):
        return 0 <= x <= 400 and 0 <= y <= 400

    def is_inside_node(self, position):
        x, y = position
        for (node, (nx, ny)) in self.node_positions.items():
            if nx - 15 <= x <= nx + 15 and ny - 15 <= y <= ny + 15:
                return True
        return False

app = CarMovementApp()
app.mainloop()

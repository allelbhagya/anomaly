    def move_car(self, dx, dy):
        step_size = 5
        prev_x, prev_y = self.current_position
        new_x = prev_x + dx * step_size
        new_y = prev_y + dy * step_size

        # Check if the new position is valid and on a path
        if self.is_valid_move(new_x, new_y) and self.is_on_path(new_x, new_y):
            self.current_position = (new_x, new_y)
            self.canvas.coords(self.car, new_x - 5, new_y - 5, new_x + 5, new_y + 5)

            # Check if the car is near a new node
            for node, (nx, ny) in self.node_positions.items():
                if math.isclose(new_x, nx, abs_tol=10) and math.isclose(new_y, ny, abs_tol=10):
                    self.current_node = node
                    if node in [1, 2, 3, 4, 5, 6, 7, 8]:  # Check if the car is inside a blue dot node
                        self.current_cost = 0  # Reset current cost
                        self.current_cost_label.config(text=f"Current Cost: {self.current_cost:.3f}")
                        self.anomaly_message.config(text="Status: Normal")  # Reset anomaly status
                    break

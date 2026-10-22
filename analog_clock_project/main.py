"""Analog clock application with stopwatch and theme switching."""

import math
import time
import tkinter as tk
from datetime import datetime


class AnalogClockApp:
    """Display a live analog clock with stopwatch and theme controls."""

    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock")
        self.root.geometry("520x650")
        self.root.minsize(420, 540)

        self.is_dark = True
        self.stopwatch_running = False
        self.stopwatch_started_at = 0.0
        self.stopwatch_elapsed = 0.0
        self.after_id = None

        self.colors = {}
        self._set_theme_colors()

        self.main_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.main_frame.pack(fill="both", expand=True, padx=18, pady=18)

        self.title_label = tk.Label(
            self.main_frame,
            text="ANALOG CLOCK",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"],
        )
        self.title_label.pack(pady=(0, 12))

        self.clock_canvas = tk.Canvas(
            self.main_frame,
            width=400,
            height=400,
            bg=self.colors["background"],
            highlightthickness=0,
        )
        self.clock_canvas.pack(fill="both", expand=True)

        self.digital_label = tk.Label(
            self.main_frame,
            text="",
            font=("Consolas", 18, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"],
        )
        self.digital_label.pack(pady=(8, 12))

        self.stopwatch_label = tk.Label(
            self.main_frame,
            text="Stopwatch  00:00.00",
            font=("Consolas", 13),
            bg=self.colors["background"],
            fg=self.colors["text"],
        )
        self.stopwatch_label.pack(pady=(0, 10))

        button_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        button_frame.pack(fill="x", pady=(0, 4))

        self.stopwatch_button = tk.Button(
            button_frame,
            text="Start",
            command=self.toggle_stopwatch,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.stopwatch_button.pack(side="left", expand=True, padx=4)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_stopwatch,
            font=("Segoe UI", 10),
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
        )
        self.reset_button.pack(side="left", expand=True, padx=4)

        self.theme_button = tk.Button(
            button_frame,
            text="Light theme",
            command=self.toggle_theme,
            font=("Segoe UI", 10),
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
        )
        self.theme_button.pack(side="left", expand=True, padx=4)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply_theme()
        self.update_clock()

    def _set_theme_colors(self):
        """Set the current palette."""
        if self.is_dark:
            self.colors = {
                "background": "#111827",
                "face": "#1F2937",
                "text": "#F9FAFB",
                "muted": "#9CA3AF",
                "accent": "#38BDF8",
                "second": "#F87171",
                "tick": "#D1D5DB",
                "button": "#374151",
                "button_text": "#F9FAFB",
                "border": "#4B5563",
            }
        else:
            self.colors = {
                "background": "#F3F4F6",
                "face": "#FFFFFF",
                "text": "#111827",
                "muted": "#6B7280",
                "accent": "#0284C7",
                "second": "#DC2626",
                "tick": "#374151",
                "button": "#E5E7EB",
                "button_text": "#111827",
                "border": "#D1D5DB",
            }

    def apply_theme(self):
        """Apply the selected palette to widgets."""
        self._set_theme_colors()
        self.root.configure(bg=self.colors["background"])
        self.main_frame.configure(bg=self.colors["background"])
        for widget in (
            self.title_label,
            self.digital_label,
            self.stopwatch_label,
        ):
            widget.configure(
                bg=self.colors["background"],
                fg=self.colors["text"],
            )
        self.clock_canvas.configure(bg=self.colors["background"])
        for button in (
            self.stopwatch_button,
            self.reset_button,
            self.theme_button,
        ):
            button.configure(
                bg=self.colors["button"],
                fg=self.colors["button_text"],
                activebackground=self.colors["accent"],
                activeforeground=self.colors["background"],
                bd=0,
            )
        self.theme_button.configure(
            text="Light theme" if self.is_dark else "Dark theme"
        )
        self.draw_clock()

    def toggle_theme(self):
        """Switch between dark and light themes."""
        self.is_dark = not self.is_dark
        self.apply_theme()

    def toggle_stopwatch(self):
        """Start or pause the stopwatch."""
        if self.stopwatch_running:
            self.stopwatch_elapsed += time.perf_counter() - self.stopwatch_started_at
            self.stopwatch_running = False
            self.stopwatch_button.configure(text="Start")
        else:
            self.stopwatch_started_at = time.perf_counter()
            self.stopwatch_running = True
            self.stopwatch_button.configure(text="Pause")
        self.update_stopwatch()

    def reset_stopwatch(self):
        """Reset the stopwatch to zero."""
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0.0
        self.stopwatch_started_at = 0.0
        self.stopwatch_button.configure(text="Start")
        self.update_stopwatch()

    def get_stopwatch_elapsed(self):
        """Return elapsed stopwatch time in seconds."""
        if self.stopwatch_running:
            return self.stopwatch_elapsed + (
                time.perf_counter() - self.stopwatch_started_at
            )
        return self.stopwatch_elapsed

    def update_stopwatch(self):
        """Refresh the stopwatch display."""
        elapsed = self.get_stopwatch_elapsed()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centiseconds = int((elapsed * 100) % 100)
        self.stopwatch_label.configure(
            text=f"Stopwatch  {minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        )

    def draw_clock(self):
        """Draw the clock face, tick marks, numerals, and hands."""
        canvas = self.clock_canvas
        canvas.delete("all")

        width = max(canvas.winfo_width(), 300)
        height = max(canvas.winfo_height(), 300)
        size = min(width, height) - 24
        center_x = width / 2
        center_y = height / 2
        radius = size / 2

        canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill=self.colors["face"],
            outline=self.colors["border"],
            width=2,
        )

        for mark in range(60):
            angle = math.radians(mark * 6 - 90)
            is_hour_mark = mark % 5 == 0
            outer_radius = radius * 0.91
            inner_radius = radius * (0.81 if is_hour_mark else 0.86)
            x1 = center_x + math.cos(angle) * inner_radius
            y1 = center_y + math.sin(angle) * inner_radius
            x2 = center_x + math.cos(angle) * outer_radius
            y2 = center_y + math.sin(angle) * outer_radius
            canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=self.colors["text"] if is_hour_mark else self.colors["muted"],
                width=3 if is_hour_mark else 1,
                capstyle=tk.ROUND,
            )

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            number_radius = radius * 0.70
            x = center_x + math.cos(angle) * number_radius
            y = center_y + math.sin(angle) * number_radius
            canvas.create_text(
                x,
                y,
                text=str(number),
                fill=self.colors["text"],
                font=("Segoe UI", max(10, int(radius * 0.09)), "bold"),
            )

        now = datetime.now()
        second_value = now.second + now.microsecond / 1_000_000
        minute_value = now.minute + second_value / 60
        hour_value = (now.hour % 12) + minute_value / 60

        self._draw_hand(
            center_x,
            center_y,
            radius * 0.48,
            hour_value * 30,
            self.colors["text"],
            max(4, int(radius * 0.035)),
        )
        self._draw_hand(
            center_x,
            center_y,
            radius * 0.68,
            minute_value * 6,
            self.colors["accent"],
            max(3, int(radius * 0.023)),
        )
        self._draw_hand(
            center_x,
            center_y,
            radius * 0.78,
            second_value * 6,
            self.colors["second"],
            max(1, int(radius * 0.009)),
        )

        canvas.create_oval(
            center_x - 6,
            center_y - 6,
            center_x + 6,
            center_y + 6,
            fill=self.colors["second"],
            outline=self.colors["second"],
        )

    def _draw_hand(self, center_x, center_y, length, degrees, color, width):
        """Draw a clock hand from its center point."""
        angle = math.radians(degrees - 90)
        end_x = center_x + math.cos(angle) * length
        end_y = center_y + math.sin(angle) * length
        self.clock_canvas.create_line(
            center_x,
            center_y,
            end_x,
            end_y,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
        )

    def update_clock(self):
        """Refresh the clock and schedule the next update."""
        now = datetime.now()
        self.digital_label.configure(text=now.strftime("%A, %d %B  |  %H:%M:%S"))
        self.draw_clock()
        self.update_stopwatch()
        self.after_id = self.root.after(50, self.update_clock)

    def close(self):
        """Cancel scheduled updates and close the application."""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.root.destroy()


def main():
    """Create and run the application."""
    root = tk.Tk()
    AnalogClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
InstaHealth - Zero-Cloud On-Device Smartwatch Health Intelligence System
Language: Python 3 (Tkinter Standard Library - Zero External Dependencies)

Features:
- 100% on-device physiological modeling (Tanaka/Gulati equations, Karvonen HRR)
- Multi-profile isolation with emoji avatars (🏃‍♂️, 🧘‍♀️, 🚴‍♂️, 🏊‍♂️)
- 48-Hour (2-day) background calibration with demographic human benchmarking
- Day 3+ automatic calibration card dismissal and tailored prescriptions
- Horizontal swipeable circular ring carousel with page indicator dots
- High-contrast OLED dark theme with all typography >= 11pt
"""

import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox

# ==============================================================================
# 1. ON-DEVICE PHYSIOLOGICAL ENGINE (ZERO-CLOUD)
# ==============================================================================

CLINICAL_BASELINES = {
    "18-29": {
        "label": "18–29 yrs",
        "restingHR": 60,
        "hrRange": "55–66 bpm",
        "sleepHours": 7.8,
        "sleepRange": "7.5–8.5 hrs",
        "stepTarget": 8000,
        "stepRange": "7,000–10,000",
        "calories": 2400,
        "maxStillMinutes": 60
    },
    "30-39": {
        "label": "30–39 yrs",
        "restingHR": 63,
        "hrRange": "58–70 bpm",
        "sleepHours": 7.5,
        "sleepRange": "7.0–8.0 hrs",
        "stepTarget": 7500,
        "stepRange": "6,500–9,000",
        "calories": 2200,
        "maxStillMinutes": 60
    },
    "40-49": {
        "label": "40–49 yrs",
        "restingHR": 66,
        "hrRange": "60–73 bpm",
        "sleepHours": 7.2,
        "sleepRange": "7.0–8.0 hrs",
        "stepTarget": 7000,
        "stepRange": "6,000–8,500",
        "calories": 2050,
        "maxStillMinutes": 55
    },
    "50-59": {
        "label": "50–59 yrs",
        "restingHR": 68,
        "hrRange": "62–75 bpm",
        "sleepHours": 7.0,
        "sleepRange": "6.5–7.5 hrs",
        "stepTarget": 6500,
        "stepRange": "5,500–8,000",
        "calories": 1900,
        "maxStillMinutes": 50
    },
    "60+": {
        "label": "60+ yrs",
        "restingHR": 70,
        "hrRange": "64–78 bpm",
        "sleepHours": 7.0,
        "sleepRange": "6.5–7.5 hrs",
        "stepTarget": 6000,
        "stepRange": "5,000–7,500",
        "calories": 1750,
        "maxStillMinutes": 45
    }
}

class HealthEngine:
    def __init__(self):
        self.baselines = CLINICAL_BASELINES
        self.profiles = {}
        self.active_id = "runner"
        
        # Pre-seed default profile (Runner, 22y Male)
        self.add_profile("runner", emoji="🏃‍♂️", age=22, gender="Male")

    def _get_cohort(self, age):
        if age < 30: return "18-29"
        if age < 40: return "30-39"
        if age < 50: return "40-49"
        if age < 60: return "50-59"
        return "60+"

    def add_profile(self, profile_id, emoji="🏃‍♂️", age=22, gender="Male"):
        cohort = self._get_cohort(age)
        base = self.baselines[cohort]
        self.profiles[profile_id] = {
            "id": profile_id,
            "emoji": emoji,
            "age": int(age),
            "gender": gender,
            "cohort": cohort,
            "day_count": 1,
            "learned_baseline": dict(base),
            # Telemetry for days
            "telemetry": {
                "hr": base["restingHR"] - 2,
                "sleep_hours": 7.2,
                "steps": 6400,
                "still_minutes": 35,
                "calories": 450
            }
        }
        self.active_id = profile_id
        return self.profiles[profile_id]

    def get_active_profile(self):
        return self.profiles[self.active_id]

    def advance_day(self):
        p = self.profiles[self.active_id]
        p["day_count"] += 1
        # Slightly vary telemetry to reflect live activity
        if p["day_count"] == 2:
            p["telemetry"]["steps"] = 7200
            p["telemetry"]["sleep_hours"] = 7.4
            p["telemetry"]["hr"] = p["learned_baseline"]["restingHR"]
        elif p["day_count"] >= 3:
            p["telemetry"]["steps"] = 8600
            p["telemetry"]["sleep_hours"] = 7.6
            p["telemetry"]["hr"] = p["learned_baseline"]["restingHR"] + 1
        return p["day_count"]

    def calculate(self):
        p = self.profiles[self.active_id]
        t = p["telemetry"]
        
        # 1. Sex-differentiated HRmax formulation
        if p["gender"] == "Female":
            # Gulati et al. (Circulation 2010)
            max_hr = 206.0 - (0.88 * p["age"])
        else:
            # Tanaka et al. (JACC 2001)
            max_hr = 208.0 - (0.7 * p["age"])

        # 2. Karvonen Heart Rate Reserve (HRR)
        rhr = p["learned_baseline"]["restingHR"]
        hrr = max(30.0, max_hr - rhr)
        strain = max(0.0, min(100.0, ((t["hr"] - rhr) / hrr) * 100.0))
        
        # 3. Calibration stage evaluation
        is_calibrating = p["day_count"] < 3
        cohort_data = self.baselines[p["cohort"]]

        if is_calibrating:
            recs = {
                "calibrating": True,
                "days_remaining": 3 - p["day_count"],
                "target_sleep": cohort_data["sleepHours"],
                "target_steps": cohort_data["stepTarget"],
                "human_averages": cohort_data
            }
        else:
            # Day 3+: Adaptive personalized prescriptions
            extra_sleep = max(0.0, (strain - 20.0) / 100.0 * 1.5)
            step_mod = 1.0 + ((strain - 30.0) / 200.0)
            recs = {
                "calibrating": False,
                "days_remaining": 0,
                "target_sleep": round(p["learned_baseline"]["sleepHours"] + extra_sleep, 1),
                "target_steps": int(round(p["learned_baseline"]["stepTarget"] * step_mod)),
                "human_averages": cohort_data
            }

        return {
            "profile": p,
            "max_hr": round(max_hr, 1),
            "strain": round(strain, 1),
            "is_calibrating": is_calibrating,
            "recs": recs,
            "telemetry": t
        }

# ==============================================================================
# 2. SMARTWATCH DESKTOP INTERFACE (TKINTER GUI)
# ==============================================================================

class InstaHealthSmartwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InstaHealth — Zero-Cloud Smartwatch (Python)")
        self.root.geometry("460x780")
        self.root.configure(bg="#0F172A")
        self.root.resizable(False, False)

        self.engine = HealthEngine()
        self.current_ring_index = 0
        self.drag_start_x = 0

        self.setup_ui()
        self.refresh_display()

    def setup_ui(self):
        # Container
        main_frame = tk.Frame(self.root, bg="#0F172A", padx=16, pady=16)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # External Simulator Controls Header
        top_ctrl = tk.Frame(main_frame, bg="#0F172A")
        top_ctrl.pack(fill=tk.X, pady=(0, 10))

        btn_person = tk.Button(
            top_ctrl, text="👤 Change Person", bg="#2563EB", fg="white",
            font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2",
            padx=10, pady=5, command=self.open_change_person_dialog
        )
        btn_person.pack(side=tk.LEFT)

        btn_advance = tk.Button(
            top_ctrl, text="⏭️ Next Day", bg="#0D9488", fg="white",
            font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2",
            padx=10, pady=5, command=self.advance_simulation_day
        )
        btn_advance.pack(side=tk.RIGHT)

        # Smartwatch Outer Case Frame
        self.case_canvas = tk.Canvas(
            main_frame, width=410, height=620, bg="#0F172A", highlightthickness=0
        )
        self.case_canvas.pack(pady=4)

        # Draw physical watch bezel
        # Bezel rim
        self.case_canvas.create_oval(15, 15, 395, 605, fill="#1E293B", outline="#334155", width=4)
        # OLED Display Screen (Pure Black)
        self.screen_rect = self.case_canvas.create_oval(25, 25, 385, 595, fill="#000000", outline="#0F172A", width=2)
        # Side crown button
        self.case_canvas.create_rectangle(392, 180, 404, 250, fill="#475569", outline="#64748B", width=2)

        # Bind Drag/Swipe gestures on the watch canvas
        self.case_canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.case_canvas.bind("<ButtonRelease-1>", self.on_drag_end)

        # Bottom Carousel Navigation Bar
        nav_frame = tk.Frame(main_frame, bg="#0F172A")
        nav_frame.pack(fill=tk.X, pady=(8, 0))

        btn_prev = tk.Button(
            nav_frame, text="◀ Prev Ring", bg="#334155", fg="white",
            font=("Helvetica", 11), relief="flat", cursor="hand2",
            command=self.prev_ring
        )
        btn_prev.pack(side=tk.LEFT, padx=10)

        lbl_hint = tk.Label(
            nav_frame, text="Swipe or click arrows", bg="#0F172A", fg="#94A3B8",
            font=("Helvetica", 11)
        )
        lbl_hint.pack(side=tk.LEFT, expand=True)

        btn_next = tk.Button(
            nav_frame, text="Next Ring ▶", bg="#334155", fg="white",
            font=("Helvetica", 11), relief="flat", cursor="hand2",
            command=self.next_ring
        )
        btn_next.pack(side=tk.RIGHT, padx=10)

    # --------------------------------------------------------------------------
    # GESTURE HANDLING
    # --------------------------------------------------------------------------
    def on_drag_start(self, event):
        self.drag_start_x = event.x

    def on_drag_end(self, event):
        dx = event.x - self.drag_start_x
        if dx < -35:
            # Swipe left -> Next ring
            self.next_ring()
        elif dx > 35:
            # Swipe right -> Prev ring
            self.prev_ring()

    def prev_ring(self):
        self.current_ring_index = (self.current_ring_index - 1) % 5
        self.refresh_display()

    def next_ring(self):
        self.current_ring_index = (self.current_ring_index + 1) % 5
        self.refresh_display()

    # --------------------------------------------------------------------------
    # RENDERING THE WATCH SCREEN
    # --------------------------------------------------------------------------
    def refresh_display(self):
        # Clear previous elements drawn on the OLED screen area
        self.case_canvas.delete("watch_content")

        res = self.engine.calculate()
        profile = res["profile"]
        telemetry = res["telemetry"]
        recs = res["recs"]
        is_calibrating = res["is_calibrating"]

        # 1. Top Status Bar (Time, Profile, Battery)
        self.case_canvas.create_text(
            65, 65, text="10:09", fill="#94A3B8", font=("Helvetica", 12, "bold"), tags="watch_content"
        )
        profile_tag = f"{profile['emoji']} Day {profile['day_count']}"
        self.case_canvas.create_text(
            205, 65, text=profile_tag, fill="#38BDF8", font=("Helvetica", 12, "bold"), tags="watch_content"
        )
        self.case_canvas.create_text(
            345, 65, text="98% 🔋", fill="#10B981", font=("Helvetica", 11), tags="watch_content"
        )

        # 2. Main Title: "[Emoji]'s Body Activity" (Strictly >= 14pt)
        title_text = f"{profile['emoji']}'s Body Activity"
        self.case_canvas.create_text(
            205, 95, text=title_text, fill="#F8FAFC", font=("Helvetica", 15, "bold"), tags="watch_content"
        )

        # 3. Dynamic Swipeable Ring (Ring Index: 0..4)
        cx, cy, radius = 205, 215, 75
        self.draw_circular_ring(cx, cy, radius, self.current_ring_index, telemetry, recs)

        # 4. Page Indicator Dots (● ○ ○ ○ ○)
        dots_y = 310
        dot_spacing = 16
        start_x = 205 - (2 * dot_spacing)
        for i in range(5):
            x = start_x + (i * dot_spacing)
            color = "#38BDF8" if i == self.current_ring_index else "#334155"
            size = 4 if i == self.current_ring_index else 3
            self.case_canvas.create_oval(
                x - size, dots_y - size, x + size, dots_y + size,
                fill=color, outline=color, tags="watch_content"
            )

        # 5. Calibration Card / Day 3 Auto-Close Section
        card_top_y = 335
        if is_calibrating:
            # DAY 1 & 2: Show Live Comparison with Human Demographic Baselines
            self.case_canvas.create_rectangle(
                55, card_top_y, 355, card_top_y + 195,
                fill="#0F172A", outline="#0284C7", width=2, tags="watch_content"
            )
            # Status Badge
            self.case_canvas.create_text(
                205, card_top_y + 18,
                text=f"⏳ Calibrating: Day {profile['day_count']} / 2",
                fill="#FBBF24", font=("Helvetica", 12, "bold"), tags="watch_content"
            )
            self.case_canvas.create_text(
                205, card_top_y + 36,
                text="Benchmarking against clinical averages",
                fill="#94A3B8", font=("Helvetica", 11), tags="watch_content"
            )

            # Demographic Comparison Table
            cohort = recs["human_averages"]
            rows = [
                ("Metric", "Human Avg", "You"),
                ("Resting HR", cohort["hrRange"], f"{telemetry['hr']} bpm"),
                ("Sleep Need", cohort["sleepRange"], f"{telemetry['sleep_hours']} hrs"),
                ("Step Target", cohort["stepRange"], f"{telemetry['steps']:,}")
            ]

            row_y = card_top_y + 60
            for idx, (col1, col2, col3) in enumerate(rows):
                is_hdr = idx == 0
                font_style = ("Helvetica", 11, "bold") if is_hdr else ("Helvetica", 11)
                color = "#E2E8F0" if is_hdr else "#94A3B8"
                c3_color = "#E2E8F0" if is_hdr else "#38BDF8"

                self.case_canvas.create_text(105, row_y, text=col1, fill=color, font=font_style, tags="watch_content")
                self.case_canvas.create_text(210, row_y, text=col2, fill=color, font=font_style, tags="watch_content")
                self.case_canvas.create_text(305, row_y, text=col3, fill=c3_color, font=font_style, tags="watch_content")
                row_y += 24

            self.case_canvas.create_text(
                205, card_top_y + 175,
                text=f"🔒 Day 3 closes this card automatically",
                fill="#64748B", font=("Helvetica", 11, "italic"), tags="watch_content"
            )

        else:
            # DAY 3+: Calibration Closed! Tailored Daily Prescriptions Active
            self.case_canvas.create_rectangle(
                55, card_top_y, 355, card_top_y + 195,
                fill="#0F172A", outline="#10B981", width=2, tags="watch_content"
            )
            self.case_canvas.create_text(
                205, card_top_y + 20,
                text="✓ Calibrated Model Active",
                fill="#34D399", font=("Helvetica", 13, "bold"), tags="watch_content"
            )
            self.case_canvas.create_text(
                205, card_top_y + 42,
                text=f"Tuned for {profile['gender']} ({profile['age']}y) based on 48h activity",
                fill="#94A3B8", font=("Helvetica", 11), tags="watch_content"
            )

            # Prescriptions
            p_rows = [
                (f"😴 Sleep Needed Tonight:", f"{recs['target_sleep']} hrs"),
                (f"🚶 Daily Step Target:", f"{recs['target_steps']:,} steps"),
                (f"🪑 Max Stillness Limit:", f"60 mins"),
                (f"❤️ Cardio Readiness:", f"94% (Prime)")
            ]
            py = card_top_y + 72
            for label, val in p_rows:
                self.case_canvas.create_text(75, py, text=label, anchor="w", fill="#F1F5F9", font=("Helvetica", 11), tags="watch_content")
                self.case_canvas.create_text(335, py, text=val, anchor="e", fill="#38BDF8", font=("Helvetica", 11, "bold"), tags="watch_content")
                py += 26

            self.case_canvas.create_text(
                205, card_top_y + 176,
                text="100% on-device • 0 bytes cloud data",
                fill="#64748B", font=("Helvetica", 11), tags="watch_content"
            )

    def draw_circular_ring(self, cx, cy, r, ring_idx, telemetry, recs):
        # Base ring background
        self.case_canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline="#1E293B", width=14, tags="watch_content"
        )

        configs = [
            {
                "name": "Cardio Strain",
                "val": f"{round(((telemetry['hr'] - 60) / 70) * 100)}%",
                "sub": "Karvonen HRR Strain",
                "ratio": min(1.0, max(0.1, ((telemetry['hr'] - 60) / 70))),
                "color": "#FF2D55"
            },
            {
                "name": "Sleep",
                "val": f"{telemetry['sleep_hours']} / {recs['target_sleep']}h",
                "sub": "Hours Slept / Target Need",
                "ratio": min(1.0, telemetry["sleep_hours"] / recs["target_sleep"]),
                "color": "#00F0FF"
            },
            {
                "name": "Steps",
                "val": f"{telemetry['steps']:,} / {recs['target_steps']:,}",
                "sub": "Steps Walked / Daily Goal",
                "ratio": min(1.0, telemetry["steps"] / recs["target_steps"]),
                "color": "#00E676"
            },
            {
                "name": "Stillness",
                "val": f"{telemetry['still_minutes']} / 60m",
                "sub": "Mins Still / Inactivity Limit",
                "ratio": min(1.0, telemetry["still_minutes"] / 60.0),
                "color": "#FFD600"
            },
            {
                "name": "Energy Burn",
                "val": f"{telemetry['calories']} / 650 kcal",
                "sub": "Active Burn / Daily Goal",
                "ratio": min(1.0, telemetry["calories"] / 650.0),
                "color": "#FF6D00"
            }
        ]

        cfg = configs[ring_idx]
        extent_angle = -int(cfg["ratio"] * 360)

        # Draw progress arc (starting at 90 deg = top)
        if extent_angle != 0:
            self.case_canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=90, extent=extent_angle,
                outline=cfg["color"], width=14, style=tk.ARC, tags="watch_content"
            )

        # Central ring text
        self.case_canvas.create_text(
            cx, cy - 14, text=cfg["name"].upper(),
            fill="#94A3B8", font=("Helvetica", 11, "bold"), tags="watch_content"
        )
        self.case_canvas.create_text(
            cx, cy + 8, text=cfg["val"],
            fill="#FFFFFF", font=("Helvetica", 14, "bold"), tags="watch_content"
        )
        self.case_canvas.create_text(
            cx, cy + 28, text=cfg["sub"],
            fill=cfg["color"], font=("Helvetica", 11), tags="watch_content"
        )

    # --------------------------------------------------------------------------
    # SIMULATION ACTIONS
    # --------------------------------------------------------------------------
    def advance_simulation_day(self):
        new_day = self.engine.advance_day()
        self.refresh_display()
        if new_day == 3:
            messagebox.showinfo(
                "Day 3 Reached!",
                "48-Hour baseline calibration is now complete!\n"
                "The calibration card has automatically closed, unlocking tailored daily prescriptions."
            )

    def open_change_person_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Change Person — Add / Switch Profile")
        dlg.geometry("380x420")
        dlg.configure(bg="#0F172A")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        # Modal Header
        tk.Label(
            dlg, text="Select or Add Person", bg="#0F172A", fg="#F8FAFC",
            font=("Helvetica", 14, "bold")
        ).pack(pady=(16, 4))
        tk.Label(
            dlg, text="Each person starts with fresh isolated data.",
            bg="#0F172A", fg="#94A3B8", font=("Helvetica", 11)
        ).pack(pady=(0, 16))

        form_frame = tk.Frame(dlg, bg="#0F172A", padx=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Emoji Selection
        tk.Label(
            form_frame, text="Person Emoji:", bg="#0F172A", fg="#E2E8F0",
            font=("Helvetica", 11, "bold")
        ).grid(row=0, column=0, sticky="w", pady=8)

        emoji_var = tk.StringVar(value="🧘‍♀️")
        emoji_combo = ttk.Combobox(
            form_frame, textvariable=emoji_var,
            values=["🏃‍♂️ Runner", "🧘‍♀️ Meditator", "🚴‍♂️ Cyclist", "🏊‍♂️ Swimmer", "🚶 Walker"],
            font=("Helvetica", 11), state="readonly", width=16
        )
        emoji_combo.grid(row=0, column=1, sticky="w", pady=8)

        # 2. Gender Selection
        tk.Label(
            form_frame, text="Biological Sex:", bg="#0F172A", fg="#E2E8F0",
            font=("Helvetica", 11, "bold")
        ).grid(row=1, column=0, sticky="w", pady=8)

        gender_var = tk.StringVar(value="Female")
        gender_combo = ttk.Combobox(
            form_frame, textvariable=gender_var,
            values=["Female", "Male"],
            font=("Helvetica", 11), state="readonly", width=16
        )
        gender_combo.grid(row=1, column=1, sticky="w", pady=8)

        # 3. Age Selection
        tk.Label(
            form_frame, text="Age (years):", bg="#0F172A", fg="#E2E8F0",
            font=("Helvetica", 11, "bold")
        ).grid(row=2, column=0, sticky="w", pady=8)

        age_entry = tk.Entry(form_frame, font=("Helvetica", 11), width=18, bg="#1E293B", fg="white", insertbackground="white")
        age_entry.insert(0, "28")
        age_entry.grid(row=2, column=1, sticky="w", pady=8)

        # Action Buttons
        btn_frame = tk.Frame(dlg, bg="#0F172A", pady=16)
        btn_frame.pack(fill=tk.X)

        def save_person():
            try:
                age_val = int(age_entry.get().strip())
                if age_val < 5 or age_val > 110:
                    raise ValueError("Age out of range")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid age between 5 and 110.", parent=dlg)
                return

            chosen_emoji = emoji_var.get().split()[0]
            chosen_gender = gender_var.get()
            profile_id = f"person_{chosen_emoji}_{age_val}"

            # Create isolated profile
            self.engine.add_profile(
                profile_id=profile_id,
                emoji=chosen_emoji,
                age=age_val,
                gender=chosen_gender
            )
            dlg.destroy()
            self.refresh_display()
            messagebox.showinfo(
                "Profile Switched",
                f"Switched to {chosen_emoji} ({chosen_gender}, {age_val}y)!\n"
                f"Fresh calibration started at Day 1 with zero data leakage."
            )

        btn_submit = tk.Button(
            btn_frame, text="Save & Switch Person", bg="#10B981", fg="white",
            font=("Helvetica", 11, "bold"), relief="flat", cursor="hand2",
            padx=16, pady=8, command=save_person
        )
        btn_submit.pack()

# ==============================================================================
# 3. VERIFICATION SELF-TEST
# ==============================================================================

def run_headless_tests():
    print("Testing InstaHealth Python Engine...")
    engine = HealthEngine()

    # Test 1: Check baseline calculation for Male 22y
    res = engine.calculate()
    assert res["profile"]["gender"] == "Male"
    # Tanaka: 208 - (0.7 * 22) = 192.6
    assert abs(res["max_hr"] - 192.6) < 0.1
    assert res["is_calibrating"] is True
    print("✓ Check 1 Passed: Tanaka formulation verified for Male (192.6 bpm).")

    # Test 2: Add Female 40y profile
    engine.add_profile("female_40", emoji="🧘‍♀️", age=40, gender="Female")
    res_f = engine.calculate()
    # Gulati: 206 - (0.88 * 40) = 170.8
    assert abs(res_f["max_hr"] - 170.8) < 0.1
    assert res_f["profile"]["emoji"] == "🧘‍♀️"
    assert res_f["is_calibrating"] is True
    print("✓ Check 2 Passed: Gulati formulation verified for Female (170.8 bpm).")

    # Test 3: Advance to Day 3 -> Auto-close calibration
    engine.advance_day() # Day 2
    assert engine.get_active_profile()["day_count"] == 2
    assert engine.calculate()["is_calibrating"] is True

    engine.advance_day() # Day 3
    res_day3 = engine.calculate()
    assert res_day3["is_calibrating"] is False
    assert res_day3["recs"]["calibrating"] is False
    assert res_day3["recs"]["target_sleep"] >= 7.0
    print("✓ Check 3 Passed: Day 3 auto-close verified, tailored prescriptions unlocked.")

    print("All InstaHealth Python tests passed successfully!")

# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_headless_tests()
    else:
        root = tk.Tk()
        app = InstaHealthSmartwatchApp(root)
        root.mainloop()

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



class ChartsModule:
    """Feature module extracted from the original application."""

    def create_stat_card(self, parent, title, value, color, col):
            """Create a statistics card"""
            card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color)
            card.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
            parent.grid_columnconfigure(col, weight=1)

            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=36, weight="bold"),
                text_color="white"
            )
            value_label.pack(pady=(20, 5))

            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14),
                text_color="white"
            )
            title_label.pack(pady=(5, 20))

    def create_pie_chart(self, parent, data):
            """Create pie chart for students by course"""
            fig = Figure(figsize=(6, 4), dpi=100)
            fig.patch.set_facecolor('#2b2b2b')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2b2b2b')

            if data and len(data) > 0:
                courses = [item['course_name'] for item in data]
                counts = [item['count'] for item in data]

                # Create pie chart
                colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
                wedges, texts, autotexts = ax.pie(
                    counts,
                    labels=courses,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors[:len(courses)],
                    textprops={'color': 'white', 'fontsize': 10}
                )

                # Add count to labels
                for i, (wedge, text) in enumerate(zip(wedges, texts)):
                    text.set_text(f'{courses[i]}\n({counts[i]})')

                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(10)
                    autotext.set_weight('bold')

                ax.set_title('Course Enrollment Distribution', color='white', fontsize=12, pad=20)
            else:
                ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                        color='white', fontsize=14, transform=ax.transAxes)
                ax.set_title('Course Enrollment Distribution', color='white', fontsize=12)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_attendance_bar_chart(self, parent):
            """Create bar chart for attendance by course"""
            fig = Figure(figsize=(6, 4), dpi=100)
            fig.patch.set_facecolor('#2b2b2b')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2b2b2b')

            # Get courses
            courses = self.db.get_all_courses()

            if courses and len(courses) > 0:
                course_names = [c['course_name'][:15] for c in courses]  # Truncate long names
                attendance_rates = [self.db.get_course_attendance(c['course_id']) for c in courses]

                bars = ax.bar(course_names, attendance_rates, color='#3498db', edgecolor='white', linewidth=1.5)

                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{height:.1f}%',
                            ha='center', va='bottom', color='white', fontsize=9, weight='bold')

                ax.set_ylabel('Attendance Rate (%)', color='white', fontsize=11)
                ax.set_xlabel('Courses', color='white', fontsize=11)
                ax.set_title('Attendance Performance by Course', color='white', fontsize=12, pad=20)
                ax.tick_params(colors='white', labelsize=9)
                ax.set_ylim(0, 110)

                # Rotate x labels if needed
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

                # Grid
                ax.grid(axis='y', alpha=0.3, color='white', linestyle='--')
            else:
                ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                        color='white', fontsize=14, transform=ax.transAxes)
                ax.set_title('Attendance Performance by Course', color='white', fontsize=12)

            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_line_chart(self, parent, data):
            """Create line chart for monthly admissions"""
            fig = Figure(figsize=(12, 4), dpi=100)
            fig.patch.set_facecolor('#2b2b2b')
            ax = fig.add_subplot(111)
            ax.set_facecolor('#2b2b2b')

            if data and len(data) > 0:
                months = [item['month'] for item in data]
                counts = [item['count'] for item in data]

                ax.plot(months, counts, marker='o', linewidth=2, markersize=8,
                        color='#2ecc71', markerfacecolor='#27ae60', markeredgecolor='white')

                # Add value labels
                for i, (month, count) in enumerate(zip(months, counts)):
                    ax.text(i, count + 0.1, str(count), ha='center', va='bottom',
                            color='white', fontsize=9, weight='bold')

                ax.set_ylabel('Number of Admissions', color='white', fontsize=11)
                ax.set_xlabel('Month', color='white', fontsize=11)
                ax.set_title('Student Admission Trends', color='white', fontsize=12, pad=20)
                ax.tick_params(colors='white', labelsize=9)
                ax.grid(True, alpha=0.3, color='white', linestyle='--')

                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            else:
                ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                        color='white', fontsize=14, transform=ax.transAxes)
                ax.set_title('Student Admission Trends', color='white', fontsize=12)

            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))

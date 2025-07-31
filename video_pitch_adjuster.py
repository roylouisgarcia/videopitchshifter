#!/usr/bin/env python3
"""
Video Pitch Adjuster GUI
A GUI application that uses FFMPEG to:
1. Extract audio from video
2. Adjust audio pitch
3. Merge adjusted audio back to video
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import threading
from pathlib import Path
import tempfile

class VideoPitchAdjusterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Pitch Adjuster")
        self.root.geometry("800x600")
        
        # Color theme based on #1d2951
        self.colors = {
            'primary': '#1d2951',        # Main color
            'primary_light': '#2a3862',  # Lighter shade
            'primary_dark': '#141f3d',   # Darker shade
            'accent': '#4a90e2',         # Blue accent
            'accent_hover': '#357abd',   # Darker blue for hover
            'background': '#f5f6fa',     # Light background
            'text_dark': '#2c3e50',      # Dark text
            'text_light': '#ffffff',     # Light text
            'border': '#ddd',            # Border color
            'success': '#e5cb12',        # Success color (changed from green to golden yellow)
            'warning': '#f39c12',        # Warning color
            'error': '#e74c3c'           # Error color
        }
        
        # Configure the theme
        self.setup_theme()
        
        # Variables
        self.input_video_path = tk.StringVar()
        self.output_video_path = tk.StringVar()
        self.pitch_adjustment = tk.DoubleVar(value=0.0)
        self.processing = False
        
        # Create GUI elements
        self.create_widgets()
        
    def setup_theme(self):
        """Configure the custom theme"""
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Main.TFrame',
                       background=self.colors['background'],
                       relief='flat')
        
        style.configure('Primary.TFrame',
                       background=self.colors['primary'],
                       relief='flat')
        
        style.configure('Card.TLabelframe',
                       background=self.colors['background'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'])
        
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Arial', 10, 'bold'))
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Arial', 18, 'bold'))
        
        style.configure('Main.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_dark'],
                       font=('Arial', 9))
        
        style.configure('Value.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['accent'],
                       font=('Arial', 9, 'bold'))
        
        style.configure('Status.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_dark'],
                       font=('Arial', 9))
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],  # Changed to use primary color (#1d2951)
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['primary'],
                       focuscolor='none',
                       font=('Arial', 9, 'bold'))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', self.colors['primary_dark'])],
                 foreground=[('active', self.colors['text_light']),
                           ('pressed', self.colors['text_light'])])
        
        style.configure('Accent.TButton',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],  # Changed to use primary color (#1d2951)
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['primary'],
                       focuscolor='none',
                       font=('Arial', 9, 'bold'))
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['primary_dark'])],
                 foreground=[('active', self.colors['text_light']),
                           ('pressed', self.colors['text_light'])])
        
        style.configure('Small.TButton',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],  # Changed to use primary color (#1d2951)
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['primary'],
                       focuscolor='none',
                       font=('Arial', 8, 'bold'),
                       padding=(8, 4))
        
        style.map('Small.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', self.colors['primary_dark'])],
                 foreground=[('active', self.colors['text_light']),
                           ('pressed', self.colors['text_light'])])
        
        # Configure entry styles
        style.configure('Main.TEntry',
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       font=('Arial', 9))
        
        # Configure scale styles
        style.configure('Main.Horizontal.TScale',
                       background=self.colors['background'],
                       troughcolor=self.colors['border'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
        # Configure progressbar styles
        style.configure('Main.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['border'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title with custom styling
        title_frame = ttk.Frame(main_frame, style='Primary.TFrame', padding="20")
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, text="🎵 Video Pitch Adjuster", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame, text="Professional audio pitch adjustment with video sync preservation",
                                  style='Main.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Input video section
        ttk.Label(main_frame, text="Input Video File:", style='Main.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=(10, 5))
        ttk.Entry(main_frame, textvariable=self.input_video_path, width=50, style='Main.TEntry').grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 5), padx=(10, 10))
        ttk.Button(main_frame, text="Browse", style='Accent.TButton',
                  command=self.browse_input_video).grid(row=1, column=2, pady=(10, 5), padx=(0, 5))
        
        # Output video section
        ttk.Label(main_frame, text="Output Video File:", style='Main.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_video_path, width=50, style='Main.TEntry').grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 10))
        ttk.Button(main_frame, text="Browse", style='Accent.TButton',
                  command=self.browse_output_video).grid(row=2, column=2, pady=5, padx=(0, 5))
        
        # Pitch adjustment section
        pitch_frame = ttk.LabelFrame(main_frame, text="🎛️ Pitch Adjustment Controls", 
                                   padding="15", style='Card.TLabelframe')
        pitch_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        pitch_frame.columnconfigure(1, weight=1)
        
        ttk.Label(pitch_frame, text="Pitch Adjustment:", style='Main.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Pitch slider
        self.pitch_scale = ttk.Scale(pitch_frame, from_=-20, to=20, 
                                    variable=self.pitch_adjustment, 
                                    orient=tk.HORIZONTAL, length=350,
                                    style='Main.Horizontal.TScale',
                                    command=self.update_pitch_label)
        self.pitch_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(15, 15), pady=(0, 10))
        
        # Pitch value label
        self.pitch_value_label = ttk.Label(pitch_frame, text="0.0 semitones", style='Value.TLabel')
        self.pitch_value_label.grid(row=0, column=2, sticky=tk.W, pady=(0, 10))
        
        # Preset buttons with improved styling
        preset_frame = ttk.Frame(pitch_frame, style='Main.TFrame')
        preset_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(preset_frame, text="Quick Adjustments:", style='Main.TLabel').pack(pady=(0, 8))
        
        button_frame = ttk.Frame(preset_frame, style='Main.TFrame')
        button_frame.pack()
        
        ttk.Button(button_frame, text="−1", width=6, style='Small.TButton',
                  command=lambda: self.adjust_pitch(-1)).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="Reset", width=6, style='Primary.TButton',
                  command=lambda: self.set_pitch(0)).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="+1", width=6, style='Small.TButton',
                  command=lambda: self.adjust_pitch(1)).pack(side=tk.LEFT, padx=3)
        
        # Processing section
        process_frame = ttk.LabelFrame(main_frame, text="🚀 Processing Controls", 
                                     padding="15", style='Card.TLabelframe')
        process_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        process_frame.columnconfigure(0, weight=1)
        
        # Process button
        self.process_button = ttk.Button(process_frame, text="🎬 Process Video", 
                                        style='Primary.TButton',
                                        command=self.process_video)
        self.process_button.grid(row=0, column=0, pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(process_frame, mode='indeterminate', 
                                      style='Main.Horizontal.TProgressbar')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(process_frame, text="✅ Ready to process", style='Status.TLabel')
        self.status_label.grid(row=2, column=0, pady=(0, 5))
        
        # Log text area with custom styling
        log_frame = ttk.LabelFrame(main_frame, text="📋 Process Log", 
                                 padding="15", style='Card.TLabelframe')
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Text widget with scrollbar and custom colors
        text_frame = ttk.Frame(log_frame, style='Main.TFrame')
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=8, wrap=tk.WORD,
                               bg='#ffffff', fg=self.colors['text_dark'],
                               font=('Consolas', 9), relief='solid', bd=1,
                               selectbackground=self.colors['accent'],
                               selectforeground=self.colors['text_light'])
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def browse_input_video(self):
        """Browse for input video file"""
        filename = filedialog.askopenfilename(
            title="Select Input Video",
            filetypes=[
                ("Video files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_video_path.set(filename)
            # Auto-generate output filename based on current pitch
            if not self.output_video_path.get():
                self.update_output_filename_for_pitch()
            
    def browse_output_video(self):
        """Browse for output video file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Video As",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 files", "*.mp4"),
                ("MKV files", "*.mkv"),
                ("AVI files", "*.avi"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_video_path.set(filename)
            
    def update_pitch_label(self, value):
        """Update the pitch value label"""
        pitch_value = float(value)
        self.pitch_value_label.config(text=f"{pitch_value:.1f} semitones")
        
        # Update output filename based on pitch direction
        self.update_output_filename_for_pitch()
        
    def update_output_filename_for_pitch(self):
        """Update output filename based on current pitch adjustment"""
        if not self.input_video_path.get():
            return
            
        input_path = Path(self.input_video_path.get())
        current_pitch = self.pitch_adjustment.get()
        
        # Determine the appropriate suffix based on pitch direction
        if abs(current_pitch) < 0.1:  # Close to zero
            suffix = "pitch_adjusted"
        elif current_pitch > 0:
            suffix = "higher"
        else:  # current_pitch < 0
            suffix = "lower"
        
        # Generate new output filename
        output_filename = f"{input_path.stem}_{suffix}{input_path.suffix}"
        output_path = input_path.parent / output_filename
        
        # Check if the auto-generated name already exists and make it unique
        if output_path.exists():
            output_path = self._generate_unique_filename(str(output_path))
        
        self.output_video_path.set(str(output_path))
        
    def set_pitch(self, value):
        """Set pitch to specific value"""
        self.pitch_adjustment.set(value)
        self.update_pitch_label(str(value))
        
    def adjust_pitch(self, increment):
        """Adjust pitch by incrementing/decrementing current value"""
        current_value = self.pitch_adjustment.get()
        new_value = current_value + increment
        
        # Clamp to slider bounds
        min_val = -20
        max_val = 20
        new_value = max(min_val, min(max_val, new_value))
        
        self.pitch_adjustment.set(new_value)
        self.update_pitch_label(str(new_value))
        
    def log_message(self, message, msg_type="info"):
        """Add message to log with color coding"""
        self.log_text.insert(tk.END, f"{message}\n")
        
        # Color code different message types
        if msg_type == "error":
            # Color the last line red
            line_start = self.log_text.index("end-2l linestart")
            line_end = self.log_text.index("end-2l lineend")
            self.log_text.tag_add("error", line_start, line_end)
            self.log_text.tag_config("error", foreground=self.colors['error'])
        elif msg_type == "success":
            # Color the last line green
            line_start = self.log_text.index("end-2l linestart")
            line_end = self.log_text.index("end-2l lineend")
            self.log_text.tag_add("success", line_start, line_end)
            self.log_text.tag_config("success", foreground=self.colors['success'])
        elif msg_type == "warning":
            # Color the last line orange
            line_start = self.log_text.index("end-2l linestart")
            line_end = self.log_text.index("end-2l lineend")
            self.log_text.tag_add("warning", line_start, line_end)
            self.log_text.tag_config("warning", foreground=self.colors['warning'])
        elif msg_type == "step":
            # Color step headers with primary color
            line_start = self.log_text.index("end-2l linestart")
            line_end = self.log_text.index("end-2l lineend")
            self.log_text.tag_add("step", line_start, line_end)
            self.log_text.tag_config("step", foreground=self.colors['primary'], font=('Consolas', 9, 'bold'))
        
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, 
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            return result.returncode == 0
        except FileNotFoundError:
            return False
            
    def process_video(self):
        """Main processing function"""
        if self.processing:
            return
            
        # Validate inputs
        if not self.input_video_path.get():
            messagebox.showerror("Error", "Please select an input video file")
            return
            
        if not self.output_video_path.get():
            messagebox.showerror("Error", "Please specify an output video file")
            return
            
        if not os.path.exists(self.input_video_path.get()):
            messagebox.showerror("Error", "Input video file does not exist")
            return
        
        # Check if output file already exists
        output_path = self.output_video_path.get()
        if os.path.exists(output_path):
            choice = messagebox.askyesnocancel(
                "File Already Exists",
                f"The output file already exists:\n{output_path}\n\n"
                "Yes = Overwrite the existing file\n"
                "No = Choose a different filename\n"
                "Cancel = Stop processing"
            )
            
            if choice is None:  # Cancel
                return
            elif choice is False:  # No - choose different filename
                # Generate a unique filename
                output_path = self._generate_unique_filename(output_path)
                self.output_video_path.set(output_path)
                self.log_message(f"Output filename changed to: {output_path}")
            else:  # Yes - overwrite
                self.log_message(f"Will overwrite existing file: {output_path}")
            
        # Check ffmpeg
        if not self.check_ffmpeg():
            messagebox.showerror("Error", 
                               "FFMPEG not found. Please install FFMPEG and add it to your PATH")
            return
            
        # Start processing in a separate thread
        self.processing = True
        self.process_button.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="⚙️ Processing...")
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self._process_video_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_unique_filename(self, original_path):
        """Generate a unique filename by adding a number suffix"""
        path_obj = Path(original_path)
        base_name = path_obj.stem
        extension = path_obj.suffix
        directory = path_obj.parent
        
        counter = 1
        while True:
            new_filename = f"{base_name}_{counter}{extension}"
            new_path = directory / new_filename
            if not new_path.exists():
                return str(new_path)
            counter += 1
        
    def _process_video_thread(self):
        """Processing thread function"""
        try:
            input_path = self.input_video_path.get()
            output_path = self.output_video_path.get()
            pitch_change = self.pitch_adjustment.get()
            
            # Create temporary directory for intermediate files
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_audio = os.path.join(temp_dir, "extracted_audio.wav")
                temp_pitched_audio = os.path.join(temp_dir, "pitched_audio.wav")
                
                self.log_message("Starting video processing...", "step")
                self.log_message(f"Input: {input_path}")
                self.log_message(f"Output: {output_path}")
                self.log_message(f"Pitch adjustment: {pitch_change:.1f} semitones")
                
                # Step 1: Extract audio from video
                self.log_message("\nStep 1: Extracting audio from video...", "step")
                extract_cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
                    temp_audio, '-y'
                ]
                
                result = subprocess.run(extract_cmd, capture_output=True, text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise Exception(f"Audio extraction failed: {result.stderr}")
                    
                self.log_message("Audio extraction completed successfully", "success")
                
                # Step 2: Adjust pitch (only if pitch change is not zero)
                if abs(pitch_change) > 0.01:  # Small threshold to avoid processing for tiny changes
                    self.log_message(f"\nStep 2: Adjusting pitch by {pitch_change:.1f} semitones...", "step")
                    
                    # Calculate pitch shift factor
                    # Formula: 2^(semitones/12) for frequency ratio
                    pitch_ratio = 2 ** (pitch_change / 12.0)
                    
                    # Use rubberband or atempo+asetrate combination to maintain duration
                    # Method 1: Try rubberband first (best quality, maintains duration)
                    pitch_cmd_rubberband = [
                        'ffmpeg', '-i', temp_audio,
                        '-af', f'rubberband=pitch={pitch_ratio}',
                        temp_pitched_audio, '-y'
                    ]
                    
                    # Method 2: Fallback using atempo and asetrate (maintains duration)
                    # Split the adjustment: first change pitch, then adjust tempo to restore duration
                    tempo_ratio = 1.0 / pitch_ratio  # Compensate for duration change
                    pitch_cmd_fallback = [
                        'ffmpeg', '-i', temp_audio,
                        '-af', f'asetrate=44100*{pitch_ratio},aresample=44100,atempo={tempo_ratio}',
                        temp_pitched_audio, '-y'
                    ]
                    
                    # Try rubberband first, fall back to atempo method if not available
                    self.log_message("Trying rubberband filter for best quality...")
                    result = subprocess.run(pitch_cmd_rubberband, capture_output=True, text=True,
                                          creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    if result.returncode != 0:
                        self.log_message("Rubberband not available, using atempo method...")
                        pitch_cmd = pitch_cmd_fallback
                    else:
                        self.log_message("Using rubberband method for pitch adjustment")
                        pitch_cmd = pitch_cmd_rubberband
                    
                    # Run the selected pitch adjustment method
                    if result.returncode != 0:  # Only run if rubberband failed
                        result = subprocess.run(pitch_cmd, capture_output=True, text=True,
                                              creationflags=subprocess.CREATE_NO_WINDOW)
                    
                    if result.returncode != 0:
                        raise Exception(f"Pitch adjustment failed: {result.stderr}")
                        
                    self.log_message("Pitch adjustment completed successfully (duration preserved)", "success")
                    audio_to_merge = temp_pitched_audio
                else:
                    self.log_message("\nStep 2: No pitch adjustment needed (0 semitones)", "step")
                    audio_to_merge = temp_audio
                
                # Step 3: Merge adjusted audio back with video
                self.log_message("\nStep 3: Merging audio back with video...", "step")
                merge_cmd = [
                    'ffmpeg', '-i', input_path, '-i', audio_to_merge,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-map', '0:v:0', '-map', '1:a:0',
                    output_path, '-y'
                ]
                
                result = subprocess.run(merge_cmd, capture_output=True, text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode != 0:
                    raise Exception(f"Video merging failed: {result.stderr}")
                    
                self.log_message("Video merging completed successfully", "success")
                self.log_message(f"\nProcessing completed! Output saved to: {output_path}", "success")
                
                # Show success message
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Video processing completed successfully!\nOutput saved to:\n{output_path}"))
                
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.log_message(f"\nERROR: {error_msg}", "error")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            # Reset UI state
            self.root.after(0, self._reset_ui_state)
            
    def _reset_ui_state(self):
        """Reset UI to ready state"""
        self.processing = False
        self.process_button.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="✅ Ready to process")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set window icon if available (optional)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = VideoPitchAdjusterGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()

# StucyTracker

**A lightweight desktop Pomodoro timer designed for students.**

StucyTracker is an open-source desktop application built with Python to help students organize, track, and measure their study sessions using the Pomodoro Technique.

The goal is to provide a simple, customizable, and lightweight tool that runs locally on your computer, allowing users to focus on studying without unnecessary distractions.

## Features

### Planned Features

- [ ] Customizable Pomodoro and break durations.
- [ ] Study session management.
- [ ] Subject and exam selection.
- [ ] System tray integration.
- [ ] Floating timer widget.
- [ ] Automatic study session tracking.
- [ ] Excel integration for recording study sessions.
- [ ] Productivity statistics.

## Tech Stack

- **Python** – Main programming language.
- **Tkinter** – Desktop graphical interface.
- **uv** – Python project and dependency management.
- **openpyxl** – Excel file integration.
- **pystray** – System tray integration.
- **Pillow** – Image processing and application icons.
- **pytest** – Automated testing.

## Project Structure

```text
stucy-tracker/
├── src/
│   └── stucy_tracker/
│       ├── core/
│       ├── gui/
│       ├── integrations/
│       └── config/
├── tests/
├── assets/
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

## Installation

*Installation instructions will be added as the project develops.*

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency and environment management.

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/stucy-tracker.git
cd stucy-tracker
```

Install project dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run python -m stucy_tracker.main
```

## Roadmap

- **v0.1 – Core:** Timer engine, session management and configuration.
- **v0.2 – Desktop UI:** Main window, floating widget and system tray.
- **v0.3 – Academic Tracking:** Subjects, exams and Excel integration.
- **v1.0 – First Release:** Testing, documentation and distribution.

## Contributing

Contributions, suggestions and bug reports are welcome.

Feel free to open an issue to discuss improvements or report problems.

## License

License to be determined.

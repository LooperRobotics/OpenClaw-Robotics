# Contributing to Unitree Robot WhatsApp Control

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### 1. Reporting Bugs

- Search existing issues to avoid duplicates
- Use the bug report template
- Include:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots/logs if applicable
  - Environment details (OS, Python version, etc.)

### 2. Suggesting Features

- Check existing feature requests
- Use the feature request template
- Explain:
  - The problem you're solving
  - Proposed solution
  - Alternative solutions considered
  - Any relevant examples or references

### 3. Submitting Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make your changes
4. Run tests:
   ```bash
   pytest tests/ -v
   ```
5. Run linting:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```
6. Commit with clear messages:
   ```bash
   git commit -m "Add amazing feature: solves issue #123"
   ```
7. Push and create PR:
   ```bash
   git push origin feature/amazing-feature
   ```

## 📝 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all functions
- Write docstrings for public methods
- Keep functions small and focused

### Example

```python
def move_forward(speed: float = 0.5, duration: float = 0.0) -> bool:
    """
    Move the robot forward at specified speed.
    
    Args:
        speed: Movement speed (0.0 to 1.0)
        duration: Movement duration in seconds (0 for continuous)
    
    Returns:
        bool: True if command executed successfully
    
    Raises:
        ValueError: If speed is outside valid range
    """
    if not 0.0 <= speed <= 1.0:
        raise ValueError(f"Speed must be between 0.0 and 1.0, got {speed}")
    
    # Implementation
    return True
```

### Testing

- Write unit tests for new functionality
- Aim for 80%+ code coverage
- Use descriptive test names:
  ```python
  def test_move_forward_with_valid_speed_returns_success(self):
      pass
  ```

## 🔧 Development Setup

```bash
# Fork and clone
git clone https://github.com/YOURUSERNAME/unitree-whatsapp-control.git
cd unitree-whatsapp-control

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v --cov=src

# Check types
mypy src/

# Format code
black src/ tests/

# Lint
flake8 src/ tests/
```

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update docs/ for architecture changes
- Include examples for new features

## 🐛 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority: high` - Must be fixed soon
- `priority: low` - Nice to have

## 💬 Community

- Be respectful and inclusive
- Help others in issues and discussions
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Use clear, concise language

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## 🙏 Recognition

Contributors will be listed in:
- [README.md](README.md) Contributors section
- [GitHub Contributors](https://github.com/yourusername/unitree-whatsapp-control/graphs/contributors)

Thank you for helping make this project better! 🎉

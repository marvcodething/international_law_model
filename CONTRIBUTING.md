# Contributing to Contract Analysis Platform

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/contract-analysis-platform.git
cd contract-analysis-platform
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Coding Standards

- Use clear, descriptive function names.
- Add function descriptors and parameter descriptions as comments:

```python
# FUNC: Brief description of what function does
# PARAM: parameter_name - description
# RETURN: description of return value
def your_function(parameter_name):
    pass
```

- Use type hints for all functions:

```python
def analyze_contract(text: str, jurisdiction: str = "both") -> dict:
    pass
```

- Keep functions focused and organized in appropriate modules.

## Commit Messages

Use clear, descriptive commit messages:

```
type(scope): brief description

Longer description if needed explaining the motivation and implementation details.

Fixes #123
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks
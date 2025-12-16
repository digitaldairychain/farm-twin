# Contributing to { farm-twin } #

Welcome! We're excited you want to contribute to the { farm-twin } project. This document outlines the process for contributing code, setting up your environment, and ensuring your changes meet our quality standards.

## Environment Setup ## 
We recommend using a virtual environment to manage project dependencies independently from your system Python installation.

Create and activate a virtual environment:
```bash
python -m venv farm-twin-env
source farm-twin-env/bin/activate
```

Install project dependencies:
```bash
pip install -r dev/requirements_dev.txt
```

## Coding Standards ##

All Python code must follow the PEP 8 style guide. Key requirements:

- Indentation: Use 4 spaces per indentation level
- Line Length: Limit all lines to a maximum of 79 characters (where possible and practicable)
- Naming Conventions:
    - Variables and functions: snake_case (e.g., calculate_total)
    - Classes: PascalCase (e.g., DataProcessor)
    - Constants: UPPER_SNAKE_CASE (e.g., MAX_CONNECTIONS)
- Whitespace:
    - Use single spaces around operators and after commas
    - No spaces immediately inside parentheses, brackets, or braces
- Blank Lines:
    - Two blank lines before top-level function and class definitions
    - One blank line between methods in classes

Example of well-formatted code:
```python
def calculate_animal_feed(animal_type, weight):
    """Calculate recommended feed amount based on animal type and weight."""
    if weight <= 0:
        raise ValueError('Weight must be positive')
    
    base_rate = get_base_feed_rate(animal_type)
    return base_rate * weight
```

## Automated Code Quality Tools ##
We use several tools to maintain code quality. Run these before submitting your pull request:

```bash
isort .
ruff format
flake8 
```

## Pull Request Process ##

Create a feature Branch, writing focused commits with clear messages. Keep changes small and focused - ideally under 200 lines. Large features should be broken into multiple smaller Pull Requests.

Once complete, open a Pull Request, providing a clear, descriptive title and summary. In the message, explain what changes you made and why, includig testing steps for reviewers.

Once received, address review feedback and respond to all reviewer comments. Push additional commits to address feedback.

The CI pipeline will automatically run tests and linting.

# Merge Approval #

Once approved, your Pull Request will be merged into the main branch. Your feature branch will typically be deleted automatically.

# Testing #

We use pytest as our testing framework. Run the full test suite to ensure your changes don't break existing functionality:

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_specific_module.py
```

# Best Practices #

- Code Readability: Write code that is self-documenting with clear variable and function names
- Small PRs: Keep pull requests small and focused - they get reviewed faster and have fewer bugs
- Testing: Add tests for new functionality and ensure all existing tests pass
- Documentation: Update documentation when changing functionality
- Communication: Ask questions if you're unsure about any part of the codebase

Thank you for contributing to { farm-twin }!

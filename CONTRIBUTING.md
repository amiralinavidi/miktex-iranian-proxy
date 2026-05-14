# Contributing to MiKTeX Iranian Proxy

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Describe the bug briefly
2. **Description**: Detailed explanation of the problem
3. **Steps to reproduce**: How to trigger the bug
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**:
   - OS version
   - Python version
   - MiKTeX version
7. **Screenshots**: If applicable
8. **Logs**: Relevant error messages

**Example:**
```
Title: GUI crashes when fetching package with special characters

Description:
The GUI application crashes when trying to fetch a package name containing 
special characters like "babel-english".

Steps to reproduce:
1. Open GUI
2. Go to Manual Fetch tab
3. Enter "babel-english" in package name field
4. Click "Fetch Package"
5. Application crashes

Expected: Package should be fetched successfully
Actual: Application crashes with error

Environment:
- Windows 11
- Python 3.11
- MiKTeX 25.12

Error log:
[paste error here]
```

### Suggesting Features

For feature requests, create an issue with:

1. **Clear title**: Brief feature description
2. **Problem**: What problem does this solve?
3. **Proposed solution**: How should it work?
4. **Alternatives**: Other ways to solve this
5. **Additional context**: Screenshots, mockups, etc.

### Submitting Code

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: Use clear commit messages
6. **Push**: `git push origin feature/your-feature-name`
7. **Create Pull Request**

## 📝 Code Style

### Python Code

Follow PEP 8 style guide:

```python
# Good
def fetch_package(package_name: str) -> bool:
    """
    Fetch a package from the mirror.
    
    Args:
        package_name: Name of the package to fetch
        
    Returns:
        True if successful, False otherwise
    """
    if not package_name:
        return False
    
    # Implementation here
    return True

# Bad
def fetchPackage(packageName):
    if not packageName: return False
    # Implementation
    return True
```

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add progress bar to package download"
- "Fix crash when package name contains spaces"
- "Update README with new installation instructions"

Bad:
- "fix bug"
- "update"
- "changes"
```

### Documentation

- Add docstrings to all functions
- Update README.md if adding features
- Add comments for complex logic
- Update CHANGELOG.md

## 🧪 Testing

Before submitting:

1. **Test your changes**:
   - Run the GUI application
   - Test all affected features
   - Try edge cases

2. **Check for errors**:
   - No Python errors
   - No crashes
   - Proper error handling

3. **Test on clean environment**:
   - Fresh Python installation
   - Clean MiKTeX setup

## 📋 Pull Request Process

1. **Update documentation**:
   - README.md if needed
   - CHANGELOG.md with your changes
   - Code comments

2. **Describe your changes**:
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?

3. **Link related issues**:
   - "Fixes #123"
   - "Closes #456"

4. **Wait for review**:
   - Respond to feedback
   - Make requested changes
   - Be patient and respectful

## 🎯 Areas for Contribution

### High Priority
- [ ] Progress bars for downloads
- [ ] Better error messages
- [ ] Package search functionality
- [ ] Automatic dependency resolution

### Medium Priority
- [ ] Multiple mirror support
- [ ] Package cache management
- [ ] Export/import package lists
- [ ] Keyboard shortcuts

### Low Priority
- [ ] Themes/dark mode
- [ ] Internationalization (i18n)
- [ ] Plugin system
- [ ] Advanced logging

### Documentation
- [ ] Video tutorials
- [ ] More screenshots
- [ ] FAQ section
- [ ] Troubleshooting guide expansion

## 🌍 Translation

Help translate the application:

1. Create a new language file
2. Translate all strings
3. Test the translation
4. Submit a pull request

## 💡 Ideas Welcome

Have an idea but not sure how to implement it? Create an issue to discuss!

## ❓ Questions

Not sure about something? Feel free to:
- Open an issue with your question
- Start a discussion
- Contact the maintainers

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior:**
- Being respectful and inclusive
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy

**Unacceptable behavior:**
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to the project maintainers.

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the About section

## 📞 Contact

- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and ideas
- **Email**: [Your email if you want to provide one]

---

Thank you for contributing! 🎉

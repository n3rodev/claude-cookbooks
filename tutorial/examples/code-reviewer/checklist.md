# Code Review Checklist

This is a **structured checklist** for comprehensive code reviews. Use it as a final verification step after completing the systematic review in SKILL.md.

## How to Use

- Work through each section systematically
- Check off items as you evaluate them
- Mark items as N/A if they don't apply
- Use this to ensure nothing is missed

**Tip**: Different review types need different sections:
- **Security audit** → Focus on Security section
- **Performance review** → Focus on Performance section
- **New feature** → Focus on Architecture, Testing
- **Bug fix** → Focus on Bug Fix section

---

## Architecture & Design

### Design Principles
- [ ] Code follows Single Responsibility Principle (one reason to change)
- [ ] Dependencies are injected, not created inside functions
- [ ] Clear separation of concerns (UI, business logic, data access)
- [ ] Error handling strategy is consistent
- [ ] No circular dependencies between modules
- [ ] Overall structure is understandable in 30 seconds

### Framework/Language Conventions
- [ ] Code follows language idioms and conventions
- [ ] Design patterns are used appropriately (not over-engineered)
- [ ] Package/module structure is logical
- [ ] Public/private visibility is correct
- [ ] No anti-patterns detected (see style-guide.md)

### Error Handling
- [ ] All critical paths handle errors
- [ ] Errors are caught at appropriate level
- [ ] Error messages provide useful context
- [ ] No silent failures (bare except, swallowing errors)
- [ ] Exceptions are specific (not bare Exception)
- [ ] Errors are logged appropriately

---

## Code Quality

### Readability
- [ ] Variable names are clear and specific
- [ ] Function/method names clearly describe purpose
- [ ] Names avoid ambiguity (no abbreviations unless standard)
- [ ] Code structure is logical and easy to follow
- [ ] Complex logic is explained in comments

### Functions & Methods
- [ ] Functions are focused (one responsibility)
- [ ] Function length is reasonable (< 30 lines typically)
- [ ] Parameters are reasonable in count (< 5 parameters)
- [ ] Return values are clear and consistent
- [ ] No deeply nested code (< 4 levels)

### Comments & Documentation
- [ ] Docstrings explain purpose, not implementation
- [ ] Comments explain *why*, not *what*
- [ ] No commented-out code (dead code should be deleted)
- [ ] TODO/FIXME comments are actionable and dated
- [ ] Code is self-documenting where possible

### DRY (Don't Repeat Yourself)
- [ ] No obvious duplicated code blocks
- [ ] Repeated patterns are extracted to functions
- [ ] No copy-paste code (different variable names, same logic)
- [ ] Configuration is centralized (no magic numbers)

### Complexity
- [ ] Cyclomatic complexity is reasonable (< 10 per function)
- [ ] Boolean logic is clear (not deeply nested conditions)
- [ ] No overly long conditional statements
- [ ] Complex logic is broken into smaller functions

---

## Security & Data Handling

### Secrets & Credentials
- [ ] No hardcoded API keys, passwords, or tokens
- [ ] No hardcoded database connection strings
- [ ] No secret data in logs or error messages
- [ ] No secrets in default parameter values
- [ ] Sensitive values loaded from environment/vault

### Input Validation
- [ ] All user inputs are validated at system boundary
- [ ] Input types are checked (int, string, list, etc.)
- [ ] Input ranges/lengths are validated
- [ ] Format validation present (email, URL, etc.)
- [ ] Null/empty inputs are handled
- [ ] No assumptions about client-side validation

### Data Access Control
- [ ] Authorization checks present where needed
- [ ] Users can only access their own data
- [ ] Admin-only operations are protected
- [ ] Authorization happens BEFORE accessing data
- [ ] Authorization logic is centralized/consistent

### SQL/Database Security
- [ ] SQL queries use parameterized queries (no string concatenation)
- [ ] No raw user input in SQL queries
- [ ] Database connections use secure credentials
- [ ] Connection strings don't expose passwords

### Output Encoding
- [ ] User data is escaped before HTML output
- [ ] User data is escaped before JavaScript/JSON output
- [ ] File paths are validated (no directory traversal)
- [ ] URLs are validated (protocol, domain)

### Sensitive Data Handling
- [ ] Encryption used for sensitive data at rest
- [ ] HTTPS/TLS used for data in transit
- [ ] Sensitive data not logged
- [ ] Sensitive data properly deleted
- [ ] PII handling complies with regulations

---

## Testing

### Test Coverage
- [ ] Happy path is tested
- [ ] Error cases are tested
- [ ] Edge cases are tested (null, empty, max, min)
- [ ] Boundary conditions are tested
- [ ] Critical business logic has tests

### Unit Tests
- [ ] Tests are isolated (no external dependencies)
- [ ] Mock objects are used appropriately
- [ ] One assertion per test (typically)
- [ ] Test names clearly describe what's tested
- [ ] Tests don't depend on execution order
- [ ] Tests are deterministic (not flaky)

### Test Quality
- [ ] Tests verify behavior, not implementation
- [ ] Tests are maintainable (easy to update)
- [ ] No duplicate test code
- [ ] Test setup is clear and minimal
- [ ] Assertions have meaningful messages

### Integration Tests
- [ ] Critical integrations are tested
- [ ] External service failures are handled
- [ ] Data flow between components is tested
- [ ] No dependency on test execution order

### Performance Tests
- [ ] Slow operations have performance baselines
- [ ] Resource-heavy operations are profiled
- [ ] No obvious performance regressions

---

## Performance

### Algorithm Efficiency
- [ ] No O(n²) algorithms where O(n) is possible
- [ ] No repeated expensive computations
- [ ] Sorting is necessary (not done unnecessarily)
- [ ] Search algorithms are appropriate
- [ ] No obvious inefficiencies in loops

### Database Queries
- [ ] No N+1 query problems
- [ ] Queries use indexes appropriately
- [ ] Query results are filtered early (WHERE not application code)
- [ ] Unnecessary columns aren't selected
- [ ] Connection pooling is used

### Resource Usage
- [ ] No memory leaks (long-lived processes)
- [ ] Files are closed (context managers used)
- [ ] Connections are closed/pooled
- [ ] Large data structures are not unnecessarily duplicated
- [ ] Streaming used for large datasets

### Optimization
- [ ] Caching is used where appropriate
- [ ] No premature optimization (readability prioritized)
- [ ] Profile before optimizing
- [ ] Optimization benefits are documented

---

## Dependencies & Maintenance

### Dependency Management
- [ ] External dependencies are justified
- [ ] No unused dependencies
- [ ] Versions are pinned (reproducible builds)
- [ ] Deprecated dependencies are not used
- [ ] Dependency conflicts are resolved

### Code Maintainability
- [ ] Magic numbers are extracted to named constants
- [ ] Configuration is centralized
- [ ] Easy to locate and modify behavior
- [ ] No hidden assumptions about state
- [ ] Clear entry points/public API

### Logging & Observability
- [ ] Error cases are logged with context
- [ ] Log levels are appropriate (INFO, WARN, ERROR)
- [ ] No sensitive data in logs
- [ ] Logs are structured/parseable
- [ ] Request tracing possible (correlation IDs)

### Documentation
- [ ] README explains purpose and setup
- [ ] Complex logic is documented
- [ ] API/public functions have docstrings
- [ ] Non-obvious decisions are explained
- [ ] Examples included for complex features

---

## Bug Fix Specific Checks

Use this section when reviewing **bug fixes**:

- [ ] The fix actually solves the reported problem
- [ ] Root cause is addressed (not just symptoms)
- [ ] Similar bugs in other places are fixed
- [ ] Fix doesn't introduce regressions
- [ ] Edge cases that caused the bug are now tested
- [ ] Future developers won't make the same mistake
- [ ] Behavior change is documented

---

## New Feature Specific Checks

Use this section when reviewing **new features**:

- [ ] Feature matches specification/requirements
- [ ] API/interface is intuitive and consistent
- [ ] Backward compatibility is maintained
- [ ] New code follows existing conventions
- [ ] Documentation updated (README, API docs)
- [ ] Feature is testable and tested
- [ ] Performance impact assessed

---

## Refactoring Specific Checks

Use this section when reviewing **refactoring**:

- [ ] Behavior is unchanged (no bugs introduced)
- [ ] Code is actually more readable/maintainable
- [ ] Performance is not degraded
- [ ] Tests still pass
- [ ] All usages updated consistently
- [ ] Deprecation path exists if public API changed

---

## Review Completion Checklist

Before submitting your review:

- [ ] All applicable sections above have been checked
- [ ] Severity levels are assigned (MUST/SHOULD/COULD)
- [ ] Line numbers provided for specific issues
- [ ] Positive feedback included (what's good?)
- [ ] Actionable suggestions (not just "make it better")
- [ ] References to style guide (see style-guide.md - Section X)
- [ ] Overall assessment is clear (Approve/Request Changes/Needs Discussion)
- [ ] Tone is constructive and helpful

---

## Quick Reference by Review Type

### Code Quality Audit
1. Code Quality section ✓
2. Architecture & Design section ✓
3. Dependency & Maintenance section ✓
4. Security (input validation only) ✓

### Security Audit
1. Security & Data Handling section ✓✓ (thorough)
2. Testing (security tests) ✓
3. Dependencies (vulnerability scanning) ✓
4. Code Quality (focus on error handling) ✓

### Performance Review
1. Performance section ✓✓ (thorough)
2. Architecture (design efficiency) ✓
3. Testing (performance tests) ✓
4. Dependencies (unnecessary dependencies) ✓

### New Feature Review
1. Architecture & Design section ✓
2. Code Quality section ✓
3. Testing (comprehensive) ✓
4. New Feature Specific Checks section ✓
5. Documentation ✓

### Bug Fix Review
1. Bug Fix Specific Checks section ✓
2. Testing (edge cases that caused bug) ✓
3. Code Quality (could this cause future bugs?) ✓
4. Similar patterns elsewhere? ✓

---

## Notes for Reviewers

1. **Prioritize security** - Security issues trump everything else
2. **Context matters** - What's appropriate for production differs from prototypes
3. **Focus on impact** - High impact issues before low impact nitpicks
4. **Be constructive** - Explain why, provide examples, offer solutions
5. **Acknowledge trade-offs** - Sometimes good-enough is better than perfect
6. **Ask questions** - "Why was this approach chosen?" reveals reasoning

---

## Scoring Guide

If you need to assign an overall score to the code:

**Score 1-2**: Critical issues, do not merge
- Major security vulnerabilities
- Fundamental design flaws
- Missing critical functionality
- Severe performance problems

**Score 3-4**: Significant issues, needs revision
- Multiple important issues
- Poor code quality
- Missing tests
- Potential maintainability problems

**Score 5-6**: Good code, minor issues
- Some code quality improvements suggested
- Minor issues that don't block approval
- Good test coverage
- Solid design

**Score 7-8**: High quality code, polish it
- Well-written, maintainable
- Good test coverage
- Some edge cases to consider
- Minor improvements possible

**Score 9-10**: Exemplary code
- Excellent design
- Comprehensive testing
- Clear documentation
- Best practices throughout

---

**Return to SKILL.md**: Use this checklist during Step 4 of the systematic review workflow.

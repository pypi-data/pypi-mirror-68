# jira power tools

A collection of tools to make it easier to work with the 
[Python Jira API](https://pypi.org/project/jira/).

[![PyPI](https://img.shields.io/pypi/v/jira-power-tools.svg)](https://pypi.org/project/jira-power-tools/) ![Build](https://github.com/dbradf/jira-power-tools/workflows/Test%20Python%20Package/badge.svg)

## Usages

### Lazy Pagination of Jira Issues

If you are querying a lot of jira issues. Paginating the results can lighten the memory usage
on the Jira server. But needing to keep track of the pagination is painful. Using lazy pagination
gives you an iterable that can track pagination for you:

```python
import jirapt

jira = # jira server instance.
jql = "JQL query"

issues = jirapt.search_issues(jira, jql, ...) # you can include any parameters you might pass to search_issues.

for issue in issues:
    # perform work on issue
```

Note: You gather results in parallel by specifying `n_threads=N`. This will gather all the results
before starting iteration. So there will be a delay before the first iteration starts and all the
results will need to fit into memory.

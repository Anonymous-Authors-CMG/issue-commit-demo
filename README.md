# issue-commit-demo

A live demo of **[Issue Commit](https://github.com/Anonymous-Authors-CMG/CMG-Skills)**,
a GitHub Action that reads each new pull request, finds the open issue it
addresses, and suggests a commit message that explains *why*.

This repository is a tiny Python library (`textkit`) with a few real bugs, a
handful of open issues about them (plus some unrelated ones), and pull
requests that fix them. The bot has commented on every PR.

**Go look at the pull requests →** [open PRs](../../pulls)

## The three cases

| PR | What the PR does | What the bot does |
|---|---|---|
| **[#A](../../pulls)** | Fixes a bug. The author forgot to write `Fixes #…`. | Finds the issue among all open ones, shows the evidence, and suggests a message ending in `Fixes #n`. |
| **[#B](../../pulls)** | Refactors code. There is no matching issue. | Says no issue clearly matches, instead of guessing, and writes the message from the diff alone. |
| **[#C](../../pulls)** | Fixes a bug and already says `Fixes #n`. | Skips the search and writes the message from that issue. |

Each PR's comment is posted by `github-actions[bot]`. The full run, including
timing and every step, is under [Actions](../../actions/workflows/issue-commit.yml);
each run's **Summary** tab shows the same result.

## How it's wired

One workflow file, [`.github/workflows/issue-commit.yml`](.github/workflows/issue-commit.yml):

```yaml
on:
  pull_request:
    types: [opened, ready_for_review, reopened]

permissions:
  contents: read
  issues: read
  pull-requests: write

jobs:
  suggest:
    runs-on: ubuntu-latest
    steps:
      - uses: Anonymous-Authors-CMG/CMG-Skills@v1
        with:
          api-key: ${{ secrets.CMG_API_KEY }}
          base-url: ${{ secrets.CMG_BASE_URL }}
          model: ${{ secrets.CMG_MODEL }}
```

and three repository secrets for the model: here, DeepSeek's
`deepseek-flash` at `https://api.deepseek.com`.

To re-run the bot on any PR: Actions → Issue Commit → **Run workflow**, and
enter the PR number.

## What happens in a run

1. Read the PR's title, description and diff through the GitHub API. The PR's
   code is never checked out or run.
2. **Stage 1:** show the model only the *titles* of all open issues, in
   chunks, and keep the likely ones.
3. **Stage 2:** read the full text of the top five and re-rank them.
4. **Check:** ask whether the best one is really addressed by this diff. If it
   can't name a concrete link, report "no match".
5. Write the commit message, then post or update one comment.

Setup guide for your own repository:
[CMG-Skills/docs/ci.md](https://github.com/Anonymous-Authors-CMG/CMG-Skills/blob/main/docs/ci.md).

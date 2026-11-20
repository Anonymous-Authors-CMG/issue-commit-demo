# issue-commit-demo

A live demo of **[Issue Commit](https://github.com/Anonymous-Authors-CMG/CMG-Skills)**,
a GitHub Action that reads each new pull request, finds the open issue it
addresses, and suggests a commit message that explains *why*.

This repository is a tiny Python library (`textkit`) with a few real bugs, a
handful of open issues about them (plus some unrelated ones), and pull
requests that fix them. The bot has commented on every PR.

**Go look at the pull requests →** [open PRs](../../pulls)

## The three cases

The repository has eight open issues: three real bugs and five unrelated
requests that serve as distractors. Each PR below shows one situation.

| PR | What the PR does | What the bot said |
|---|---|---|
| **[#9](../../pull/9)** Sum all units in parse_duration | Fixes [#2](../../issues/2). The description never mentions it. | Found **#2** among the eight, strong match, and suggested a message ending in `Fixes #2`. |
| **[#10](../../pull/10)** Build wrap() lines from word lists | A refactor. No issue asks for it. | **No match.** It rejected [#3](../../issues/3), a feature request for the same `wrap()` function, because the refactor doesn't do what #3 asks. |
| **[#11](../../pull/11)** Count the ellipsis toward truncate width | Fixes [#4](../../issues/4) and says so. | Skipped the search and wrote the message from #4. |

#10 is the interesting one. A search that only matches words would link it to
#3, since both are about `wrap()`. The bot checks each candidate against the
diff before suggesting it, and says "no match" when nothing holds up.

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

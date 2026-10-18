# Repository maintenance

## 1. Make the repository private (owner, one click)

GitHub → **Settings** → **General** → *Danger Zone* → **Change repository visibility** → **Private**.
Or from a terminal with your own login: `gh repo edit juanperez238421-cpu/Manim-Scientific-Visualize --visibility private --accept-visibility-change-consequences`.

What changes when it is private:
- The GIFs in the README and any raw links to `published_renders/` stop working for people who are not collaborators.
- GitHub Actions minutes for private repos count against the account's monthly free quota (2,000 min on the Free plan).
  The daily `cleanup-manim-artifacts.yml` schedule and the one-off render workflows in `.github/workflows/`
  are worth disabling or deleting if they are not needed any more.

## 2. Archive delivery branches as tags

The repository had 259 branches, almost all one-off deliveries (`render/…`, `agent/…`, `manim/…`, `physics9-…`,
`chatgpt/…`, `codex/…`, `trigger/…`, `archive/…`). The plan keeps **only `main`** and turns every other branch into a tag
`archive/<branch name>` pointing at exactly the same commit, then deletes the branch. Nothing is lost: every commit stays
reachable through its tag and can be restored with `git push origin archive/<name>:refs/heads/<name>`.
Open pull requests from those branches are closed by GitHub when the branch disappears.

```bash
git clone https://github.com/juanperez238421-cpu/Manim-Scientific-Visualize.git && cd Manim-Scientific-Visualize
tools/archive_branches_to_tags.sh            # dry run: prints the 258 branch -> tag pairs
tools/archive_branches_to_tags.sh --apply    # push tags, verify each one, then delete the branches
```

The script stops before deleting anything if a single tag is missing. It has to run from your computer: tag pushes and
repository-settings changes are not permitted from the Claude sandbox.

## 3. Size

`main` is about 1.8 GB because earlier renders (MP4, GIF) were committed into history. Archiving branches does not
shrink it; only a history rewrite (`git filter-repo --strip-blobs-bigger-than 20M`) followed by a force push would, and
that changes every commit hash. New renders from `pdf2video` are kept out of git (`build/` is ignored); deliver them as
files or GitHub Release assets instead.

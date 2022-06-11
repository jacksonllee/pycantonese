# Contributing

Thank you for your interest in contributing to the `pycantonese` codebase!

If you would like to add or update a feature in `pycantonese`,
it is recommended that you first file a GitHub issue to discuss your proposed changes
and check their compatibility with the rest of the package before making a pull request.

This page assumes that you have already created a fork of the `pycantonese` repo
under your GitHub account and have the codebase available locally for
development work. If you have followed
[these steps](https://github.com/jacksonllee/pycantonese#setting-up-a-development-environment),
then you are all set.

## Working on a Feature or Bug Fix

The development steps below assume that your local Git repo has a remote
`upstream` link to `jacksonllee/pycantonese`:
   
```bash
git remote add upstream https://github.com/jacksonllee/pycantonese.git
```

After this step (which you only have to do once),
running `git remote -v` should show your local Git repo
has links to both "origin" (pointing to your fork `<your-github-username>/pycantonese`)
and "upstream" (pointing to `jacksonllee/pycantonese`).

To work on a feature or bug fix:

1. Before doing any work, check out the main branch and
   make sure that your local main branch is up-to-date with upstream main:
   
   ```bash
   git checkout main
   git pull upstream main
   ``` 
   
2. Create a new branch. This branch is where you will make commits of your work.
   (As a best practice, never make commits while on a `main` branch.
   Running `git branch` tells you which branch you are on.)
   
   ```bash
   git checkout -b new-branch-name
   ```
   
3. Make as many commits as needed for your work.

4. When you feel your work is ready for a pull request,
   push your branch to your fork.

   ```bash
   git push origin new-branch-name
   ```
   
5. Go to your fork `https://github.com/<your-github-username>/pycantonese` and
   create a pull request off of your branch against the `jacksonllee/pycantonese` repo.

## Running Tests and Code Style Checks

The `pycantonese` repo has continuous integration (CI) turned on,
with autobuilds running pytest
(for the test suite in [`tests/`](tests) and
documentation code examples in [`docs/source/`](docs/source))
as well as `black` and `flake8` for consistent code styling.
If an autobuild at an open pull request fails,
then the errors must be fixed by further commits pushed to the branch
by the author before merging is possible.

Work in progress is more than welcome.
If you aren't sure how to, say, add tests to go with your proposed changes,
please still feel free to create a pull request.
We will guide you to polish up your pull request.

If you would like to help avoid wasting free Internet resources
(every push of new commits to an open pull request triggers new CI builds),
you can run pytest/flake8/black checks locally before pushing commits:

```bash
flake8 src tests
black --check src tests
pytest
```

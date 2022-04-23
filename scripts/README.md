# Test

If new dependencies are added. Remember to run `poetry lock` to regenerate the lock file.

Scripts in this Folder:

| Name | When to Run | Detail |
|------|-------------|--------|
| `pytest-using-docker.sh` | When new tests or codes are added |Run pytest against different Python version: `3.6.15`, `3.7.13`, `3.8.13`, `3.9.12`, `3.10.4`. |
| `build-and-install-using-docker.sh` | Before releasing a new version | Test if pinferencia can be installed properly in different Python version environment: `3.6.15`, `3.7.13`, `3.8.13`, `3.9.12`, `3.10.4`. |
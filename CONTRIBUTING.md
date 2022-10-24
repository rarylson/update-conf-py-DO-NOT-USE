Contributing
============

Contributions are always welcome. Furthermore, we love pull requests. Really!!! :smile:

How can you contribute with this project?
-----------------------------------------

### Bug reports

Report bugs at [update-conf.py - Issues](https://github.com/rarylson/update-conf.py/issues) with the `Bug` flag.

If you are reporting a bug, please include:

- Your environment (operating system and version, python version, etc);
- Any other details about your local setup that might be helpful in troubleshooting;
- The detailed steps to reproduce the bug.

### Bugfixes

You can find known bugs in [README - TODO](README.md#TODO). But someday we may move them to [update-conf.py - Issues (Bug)](https://github.com/rarylson/update-conf.py/labels/bug).

Feel free to contribute solving any of these bugs.

When solving a bug, please add the bug reference in commit message and pull request.

### Propose features

For now, if you want to propose some feature, propose it at [update-conf.py - Issues](https://github.com/rarylson/update-conf.py/issues) with the `Enhancement` flag.

Also please:

- Explain in detail how it would work;
- Keep the scope as narrow as possible, to make it easier to implement.

Of course proposing a feature is welcome. But remember that this is a volunteer-driven project, so code contributions are even more awesome :smile:.

### Implement features

Currently, some proposed features are in [README - TODO](README.md#TODO). But someday we may move them to [update-conf.py - Issues (Enhancement)](https://github.com/rarylson/update-conf.py/labels/enhancement).

Feel free to contribute implementing any of these features.

When implementing a feature, please inform what feature is being implemented in commit message and pull request.

Pull request guidelines
-----------------------

When creating a pull request, please follow these guidelines:

- Fork the project on Github;
- To get the most updated branch, base your changes in the develop branch;
    - You can use the master branch, but you may lost some updates do not merged in the master branch yet;
    - Run:

      ```sh
      git clone git@github.com:YOUR_NAME/update-conf.py.git
      cd update-conf.py
      git checkout -b YOUR-BRANCH origin/develop
      ```

- For bugs and features, it's recomended to install the project in your local environmet inside a virtualenv;
  - The following setup might work at the most situations:

    ```sh
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements-dev.txt
    python setup.py develop
    ```

  - However, if you really need a complete environment, you can run (if you're using Ubuntu):

    ```sh
    make develop-deps-ubuntu
    make install-develop
    ```

- If your pull request solves a bug, please include the necessary unit tests that reproduces the bug (and that passes after the fix);
- If your pull request adds a feature, please include the necessary unit tests;
- Add any necessary docstrings and comments to the code;
- Verify if your code passes in the checks and tests:

  ```sh
  make check
  make test  # or 'sudo make test' to run all tests
  ```

- Push your changes:

  ```sh
  git push --set-upstream origin YOUR-BRANCH
  ```

- Make a pull request comparing your new branch with the project develop branch;
- Verify if your code works for all supported Python versions;
    - You can check [update-conf.py - GitHub Actions](https://github.com/rarylson/update-conf.py/actions/workflows/tests.yml) for troubleshooting if necessary.

If you follow all the previous guidelines, you're really an angel :angel: :+1:!

But if you can't follow all of them, DO NOT WORRY! Just submit your contribution! :smiley:

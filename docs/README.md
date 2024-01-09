# backend-di--python-lib-template 
Python repository template to easily publish a new library in Artifactory.

## 🤔 How to use this template
### 🔄 Replacements
- Search for all occurrences of `backend-di--python-lib-template` (REPO_TEMPLATE_NAME) and replace it with the name of your repository.
- Search for all occurrences -including folders- of `pylibtemplate` (LIBRARY_NAME) and replace it with the name of your library.

### 🏁 Base tag
- Create a base tag in your repository. This tag will be used to create the first version of your library.
```
git tag -m "1.0.0" 1.0.0
```
Above command can be executed on the IDE terminal while working over your first feature branch.

### 👨‍💻👩‍💻 Code guidelines
- [x] 😊 Must be basic and simple. Consider this as strictly tied to solve a specific problem.
- [x] 😎 Must follow SOLID principles (whatever you can).
- [x] 🧪 Must be tested (partially).
- [x] 👀 Keep an eye on the amount of library dependencies by trying to avoid creating a big monorepo.

### 🦾 Versioning
- Library versioning will look like this: `MAJOR.MINOR.PATCH - <Pokemon Name>`. E.g.
```
1.0.0 - Mercurial Butterfree
```

### 📦 Package
- Package name will look like this: `<LIBRARY_NAME>-<VERSION>-py3-none-any.whl`. E.g.
```
pylibtemplate-1.0.0-py3-none-any.whl
```

### ❌ Delete this section
- Once finished with the initial library configuration, delete this `How to use this template` section. 

## 💻 Installation
### 💊 Dependencies
- `python` >= 3.8
- Jfrog Artifactory access token.

### ⚙️ Configure pip
It is recommended to use a virtual environment so as not to modify the pip behavior of the system.

This sentence adds the artifactory repository as your `pip` default url.

```
pip config set global.extra-index-url "https://<your-email>:<artifactory-token>@artifactory.mpi-internal.com/artifactory/api/pypi/pypi-virtual/simple"
```

> If you use `poetry` you can add the artifact repository following the standard `poetry` steps.

### 🔗 Install

#### Latest version available

```
pip install <PYTHON_LIBRARY_NAME>
```
#### Specific version
This is based on Github tags. You can check the available versions [here](https://github.mpi-internal.com/scmspain/backend-di--python-lib-template/tags).

Example for version 1.0.10
```
pip install <PYTHON_LIBRARY_NAME>==1.0.10
```

## Support and Questions

You can send your questions and suggestions to [The Team](mailto:your_team_email@companyname.com).
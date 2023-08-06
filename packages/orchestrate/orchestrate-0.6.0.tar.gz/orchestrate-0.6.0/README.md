# Orchestrate

## Requirements
SigOpt Orchestrate has been tested on clusters running Kubernetes 1.10, 1.11, and 1.12.

## Installation
_For development instructions, refer to [installation for development](#installation-for-development) instead._

Install [docker](https://www.docker.com/).

```bash
git clone git@github.com:sigopt/orchestrate.git
cd orchestrate
pip install .
sigopt test
```

## Help

To get the most up-to-date information about available commands, run
```bash
sigopt -h
```

Similarly, for usage about a particular command, run
```bash
sigopt logs -h
```

## Manage kubernetes clusters

### Create a cluster

To create an example cluster, first we can clone `sigopt-examples`  into a separate directory (not in orchestrate).

```bash
git clone https://github.com/sigopt/sigopt-examples
cd sigopt-examples
sigopt cluster create -f orchestrate/clusters/tiny_cluster.yml
```

*Note: Creating a cluster with GPU support requires that you accept the
end user license agreement (EULA) for the EKS-optimized AMI with GPU support.
This can be done [here](https://aws.amazon.com/marketplace/pp/B07GRHFXGM)
by subscribing to the AMI.*

Once the above command succeeds, you should be able to get more information about your cluster's nodes using `kubectl` commands.

```bash
sigopt kubectl get nodes
sigopt kubectl describe nodes
```

For further information and debugging your nodes, consult the [kubectl documentation](https://kubernetes.io/docs/reference/kubectl/overview/).

### Destroy a cluster

```bash
sigopt cluster destroy --cluster-name orchestrate
```

## Run Example Experiment

We can also run an example experiment from the `sigopt-examples` repository.

```bash
cd orchestrate/sgd_classifier
sigopt run
```

You can also run experiments from other directories. From `sigopt-examples` directory:
```bash
sigopt run --directory orchestrate/sgd_classifier/ -f orchestrate/sgd_classifier/orchestrate.yml
```

## Connect to someone else's cluster
Every cluster creates an access role, `<cluster_name>-k8s-access-role`.

If you created the cluster, you already have access to role. To grant team member permission to access the cluster, use the [AWS IAM console](https://console.aws.amazon.com/iam/home#/roles) to add their IAM User as a "trusted entity" to access this role.

Once a user has the correct permission to assume the IAM role they can configure orchestrate to use your cluster:

```
sigopt cluster connect --cluster-name <cluster name>
```

## Installation for Development
Install [docker](https://www.docker.com/).

Build the base docker images by following the [README](docker/).

Clone the repo:
```bash
git clone git@github.com:sigopt/orchestrate.git
cd orchestrate
```

Create a virtual environment:
```
pip install virtualenv
virtualenv -p `which python3.6` venv
```

Activate the virtual environment:
```
source venv/bin/activate
```

Install development and production dependencies:
```
make update
```

### Option #1: install the orchestrate package locally
Install the orchestrate cli and python package into your local virtualenv. Please note that changes you make while you are developing will require you to re-install the package to see the changes reflected:

```
pip install .
```

Now you can run commands as above, like

```
sigopt -h
```
### Option #2: run orchestrate directly

Invoke the orchestrate CLI directly, without installing package, by using the bin script from this repository:
```
./bin/sigopt -h
```

## Pointing at development APIs

You can set the `SIGOPT_API_URL` environment variable to point at a different SigOpt API
rather than `https://api.sigopt.com`. This is useful when operating behind a proxy or in development.
Be aware that `SIGOPT_API_URL` must be reachable both locally and within the Orchestrate docker images.
That means that `localhost` will not work as expected, since `localhost` within the container is different
from `localhost` outside.

To get around this on OSX, you can use `host.docker.internal` instead of `localhost` when using `run-local`.
You will need to add `127.0.0.1 host.docker.internal` as a line in your /etc/hosts, which will
ensure that both inside the containers and outside, `host.docker.internal` refers to 127.0.0.1 on
the host machine.

```bash
SIGOPT_API_URL=http://host.docker.internal:5000 sigopt run-local -f orchestrate.yml
```

# Linting

We use linting to achieve coding style and consistency.
Linting runs in our test infrastructure on CircleCI.
If you have lint errors your test suite will not pass and you will not be able to merge your changes.
We installed a pre-commit hook as part of the make setup command so all your changed files will run pylint before a commit is made as well.

Lint all python code:
```bash
make lint
```
# Testing

## Unit Tests

Unit Tests can be run with:
```bash
make pytest
```
## System Tests

System tests can be run locally against a test cluster as well as in CircleCI.
You need AWS setup and the requisite permissions to create a cluster to run tests locally.
Alternatively, a small subset of the tests can be run without access to a cluster, see [Example #3](#testexample3) in Run System Tests.

### Setup Cluster for System Tests
`[cluster-name]` must match the regex: `/^[a-zA-Z][-a-zA-Z0-9]*$/`

```bash
ci/setup.sh [cluster-name]
sigopt cluster create -f ci/artifacts/cpu_test_cluster.yml
```

If you have the correct permissions to launch GPU instances in AWS and want to run all the tests
you can use the gpu_test_cluster.yml for creating the cluster to run.

### Run System Tests
Before running tests make sure that `which sigopt` points to the version of orchestrate you want to test.

Once you have a cluster up and running you can run system tests with:
```bash
ci/run_system_tests.sh [cluster-name] (optional)[Comma separated list of: (helper, local, cluster, cpu, gpu, wait, clean)]
```

Example 1: Run all tests except ones that require a gpu against a test cluster named: `testing-cluster`
```bash
ci/run_system_tests.sh testing-cluster helper,local,cluster,cpu,wait,clean
```
Example 2: Run all tests against a cluster named: `includes-gpu-node-cluster`
```
ci/run_system_tests.sh includes-gpu-node-cluster
```
<a name="testexample3"></a>Example 3: Run tests that don't require access to a cluster
```bash
ci/run_system_tests.sh placeholder helper,local
```

### Cleanup
Your test cluster can be deleted with:
```bash
sigopt cluster destroy -n [cluster-name]
```

# Releasing

## Release new Python Client

This is our current release process for the Python client:
* Use `bump-version` script to create a release branch
* Open a PR on the release branch
* Run system tests on release branch
* Release new Python client from release branch using the `publish` script
* Squash and merge release branch into master

### Release Branch
First, to create the release branch, run the `bump-version` script off of master. This script will create a new branch, update the python client version, and push the branch to GitHub:

```bash
git checkout master
git pull origin master
./bump-version <new-version>
```

### Pull Request
Next, open a PR on the new branch. **Write a comment listing out major changes since the last release**, even if the changes are simply a rehash of previous Docker build changes.

### System Tests
Every release should be tested via system tests. System tests are run through CircleCI.

We generally use [GitHub labels](https://github.com/sigopt/orchestrate/issues/labels) to keep track of system tests for ourselves, and for our coworkers, to avoid the question "did you run system tests?", or "did you know that you need to run system tests?".
* Use `system tests required` to indicate that you will run system tests on this branch
* Use `system tests passed` to indicate that you have successfully completed system tests on the most up to date version of this branch.

System tests are scheduled to be run automatically on CircleCI.
To manually trigger system tests for a branch:

1. Get your CircleCI API Token from https://circleci.com/account/api
2. Run the following:

```bash
curl \
  -u ${CIRCLECI_TOKEN}: \
  -X POST \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  -d '{"branch": "YOUR_BRANCH_NAME", "parameters":{"run_system_tests":true}}' \
  https://circleci.com/api/v2/project/gh/sigopt/orchestrate/pipeline
```

**Caveats**
 * System tests supercede our normal integration tests, so it's best to cancel the integration tests on the release branch right away
 (otherwise, CircleCI may experience errors launch two sets of tests on the same branch).
 * Never delete the system test on master

### Publish

From the release branch, run the `publish` script to create the appropriate files, and upload them to pypi. You must have pypi credentials to run this script:
```
./publish <new-version>
```

### Cleanup

Squash and merge the release branch into master.

## Publish Docker Images

Publishing new Docker images should be done from a `docker-X.Y.Z` branch using `./scripts/trigger_dockerbuild`.
**Update `DOCKER_IMAGE_VERSION = 'X.Y.Z'` in `orchestrate/version.py` before doing this!**

## License

Licensed under [Apache 2.0](LICENSE.md).

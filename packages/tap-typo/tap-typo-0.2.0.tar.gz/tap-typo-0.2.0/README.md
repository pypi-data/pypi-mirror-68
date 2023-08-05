# tap-typo

[Singer](https://singer.io) tap that extracts data from the [Typo](https://www.typo.ai?utm_source=github&utm_medium=tap-typo) platform. The tap produces JSON-formatted data output
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

- [Usage](#usage)
  - [Installation](#installation)
  - [Create a configuration file](#create-a-configuration-file)
  - [Discovery mode](#discovery-mode)
  - [Sync mode](#sync-mode)
  - [Saving state and resuming](#saving-state-and-resuming)
    - [Saving state messages](#saving-state-messages)
    - [Creating a State file](#creating-a-state-file)
    - [Resuming with a State file](#resuming-with-a-state-file)
  - [Catalog file](#catalog-file)
- [Typo registration and setup](#typo-registration-and-setup)
- [Development](#development)
- [Support](#support)



## Usage

This section describes the basic usage of **tap-typo** through an example data extraction from a Typo dataset. It assumes that you already have a Typo account, with an existing repository and a dataset. If you do not meet these prerequisites, please go to [Typo Registration and Setup](#typo-registration-and-setup).



### Installation

Python 3 is required. It is recommended to create a separate virtual environment for each tap or target as their may be incompatibilities between dependency versions.

```bash
> pip install tap-typo
```



### Create a configuration file

The config file (usually config.json) is a JSON file describing the tap's settings.

The following sample configuration can be used as a starting point:


```json
{
  "api_key": "my_apikey",
  "api_secret": "my_apisecret",
  "cluster_api_endpoint": "https://cluster.typo.ai/management/api/v1",
  "repository": "my_repository",
  "dataset": "my_dataset",
  "audit_id": "audit_id",
  "output_rfc3339_datetime": false
}
```

**Please note: the `dataset` and `audit_id` parameters are optional. When not specified the tap-typo will automatically run in sync mode using the selected datasets from the catalog.**

- **api_key**, **api_secret** and **cluster_api_endpoint** can be obtained by logging into the [Typo Console](https://console.typo.ai/?utm_source=github&utm_medium=tap-typo), clicking on your username, and then on **My Account**.
- **repository** and **dataset** correspond to their respective names and **audit_id** is optional and should be only provided when syncing data from an audit.
- Additionally, a **records_per_page** parameter can be provided to override the number of records requested at once, and a **record_limit** parameter can indicate the maximum number of records that will be obtained when the tap is executed.



### Discovery mode

In discovery mode, **tap-typo** will infer the Singer Catalog from the config file and data in Typo. The output can be redirected to a file in order to be modified and used as input to **tap-typo** (see [Catalog file section](#catalog-file)).

```bash
> tap-typo -c config.json -d > catalog.json
```



### Sync mode

Sync mode will fetch data from Typo and output to stdout. Each record has two additional fields: `__typo_result`, that can have a value of `Error` or `OK` and `__typo_record_id`, which indicates the record's internal ID in Typo. Before starting the sync, unless a custom Catalog file is provided, Typo will run discovery and build the catalog.


```bash
> tap-typo -c config.json
```



### Saving state and resuming

#### Saving state messages

When **tap-typo** runs in Sync mode it will emit one [STATE message](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md#state-message) for every RECORD message emitted.  STATE messages contain a value JSON property with the state information.

A Singer target should output the contents of the value JSON property in a STATE message.  By redirecting this target output to a file, the value property of each STATE message will be stored per line.

```bash
> tap-typo -c config.json | target-google-bigquery > state-history.txt
```



#### Creating a State file

To resume from a failed or terminated transfer, you will need create a STATE file from the last line in the redirected output (state-history.txt in our example).  Below is an example command that performs the step to create a STATE file, state.json, from state-history.txt.  You may edit this STATE file as necessary. The STATE file can be used as input to **tap-typo** to resume.

```bash
tail -n 1 state-history.txt > state.json
```

Example STATE file:

```json
{
	"bookmarks": {
		"tap-typo-repository-repo1-dataset-dataset1": {
			"__typo_record_id": 26
		}
	}
}
```



#### Resuming with a State file

To resume by providing a State file, **tap-typo** can be started with a -s parameter and providing a path to a STATE file. **tap-typo** searches the bookmarks property for a key that matches the stream name.  If found, **tap-typo** will try to resume from the location defined in the bookmark.

```bash
> tap-typo -c config.json -s state.json | target-google-bigquery > state-history.txt
```



### Catalog file

A catalog file can be provided by adding the --catalog parameter with a file path. This will prevent the discovery process and use the catalog provided in the file path.

```bash
> tap-typo -c config.json --catalog catalog.json | target-google-bigquery > state-history.txt
```



## Typo registration and setup

In order to create a Typo account, visit [https://www.typo.ai/signup](https://www.typo.ai/signup?utm_source=github&utm_medium=tap-typo) and follow the instructions.

Once registered you can log in to the Typo Console ([https://console.typo.ai/](https://console.typo.ai/?utm_source=github&utm_medium=tap-typo)) and go to the Repositories section to create a new Repository.

Next, you can start uploading data by using [target-typo](https://github.com/typo-ai/target-typo). A new dataset will be created automatically when data is submitted.



## Development

To work on development of tap-typo, clone the repository, create and activate a new virtual environment, go into the cloned folder and install tap-typo in editable mode.

```bash
git clone https://github.com/typo-ai/tap-typo.git
cd tap-typo
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```



## Support

You may reach Typo Support at the email address support@ followed by the typo domain or see the full contact information at [https://www.typo.ai](https://www.typo.ai?utm_source=github&utm_medium=tap-typo).



---

Copyright &copy; 2020 Stitch

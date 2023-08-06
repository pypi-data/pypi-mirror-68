# CLI for delairstack

# `delairstack`

**Usage**:

```console
$ delairstack [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell (shell must be restarted after installing it in order to use it).
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `analytics`: Interact with Analytics
* `configure`: Configure your credentials to connect to the...
* `products`: Interact with Products

## `delairstack configure`

Configure your credentials to connect to the platform 

**Usage**:

```console
$ delairstack configure [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `delairstack analytics`

Interact with Analytics

**Usage**:

```console
$ delairstack analytics [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new analytic
* `delete`: Delete an analytic
* `list`: List the analytics

### `delairstack analytics create`

Create a new analytic 

**Usage**:

```console
$ delairstack analytics create [OPTIONS]
```

**Options**:

* `--description PATH`: Path of the Analytic description (YAML file)  [required]
* `--company TEXT`: Company identifier
* `--help`: Show this message and exit.

### `delairstack analytics delete`

Delete an analytic 

**Usage**:

```console
$ delairstack analytics delete [OPTIONS] ANALYTIC_NAME
```

**Options**:

* `--help`: Show this message and exit.

### `delairstack analytics list`

List the analytics 

**Usage**:

```console
$ delairstack analytics list [OPTIONS]
```

**Options**:

* `--limit INTEGER`: Max number of analytics returned
* `--help`: Show this message and exit.

## `delairstack products`

Interact with Products

**Usage**:

```console
$ delairstack products [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cancel`: Cancel a running product
* `list`: List the products
* `logs`: Retrieve the logs of a product

### `delairstack products cancel`

Cancel a running product 

**Usage**:

```console
$ delairstack products cancel [OPTIONS] PRODUCT_ID
```

**Options**:

* `--help`: Show this message and exit.

### `delairstack products list`

List the products 

**Usage**:

```console
$ delairstack products list [OPTIONS]
```

**Options**:

* `-n, --limit INTEGER`: Max number of analytics returned  [default: 10]
* `--analytic TEXT`: Analytic name
* `--company TEXT`: Company identifier
* `--status [pending|processing|available|rejected|failed]`: Product status
* `--all`: If set, display also the products from internal analytics (otherwise only products from external analytics are displayed).
* `--help`: Show this message and exit.

### `delairstack products logs`

Retrieve the logs of a product 

**Usage**:

```console
$ delairstack products logs [OPTIONS] PRODUCT_ID
```

**Options**:

* `-f, --follow`: Follow logs
* `--help`: Show this message and exit.

---

*Generated with `typer delairstack_cli/main.py utils docs --name delairstack`*
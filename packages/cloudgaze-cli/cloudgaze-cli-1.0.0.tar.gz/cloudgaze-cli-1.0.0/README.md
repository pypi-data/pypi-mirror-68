# cloudgaze-cli

CLI (command line interface) to call the Cloudgaze API to transform your AWS cloudformation template specifications to draw.io compatible xml files.

This command line application makes a network call in the background to convert the template file. No data is stored on the remote endpoint, and you need to be connected to the internet to use this tool. The communication is encrypted using TLS.

## Install
`pip install cloudgaze-cli`

## Usage
```bash
$ cloudgaze --help
Usage: cloudgaze [OPTIONS] TEMPLATE_FILE OUTPUT_FILE

Options:
  --help  Show this message and exit.
```

```bash
$ cloudgaze ./path/to/template.yml ./path/to/output.xml
results written to '/abs/path/to/output.xml'
```
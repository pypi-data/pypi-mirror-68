## Changelog

### 2.2.1 - 2020-05-15

*   [relvalconsumer-2.2.1.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-2.2.1.tar.gz)

1.  Require python-wikitcms 2.6.0

### 2.2.0 - 2020-05-15

*   [relvalconsumer-2.2.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-2.2.0.tar.gz)

1.  AMI consumer: bail if no compose ID found
2.  Adjust to wikitcms change from `modular` to `dist`, enable IoT event creation
3.  Modernize project layout and infrastructure, use black, pep517 etc.

### 2.1.0 - 2019-11-13

*   [relvalconsumer-2.1.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-2.1.0.tar.gz)

1.  Add `RelvalAMIConsumer` for updating AMI pages

### 2.0.1 - 2019-09-19

*   [relvalconsumer-2.0.1.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-2.0.1.tar.gz)

1.  Support submitting bugs for over-size images via `relval size-check`

### 2.0.0 - 2019-06-18

*   [relvalconsumer-2.0.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-2.0.0.tar.gz)

1.  Handle fedfind `UnsupportedComposeError`
2.  Port to fedora-messaging, drop Python 2 compatibility

### 1.3.1 - 2018-02-22

*   [relvalconsumer-1.3.1.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-1.3.1.tar.gz)

1.  Go back to triggering on Pungi messages (not PDC) - requires wikitcms >= 2.3.0
2.  Clean up and enhance the tests somewhat

### 1.3.0 - 2018-02-13

*   [relvalconsumer-1.3.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-1.3.0.tar.gz)

1.  Run image size checks (via relval) for newly-created events

### 1.2.0 - 2017-12-22

*   [relvalconsumer-1.2.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-1.2.0.tar.gz)

1.  Stop creating Modular events
2.  Switch back to `hawkey` (from `rpm`) for RPM version comparison

### 1.1.0 - 2017-11-10

*   [relvalconsumer-1.1.0.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-1.1.0.tar.gz)

1.  Create events for Fedora-Modular 27 composes

### 1.0.1 - 2017-02-17

*   [relvalconsumer-1.0.1.tar.gz](https://files.pythonhosted.org/packages/source/a/relvalconsumer/relvalconsumer-1.0.1.tar.gz)

1.  First real release

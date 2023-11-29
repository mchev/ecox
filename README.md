# ecox

## Overview

The Traceability addon enhances the functionality of the Odoo Inventory app by introducing a new Traceability menu. This menu provides valuable insights into the traceability of products and components within your inventory.

## Features

### Traceability Menu

The addon adds a new Traceability menu within the Odoo Inventory app, providing users with a centralized hub for accessing traceability-related features.

### Sub-Elements

1. Serial by Component
2. Product by Component

## Usage

Navigate to the Traceability menu within the Odoo Inventory app.

Choose between the Serial by Component and Product by Component sub-menus to access detailed traceability information.

Search for a component.


## Hack Script to unfold elements

> Open the browser console, paste the code and hit enter.

```js
 $(".o_stock_reports_unfoldable").each(function () {
        var $unfoldable = $(this);
        $unfoldable.click();
    });
```

## Dev

Run Odoo with the custom conf and upgrade the ecox pagkage.

```bash
python3 odoo-bin -c odoo.conf -u ecox
```

./odoo.conf

```
[options]
db_host = localhost
db_port = 5432
db_user = odoo
db_password = ""
addons_path = addons,dev
```

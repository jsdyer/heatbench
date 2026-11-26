# Heat Bench

Compare oil, natural gas, propane, electric-resistance and heat-pump operating scenarios from actual annual consumption. A local calculator, with no API key or scheduled collector.

<!-- coolcode:guide -->
Start with a complete year of bills and separate space heating from hot water, cooking and other electricity use. Enter your own marginal prices, equipment efficiency, seasonal COP range and backup share. Results show delivered heat, annual costs, savings ranges and simple payback. Initial values are clearly labelled examples, not current utility tariffs. Scenarios are saved only when requested, in this browser; CSV exports preserve the assumptions. This tool does not size heating equipment or establish rebate eligibility.
<!-- /coolcode:guide -->

## Method and limits

NRCan's [Air-source Heat Pump Sizing and Selection Guide, Table 8](https://publications.gc.ca/collections/collection_2021/rncan-nrcan/M154-138-2020-eng.pdf) supplies higher-heating-value factors: oil 10.61 kWh/L, natural gas 10.36 kWh/m³, propane 7.03 kWh/L. Delivered heat equals recorded use × factor × heating share × efficiency × weather adjustment. Heat-pump electricity is its allocated heat share divided by seasonal COP; backup costs and additional annual maintenance are added. Both ends of the COP range are calculated.

COP is a seasonal assumption, not an instantaneous mild-weather rating. [NRCan explains the distinction and climate sensitivity](https://natural-resources.canada.ca/energy-efficiency/energy-star/heating-cooling-heat-pump). Fixed charges, financing, cooling, fuel-price escalation, replacement cycles and equipment life are excluded. Simple payback may not occur and is not a forecast. Electricity from a whole-home bill must not all be treated as heating.

## Expand or customize

Edit `config/defaults.json` for documented starting assumptions and source references. Keep `fuelKwh` consistent with the reviewed constants in `web/model.mjs` if changing supported fuels. The builder copies the default settings into the site. Visitors can enter values beyond all defaults, label and save any number of scenarios, load them again and export CSV. No account or remote database is used.

## Develop and publish

Run `node --test tests/*.test.mjs`, `python3 -m unittest discover -s tests -v`, `python3 scripts/build.py`. Preview `dist/` with a local HTTP server. The Pages workflow tests desktop/mobile interaction and publishes successful main builds. Set GitHub Pages source to GitHub Actions. No secrets, Cloudflare API handler, watchdog target or refresh guard is needed; the standard CoolCode visit counter uses the `heatbench` ID.

Inputs do not leave the browser. Explicitly saved scenarios use `coolcode:heatbench:scenarios:v1`; clearing site storage removes them. The standard visit counter never receives scenario values. Reference factors reviewed 2026-11-26 UTC.

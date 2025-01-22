# Karrio 2024.12.rc12

## Changes

### Feat

- feat: add `currency` to SEKO connection config

### Fix

- fix: `ups` delivery confirmation data mapping (#749)

# Karrio 2024.12.rc11

## Changes

### Fix

- fix: seko package description truncation

# Karrio 2024.12.rc10

## Changes

### Fix

- fix: seko tracking event parsing

# Karrio 2024.12.rc9

## Changes

### Feat

- feat: fix wording in webhooks test modal
- feat: make seko event Omnicode take precedence over default Code
- feat: add `REDIS_PREFIX` for redis prefix configuration
- feat: add more testing data sample for webhook testing

### Fix

- fix: docker entrypoints with proper DETACHED_WORKER flag check
- fix: easyship simple tracking support

### Chore

- chore: add new carrier logos

### Docs

- docs: `REDIS_PREFIX` env documentation

# Karrio 2024.12rc8

## Changes

### Feat

- feat: Add minimal webhook back off retries

### Fix

- fix: seko tracking event ordering

# Karrio 2024.12rc7

## Changes

### Feat

- feat: clean up `SEKO` shipment meta to collecte delegated Carrier details

### Fix

- fix: document generator invalid closing statement


# Karrio 2024.12rc6

## Changes

### Fix

- fix: `seko` tracking event date parsing
- fix: karrio image default user set up

# Karrio 2024.12rc5

## Changes

### Fix

- hotfix: `ups` delivery confirmation data mapping
- hotfix: regression on document generation caused by invalid html.close on weasyprint

# Karrio 2024.12rc4

## Changes

### Feat

- feat: add missing shipping options mapping for `ups` carrier
- feat: add support for `usps*` https://developer-cat.usps.com/ API

# Karrio 2024.12rc3

## Changes

### Feat

- feat: improve document generation by closing pdf writer
- feat: ensure shipping date for `sapient` is set to UTC before applying next_business_day calculation
- feat: Add new shadcn components for karrio UI kit

### Fix

- fix: oauth login error message parsing

# Karrio 2024.12rc2

## Changes

### Feat

- feat: replace treepoem/ghostscript by zint/pyzint for barcode generation

### Chore

- chore: update Dockerfiles metadata
- chore: update Dockerfiles away from deprecated env vars declaration
- chore: handle oss install with dockerless

### Fix

- fix: dashboard runtime environment variables issues

# Karrio 2024.12rc1

## Changes

### Feat

- feat(WIP): introduce new customizable dashboard with a new stack shacdn|tailwind|radix|tanstack
- feat: Introduce advanced Karrio CLI features with API connectivity and data query
- feat: make rate limit configurable using env vars (#589)

### Fix

- fix:`usps` API proxy and payment authentication (#709)
- fix: version freeze git reference for `dockerless` install (#721)
- fix: invalid reference useSystemConnection causing permission error (#706)
- fix: Consolidate`fedex` duties payor definition with missing account number with live tests (#718, #697)
- fix: issue with `shipping_date` and `shipment_date` being set to None and options getting overridden

# Karrio 2024.9.15

## Changes

### Fix

- fix: `fedex` payor info data mapping #718
- fix: easyship required defaults and max contact name size


# Karrio 2024.9.14

## Changes

### Feat

- feat: switch export line item description to description (`dhl express`) @DarkSwoop

# Karrio 2024.9.13

## Changes

### Feat

- feat: use actual city as fallback value for seko shipment state addresses

### Fix

- fix: fedex payment account numbers assignments

### Chore

- deps: add back pycairo as optional dependency on macos

# Karrio 2024.9.12

## Fix

- fix: missing dependencies in the build process

# Karrio 2024.9.11

## Changes

### Feat

- feat: consolidate SEKO printlabel for EU shipments
- feat: skip customs declaration for sapient when not international shipment
- feat: add DAP incoterms
- feat: make start-server script port configurable through env var

### Chore

- deps: add pycairo as dependency for document generation Macos compatibility

# Karrio 2024.9.10

## Changes

### Feat

- feat: add support for additional seko_reference_*
- feat: add rate_provider mapping to sapient integration and refactor sapient_carrier_code references to avoid clash with carrier_code reserved field
- feat: Introduce document template options field for pre-rendering optimization

### Fix

- fix: shipment parsing when label generation fails but shipment creation succeeds

# Karrio 2024.9.9

## Changes

### Fix

- hotfix: `ups` rate service charge parsing regression

# Karrio 2024.9.8

## Changes

### Fix

- fix: `ups` product origin country code mapping
- fix: `ups` `ups_worldwide_express` product code mapping

# Karrio 2024.9.7

## Changes

### Feat

- feat: Add `system_usage` to base `graphql` types

### Chore

- remove deprecated `karrio.server.admin` module from OSS build

# Karrio 2024.9.6

## Changes

### Fix

- fix: `ups` EU rate code parsing using context origin

# Karrio 2024.9.5

## Changes

### Feat

- feat: Add `Duplicate Shipment` action to shipment menu (#680)

### Fix

- fix: `ups` TotalCharge parsing for `negotiated_rates` (#703)

# Karrio 2024.9.4

## Changes

### Feat

- feat: Add `service_level` to `sapient` carrier connection settings

# Karrio 2024.9.3

## Changes

### Feat

- feat: Add fallback values for `easyship` rate request `parcels.items`

# Karrio 2024.9.2

## Changes

### Fix

- fix: `ups` TotalCharge parsing for `negotiated_rates`

# Karrio 2024.9.1

## Changes

### Chore

- remove `strawberry-graphql-django` dependency as it is not fully integrate for the value it is supposed to provide

# Karrio 2024.9

## Changes

### Feat

- feat: Easyship integration (#569)
- feat: Add `pickup` support for `fedex` JSON API integration (#690)
- feat: introduce `shipping_date` field of `datetime` type and deprecate `shipment_date` of `date` type to capture time for carriers that expect full future `datetime` ship date values.
- feat: Add dhl_express content description for insurance (#694)

### Fix

- fix: `eshipper` carrier and services mapping (#675)
- fix: `canadapost` non-uniq shipment group_id across account (#679)
- fix: `fedex_ws` pickup request encoding (#690)
- fix: organization GraphQL queries running on OSS build (#687)
- fix: Nextjs cache build issue (#688)

# Patch 2024.6.7

## Changes

### Fix

- hotfix: `canadapost` group_id invalid string format #686


# Patch 2024.6.6

## Changes

### Fix

- fix: `canadapost` shipment identifier data mapping (#683)

# Patch 2024.6.5

## Changes

### Devx

-   devx: improve karrio docker container startup with healthchecks #684

# Patch 2024.6.4

## Changes

### Feature

- feat: Add field to unified class for future support of message level

### Chore

- chore: Add tests for `UPS` EU rates parsing
- chore: make ups upper case for uniform charges details
- chore: use localhost address for default `NEXT_PUBLIC_KARRIO_PUBLIC_URL` during build

### Refactor

- refactor: #673

# Patch 2024.6.3

## Changes

### Feat

-   feat: bootstrap `seko` carrier extension
-   feat: prepare `seko` requests schemas
-   feat: test drive `seko` request mapper implementation
-   feat: compute next business `datetime` for sapient shipment_date

# Patch 2024.6.2

## Changes

### Fix

-   [Fixes](https://github.com/karrioapi/karrio/commit/4f26746ec34fd0bb41a6cef08def822eb21f3391) https://github.com/karrioapi/karrio/issues/667[: UPS ReferenceNumber changes](https://github.com/karrioapi/karrio/commit/4f26746ec34fd0bb41a6cef08def822eb21f3391)

Special thanks to @mazzarito

# Patch 2024.6.1

## Changes

### Feat

-[feat: Add GraphQL queries and typings for apps](https://github.com/karrioapi/karrio/pull/656/commits/551c73dbfa5feb5c3f47cb49736ecb57f3460d6b)

### Refactor

-   refactor: dashboard extracting non-routing code and dependencies to `@karrio/core` package
-   [refactor: dashboard from Nextjs page router to app router](https://github.com/karrioapi/karrio/pull/656/commits/8d0e2feec8c284b7f5bb577ea0b0a50b727001c2)

### Chore

-   [chore: deprecate apps module from OSS build](https://github.com/karrioapi/karrio/pull/656/commits/e115dddee06d498d5ad5a6de0b21094e528dfc53)
-   [chore: introduce CHANGELOG.md](https://github.com/karrioapi/karrio/commit/df9a232d7df0e9fdbb89b915a9ef546637d60dd1)

# Karrio OSS 2024.6

> [!IMPORTANT]
> Thank you for your patience as I go through a time of workload adjustment between my new role and the maintenance of Karrio. [Read my community announcement here](https://github.com/orgs/karrioapi/discussions/585)

### Feat

-   refactor: dashboard extracting non-routing code and dependencies to `@karrio/core` package
-   [refactor: dashboard from Nextjs page router to app router](https://github.com/karrioapi/karrio/pull/656/commits/8d0e2feec8c284b7f5bb577ea0b0a50b727001c2)
-   [feat: apply utc timezone to sapient integration ship date](https://github.com/karrioapi/karrio/commit/06e378d6eada14f10c91138078caad4d9f122e25)
-   [feat: add support for FedEx scan events multi-datetime formats](https://github.com/karrioapi/karrio/pull/655/commits/2039e5d51523f368dbbee1b0d8e631eed2b1b347)
-   [feat: handle shipment_date update when passed upstream instead of per extension implementations](https://github.com/karrioapi/karrio/pull/655/commits/0d73add6247ed558b3068f817bcdda173d0d11c8)
-   feat: add `karrio.lib` to document template context
-   feat: Disable "note" alert types as previously done in `fedex_ws` #638
-   feat: rename legacy USPS extensions to `usps_wt` (for USPS Web Tools)
-   feat: Carrier Connection REST API #582
-   reat: [carrier-integration | interoperability] SAPIENT #633
-   feat: FedEx Tracking should be giving us the `signed_by` #635
-   feat: USPS REST API integration
-   feat: Handle defaulting size units to LB/IN for UPS US rates and shipment requests
-   feat: add a description field to parcel forms
-   feat: add missing per package description data mapping to `ups` extension
-   feat: cherry-pick `hay_post` integration
-   feat: Finalize `eShipper` new API integration
-   feat: add back FedEx tracking POD image
-   feat: add workspace config for automatically applying insurance to full package value
-   feat: add support for metadata link rendering
-   feat: Add standardized flag for all supported carriers
-   feat: expose return_address to GraphQL and API specs and generated clients
-   feat: Add return address to create label forms across the dashboard
-   Introduce the `return_address` field
-   feat: Add Django admin editor for document templates
-   feat: Add support for env config of Redis username and password (#564)
-   feat: Bootstrap new `eshipper` API extension
-   feat: Make cache available to all connection settings
-   feat: add `carrier_id` to the `POST /v1/proxy/shipping/{carrier_name}/cancel` to allow precise carrier account selection for the operation. #590
-   feat: Enhance Documents REST API with support for template management CRUD operations and generic document generator API in addition to Trade API upload API. #581

### Fix

-   fix: `eshipper` cancel shipment request, and add special cancel error handling for undocumented errors
-   fix: `eshipper` `datetime` requirement for ship date and update tests for order cancellation
-   fix: tracker filter to return tracker if already existent
-   fix: `fedex` tracking estimated delivery date response parsing
-   fix: migration defaulting to hardcoded `eshipper` for `carrier_name`
-   [fix: sapient shipment cancellation response parsing](https://github.com/karrioapi/karrio/commit/660e397eb473096dc4bfc3d22eb8dcdeb3823dca)
-   [Fix FedEx multi shipment creating multiple of packages](https://github.com/karrioapi/karrio/pull/655/commits/9597f2fdfa187f1e2f7dc30583e4e05f46b33a3c)
-   [fix: invalid language and lang field default state assignment](https://github.com/karrioapi/karrio/commit/f7c1be38323853d0a61af4e7b7ff8d35b58cee73)
-   [fix: eshipper carrier data parsing for both rating and shipping response data](https://github.com/karrioapi/karrio/commit/58f37b190d0bbb9bcf3a59a067b74e2b4cb5c9fa)
-   [fix: debug and consolidate eshipper shipment cancellation with live tests](https://github.com/karrioapi/karrio/commit/e333436e29dff9718068c1d580fd43c2cd2310ac)
-   [fix: connection data parsing when saving tracing records](https://github.com/karrioapi/karrio/commit/3ff91671982a9b763d976f815a9ec40509b99635)
-   [feat: handle fedex max contact and company name](https://github.com/karrioapi/karrio/commit/71de4b7fba324ee661935a90888175b7bf792fcb)
-   fix: `usps` API token missing scope
-   fix: eShipper server URL for production mode and label problem
-   [hotfix: add fallback values to SAPIENT shipment request](https://github.com/karrioapi/karrio/commit/1fc830346f0653aefb89ed896f8817a32a1a978b)
-   fix: consolidate SAPIENT integration with live tests
-   fix: `eshipper` dimension parsing requirements
-   hot-fix(`2024.6-rc24`): migration race condition issue #645
-   clean up: remaining usage of deprecated `providers.MODELS` dynamic object created by old carrier settings models
-   hot-fix for `2024.6-rc24`: regression on carrier configuration `test_mode` assignment for carrier connection registration in live mode.
-   fix: Incorrect Item Quantity Distribution in Multi-Package Orders #634
-   fix: `eshipper` database migration leaving orphan carrier data
-   fix: #628
-   fix: authenticated requests race condition issues
-   fix: Dashboard environment variables configuration breaking change
-   fix: dashboard Nextjs undefined env var caused by deprecated environment Configs
-   fix: shipment sample fallback on document generation module
-   fix: cancel shipment `carrier_id` check
-   fix: UPS Saturday delivery option flag mapping
-   fix: FedEx variableOptions fallback value to None
-   fix: regression on FedEx shipping options parsing
-   fix: regression of quicktype schema type generation commands
-   fix: FedEx `"variableOptions"` format issue
-   fix(2 birds): cache declaration leftovers and tracing record saving failing due to cache handle

### Docs

-   docs: Update API specs and generate API docs
-   docs: update API docs with new return_address support
-   docs: setup `docusaurus` `docusaurus-openapi-docs` plugin
-   docs: Improve generated OpenAPI with annotation

### Chore

-   [chore: deprecate apps module from OSS build](https://github.com/karrioapi/karrio/pull/656/commits/e115dddee06d498d5ad5a6de0b21094e528dfc53)
-   [chore: handle `eshipper` credential transfer from username|password to principal|credential](https://github.com/karrioapi/karrio/commit/536fc037860d04cac648963e7dd038399cd7296e)
-   [chore: fix generic carrier configration parsing](https://github.com/karrioapi/karrio/commit/3ef15ca26d9a7d108f6cdceb411e94df060cae11)
-   [chore: fix docs generation and docusaurus dependencies](https://github.com/karrioapi/karrio/commit/e5dd6978569d7c6987d080e875c2b67843091754)
-   [chore: improve enum typing for lang and language configs for connectors and handle default values for carrier registration modal](https://github.com/karrioapi/karrio/commit/5a40c51755874359fc9f3356b79c18e14628d352)
-   [refactor: carrier proxies to only be generated for django admin and prevent migration requirement](https://github.com/karrioapi/karrio/commit/6889a8245eb8091d02e05644a046815f7798cc7c)
-   chore: update create_label component formatting
-   chore: update API tests for the return_address field
-   chore: update unit tests for the new return_address field
-   chore: update Readme dashboard illustration
-   chore: Apply minimal query optimization
-   chore: Prevent backup file creation from `sed` command
-   chore: investigate Admin user creation issue: `/admin/user_accounts trying to add a new user account does not get added`

### Breaking changes

-   feat: add daytime precision to tracking event time format (`AM/PM`)
-   feat: remove deprecated `eshipper_xml` extension
-   Rename legacy extension `eshiper` -> `eshipper_xml` to prepare for the upgrade to the new eShipper API
-   The Electronic Trade Document upload API was changed from `POST /v1/documents` to `POST /v1/documents/uploads`
-   The `GET /v1/documents` endpoint returning ETD upload records is now `GET /v1/documents/uploads`

> [!CAUTION]
> Please make sure to update your deployment environment variables for the dashboard when upgrading to `rc10 +`
> Check out the docs here and the following files to make sure you have the right environment variables especially if you are not using our public docker-compose files and have a custom deployment or hosted on something live Vercel.
>
> -   [Dashboard env config](https://docs.karrio.io/product/self-hosting/environment/#karrio-dashboard)
> -   Local dev [docker-compose.yml](https://github.com/karrioapi/karrio/blob/main/docker/docker-compose.yml)
> -   Hobby [docker-compose.hobby.yml](https://github.com/karrioapi/karrio/blob/main/docker/docker-compose.hobby.yml)

Special thanks to contributors: @ChrisNolan (🎉 first contribution), @jacobshilitz and @david-kocharyan

### 🚀 Celebrating a new sponsor: @alissonf216

# Karrio patch 2024.2.17

## Changes

### Fix

-   fix: FedEx duplicate tracking issue trackReplys selection

# Karrio patch 2024.2.16

## Changes

### Fix

-   fix tracking document view conflicting name causing crash when a tracker has signature or delivery image

# Karrio patch 2024.2.15

## Changes

### Feat

-   feat: Identify and ensure all required FedEx Intl data are provided according to sandbox samples
-   feat(SDK): Introduce computed `total_value` fields for Products, Package and Packages unit decorators

### Fix

-   fix: background tracking potentially None value and save related tracing records

# Karrio patch 2024.2.14

## Changes

### Feat

-   feat(TGE): Add support for Multi-piece shipment

### Fix

-   fix(#551): Invalid customs commodities assignment
    # Karrio patch 2024.2.13

## Changes

### Feat

-   feat: Add support for custom app website URL for white labelled tenant
-   feat: Apply workspace config as default tax_ids to shipper address forms

### Fix

-   fix(USPS): phone number parser to handle None values# Karrio patch 2024.2.12

## Changes

### Fix

-   fix(USPS\*): missing required PASSWORD request properties# Karrio patch 2024.2.11

## Changes

### Fix

-   fix: Missing required NumberIssuerCountryCode for DHL Express
-   fix(USPS): shipment request invalid data formatting
    # Karrio patch 2024.2.10

## Changes

### Feat

-   feat: Add customs declaration to `fedex` rate request for international shipments# Karrio patch 2024.2.9

## Changes

### Fix

-   fix: TGE missing item description fallback value
-   fix: Fedex shipping invalid extra shipper.accountNumber and soldTo fields and provided fallback values for required phone numbers.# Karrio patch 2024.2.8

## Changes

### Fix

-   fix(fedex): Signature option type# Karrio patch 2024.2.7

## Changes

### Feat

-   feat: Add missing ACCOUNT to `fedex` rate types
-   feat: Make default `fedex` rate request types configurable

### Fix

-   fix: Set a fallback value for `TGE` package description
-   fix: responsiveness for shipments and orders page headers
    # Karrio patch 2024.2.6

## Fix

-   hot-fix(`fedex`): add valid `subPackagingType` Enum# Karrio patch 2024.2.5

### Fix

-   `sscc` calculation for `TGE` integration# Karrio patch 2024.2.4
    > [!WARNING]
    > Watchout for breaking change with candapost extension. Now by default shipment are not submitted meaning you need to create a manifest to complete you shipment before pickup or dropoff.

## Hot Fix

-   Rollback problematic canadpost config migration introduced in 2024.2.3

### Breaking change

-   `candapost` shipping now require manifesting step unless you update your connection config to set `Submit shipment by default` to true.

# Karrio patch 2024.2.3

## Changes

### Feat

-   feat: Add support for marking any shipment without tracker with manual status
-   feat: Introduce manifest_required flag for carriers with manifest support
-   feat: Add Manifest `GraphQL` queries and manifest management page
-   feat: Add form for manifest creation based on selection
-   feat: consolidate `canadapost` manifest integration with live tests

### Chore

-   chore: Remove deprecated Customs CRUD APIs
-   ~~chore: Apply `transmit_shipment_by_default` for all existing `canadapost` connections~~# Karrio patch 2024.2.2

## Changes

-   fix: Improve TGE pickup date default value + sscc and shipment_id calculation
-   feat: Remove lowercase styling on APP_NAME login page
-   feat: hide sensitive email sending error from bubbling up to frontend
-   merge: @jacobshilitz [fix password reset to use EMAIL_FROM_ADDRESS as sender](https://github.com/karrioapi/karrio/pull/540/commits/254a68fdfff288816c7ebea128978ba91f9e1a60)# Karrio patch 2024.2.1

## Hot Fix

-   fix: react hooks bug caused by invalid return type" "v2024.2.rc9

### What's Changed

-   Automated build by @danh91 in https://github.com/karrioapi/karrio/pull/526
-   chore(deps): bump jwcrypto from 1.5.4 to 1.5.6 by @dependabot in https://github.com/karrioapi/karrio/pull/527
-   Debug automated build by @danh91 in https://github.com/karrioapi/karrio/pull/528
-   [hot-fix] fedex smartpost requests by @danh91 in https://github.com/karrioapi/karrio/pull/529

**Full Changelog**: https://github.com/karrioapi/karrio/compare/v2024.2.rc8...v2024.2.rc9" "v2024.2.rc8

### What's Changed

-   [hot-fixes] Hot fix 2024.2rc by @danh91 in https://github.com/karrioapi/karrio/pull/525

**Full Changelog**: https://github.com/karrioapi/karrio/compare/v2024.2.rc7...v2024.2.rc8" "v2024.2.rc7

### What's Changed

-   [patch] allied-express-local by @danh91 in https://github.com/karrioapi/karrio/pull/517
-   chore(deps): bump cryptography from 42.0.0 to 42.0.2 by @dependabot in https://github.com/karrioapi/karrio/pull/518
-   chore(deps): bump cryptography from 42.0.2 to 42.0.4 by @dependabot in https://github.com/karrioapi/karrio/pull/519
-   [release] Karrio 2024.2 by @danh91 in https://github.com/karrioapi/karrio/pull/520

**Full Changelog**: https://github.com/karrioapi/karrio/compare/v2024.2.rc5...v2024.2.rc7" "v2024.2.rc5

### What's Changed

-   [carrier-integration] Allied express local integration by @danh91 in https://github.com/karrioapi/karrio/pull/511
-   [carrier-integration] Deutsche Post by @danh91 in https://github.com/karrioapi/karrio/pull/512
-   Minor fixes by @danh91 in https://github.com/karrioapi/karrio/pull/513
-   [hotfix] Rename `deutschepost` -> `dhl_parcel_de` by @danh91 in https://github.com/karrioapi/karrio/pull/514
-   chore(deps): bump django from 4.2.8 to 4.2.10 by @dependabot in https://github.com/karrioapi/karrio/pull/515
-   feat: Australiapost full integration by @danh91 in https://github.com/karrioapi/karrio/pull/508
-   docs: Documentation update for 2024.2 release by @danh91 in https://github.com/karrioapi/karrio/pull/516

**Full Changelog**: https://github.com/karrioapi/karrio/compare/v2024.2.rc4...v2024.2.rc5" "v2024.2.rc10

### What's Changed

-   chore(deps): bump weasyprint from 61.0 to 61.2 by @dependabot in https://github.com/karrioapi/karrio/pull/530
-   [hot-fixes] Publish Karrio 2024.2 by @danh91 in https://github.com/karrioapi/karrio/pull/522

**Full Changelog**: https://github.com/karrioapi/karrio/compare/v2024.2.rc9...v2024.2.rc10# Karrio Shipping Platform Edition 2024.2

> [!IMPORTANT]
> 🥳 Karrio 2024.2 is officially finally out. Chat with us on [Karrio Launch Week](https://www.karrio.io/launch-week-x) to learn more about our vision for 2024

### Feat

-   Introduce Karrio Manifest API
-   Introduce Karrio dashboard home page with usage stats and guidance
-   Australia Post full integration (rating, label generation)
-   DHL Parcel Post integration (upgrade from the `dpdhl` integration planned for sunsetting)
-   FedEx REST API integration (upgrade from former FedEx web service integration)
-   Add support for dynamic options field generation in label generation forms
-   Add support for FedEx Smart Post rating and label creation
-   Introduce bulk shipment fulfilment
-   Upgrade creating objects by id to use `dict` instead of plain `string`
-   Refactor and improve loading flow for create_label forms
-   Introduce Workspace config object with GrapQL API support
-   Introduce manifest interface to Karrio SDK
-   Separate profile from account settings and introduce workspace config form
-   Preload customs declaration options using saved workspace configs
-   Add zones column to rate sheet
-   Introduce TGE extension

### Breaking Changes

-   Move legacy FedEx web service integration as fedex_ws extension
-   Remove the deprecated suburb field from the Address object

### Fix

-   fix: FedEx WS rating issue caused by SmartPost changes
-   fix: Allied Express min volumes
-   fix: DHL Express `customs.options` mapping

### Docs

-   Improve documentation navigation and document karrio environment + new products + enrich FAQ (WIP)
-   Introduce carrier documentation with details for capabilities, shipping options and services
-   document local development installation requirements for cloud VMs
    # Karrio preview 2024.2.rc4
    > [!IMPORTANT]
    > You can safely upgrade to this release same as previous patches. I have decided to name it Preview as it is the pre-release to the upcoming major `2024.2` release. I still recommend testing with the staging instance before updating your production instance.
    > I have been trying to work with short-lived branches where I lay the foundations for epic features and iterate faster. It is less overwhelming and allows for quick iteration. And makes it easy to solve issues and release patches more often.

### Feat

-   Add `metadata_value` and `metadata_key` filter for carrier connections
-   Add brand colour config support to allied_express connection configs
-   Replace`dpdhl` GET tracking request with POST
-   Add support for rate sheet object management (WIP)

### Fix

-   fix `easypost` tracking response parsing
-   fix `ups` invalid property added to `third_party` payment declaration
-   fix `metadata_key` filter queryset for GraphQL resolver

# Karrio preview 2024.2.rc3

> [!IMPORTANT]
> You can safely upgrade to this release same as previous patches. I have decided to name it Preview as it is the pre-release to the upcoming major `2024.2` release. I still recommend testing with the staging instance before updating your production instance.
> I have been trying to work with short-lived branches where I lay the foundations for epic features and iterate faster. It is less overwhelming and allows for quick iteration. And makes it easy to solve issues and release patches more often.

### Feat

-   Improve generic carrier brand colour rendering
-   Make allied express `service_type` and `account_service_type` config plain text input fields

### Chore

-   fix orders and shipments list styling

# Karrio preview 2024.2.rc2

> [!IMPORTANT]
> You can safely upgrade to this release same as previous patches. I have decided to name it Preview as it is the pre-release to the upcoming major `2024.2` release. I still recommend testing with the staging instance before updating your production instance.
> I have been trying to work with short-lived branches where I lay the foundations for epic features and iterate faster. It is less overwhelming and allows for quick iteration. And makes it easy to solve issues and release patches more often.

### Feat

-   Add `metadata_value` and `metadata_key` filter for carrier connections
-   Add brand colour config support to allied_express connection configs
-   Replace`dpdhl` GET tracking request with POST
-   Add support for rate sheet object management (WIP)
    # Karrio preview 2024.2.rc1
    > [!IMPORTANT]
    > You can safely upgrade to this release same as previous patches. I have decided to name it Preview as it is the pre-release to the upcoming major `2024.2` release. I still recommend testing with the staging instance before updating your production instance.
    > I have been trying to work with short-lived branches where I lay the foundations for epic features and iterate faster. It is less overwhelming and allows for quick iteration. And makes it easy to solve issues and release patches more often.

### Feat

-   bulk order fulfilment processing on the dashboard
-   Introduce draft order creation form
-   add type details for shipping options
-   Introduce a home page with usage stats and action guidance
-   add bulk label and invoice printing for orders
-   add bulk label and invoice printing for shipments
-   redesign: orders and shipments layout and info
-   Add API usage graph to developers' overview page
-   Make the Allied Express server URL configurable
-   Add brand and text colour configuration for generic carriers
-   Improve order processing with batches API allowing attaching new batch operations for existing orders
-   Improve shipment processing with batches API to allow linking new batch operation with existing shipment by id
-   Add support for `brand_color` and `text_color` for generic carrier config
-   Introduce `images` to the tracker for signature and delivery images
-   Expose `delivery_image_url` and `signature_image_url` to OpenAPI and GraphQL API
-   Add proof of delivery image support for UPS tracking

### Fix

-   fix: Adming queries for system usage stats
-   fix: ZPL label `dpmm` for preview
-   fix: duplicated carrier gateway call bug

### Chore

-   chore: clean up lists layout
-   chore: Clean up `create_label` form and state management

### Breaking changes

-   The document generation API endpoint has been replaced from `/documents/` -> `documents/templates/`

### Celebrating Karrio's newest sponsor 🥳 🎉 🎉

Thanks, @DarkSwoop for sponsoring Karrio 🙏🏿

# Karrio patch 2023.9.13

## Changes

### Feat

-   feat: Add workflow webhook URL
-   feat: reorganize workflow action data to provide dedicated tabs for input, output logs and details
-   feat: Introduce `metafields` and link to workflow objects
-   feat: Improve workflow execution data flow and tracing
-   feat: Add support for workflow conditional action and single action execution
-   feat: Add support for Posthog on the API, dashboard and docs

### Fix

-   merge: Use HS code for DHL Express customs declaration by @DarkSwoop
-   USPS label response conditional parsing when errors are returned and set defaults for secondary address lines #491

Special thanks to @DarkSwoop for the valuable feedback from DHL contacts that helps improve Karrio's DHL express extension# Karrio patch 2023.9.12

## Feat

-   Add pending status to karrio SDK to handle event code when a package hasn't been picked up and can still be cancelled
-   Add admin module to OSS build
-   Move action buttons to the header on the developers' sub-section
-   Add basic CRUD operation for system carrier management
-   Prepare rate sheets management card
-   Add staff permission management admin APIs
-   Add minimal staff user management functionalities to the admin dashboard
-   Introduce and configure `strawberry_django` optimizer
-   Introduce karrio automation panels to the dashboard
-   Finalize beta workflow creation form in the dashboard

## Chore

-   Separate core Graphql types and queries from ee
-   Add sponsors section to README

## Fix

-   Easypost Fee parsing issue
-   Add omitted customs cancel request options
-   Fix grammatical and sentence structure errors in the OpenAPI schema page

I am particularly excited about karrio built-in automation. The vision is to simplify syncing data between karrio and other platforms.
I have been asked for integrations with platforms such as Shopify, Woocommerce, Commercetools and various ERP systems to sync orders and relevant data across the systems. With karrio built-in automation, I hope to tackle that with the least amount of work.

Shout out to Fadi owner at [Shipr](https://www.shipr.com.au/) as we collaborate to make Karrio a turnkey solution for 3PLs and logistics providers.
With this, they will be able to deploy their dedicated shipping platform, automate shipping but, also empower their merchants and customers with their own workspace and API access. In addition to our API and Webhook, it will be even easier to integrate karrio and build your custom shipping tech stack.

Reach out for private beta access to [Karrio Cloud](https://www.karrio.io/)

<p align="center">
 <img width="400" alt="Screenshot 2023-12-31 at 12 35 14 AM" src="https://github.com/karrioapi/karrio/assets/10974180/154c9448-4335-433c-b3a3-e584f795a199">

<img width="400" alt="Screenshot 2023-12-31 at 12 34 48 AM" src="https://github.com/karrioapi/karrio/assets/10974180/2b17c8b8-9732-4ded-9f41-e4788d8554c3">

<img width="400" alt="Screenshot 2023-12-31 at 12 34 27 AM" src="https://github.com/karrioapi/karrio/assets/10974180/353c856c-9774-470d-8f4e-ec2984c1dead">

</p>
# Karrio patch 2023.9.11
## Feat

-   Add rating and label generation to sendle integration

## Chore

-   (merge) @jacobshilitz fix for API logs index
-   (merge) @jacobshilitz fix for `vscode` path updates
-   (fix) canadapost multi-piece shipment parsing

Special thanks to @jacobshilitz for the powerful performance fix for API log indexes 🔥 # Karrio patch 2023.9.10

## Feat

-   Add allied express service listing on the connection config modal# Karrio patch 2023.9.9

## Feat

-   (improve) addresses and parcel listing page layouts to handle large numbers
-   (add) support for live address full search on name input
-   (update) name input to autocomplete with headless UI Combobox component# Karrio patch 2023.9.8

## Changes

-   (fix) dashboard org switcher inconsistency on the frontend
-   (add) meaningful defaults for rate and label generation requests of `allied_express` extension
-   (introduce) RateSheet object (reusable dedicated rate sheet object that can be linked to various carriers with custom sheet content)
-   (add) GraphQL APIs to manage rate sheets# Karrio patch 2023.9.7

## Changes

-   (improve) UX and design consistency across the dashboard
-   (add) new carrier integration for Allied Express
-   (fix) missing fixed weight unit for canadapost customs item definition
-   (merge) @DarkSwoop paperless trade filter fix
-   (add) unit tests for non-supported paperless trade shipment # Karrio patch 2023.9.6
-   (fix) `dhl_express` option parsing and filter# Karrio patch 2023.9.5
-   (fix) issues with dynamically set `paperless_trade` option and `dhl_express_all`
-   (add) support for shipment messages parsing for `easypost`
-   (fix) `asendia_us` connection configuration requirements# Karrio patch 2023.9.4

### Changes

-   Introduce the Karrio admin server module with an admin GraphQL API
-   Lay the foundation of the Karrio admin dashboard in the same codebase as the current dashboard# Karrio patch 2023.9.3
-   (fix) **DEFAULT_SERVICE** imports for carriers with custom rate sheets
-   (fix) `dhl_express` paperless trade option processing# Karrio patch 2023.9.2
-   (refactor) Enum types and various usages due to related breaking changes in `Python 11`
-   (update) docker base images to `python:3.12-slim` and development image to `python:3.12-slim-bullseye` to improve development on Mac M chips# Karrio patch 2023.9.1
-   (merge) `dhl_express` dutiable fix by @DarkSwoop
-   (fix) canadpost multi-piece shipping cancellation options
-   (update) vulnerable dependencies

Special thanks to @DarkSwoop # Karrio Shipping Platform Edition 2023.9

## Changes

-   Canada Post multi-piece shipment support [#392](https://github.com/karrioapi/karrio/issues/392)
-   [carrier-integration] GEODIS (full integration) [#390](https://github.com/karrioapi/karrio/issues/390)
-   [carrier-integration] Colissimo [#389](https://github.com/karrioapi/karrio/issues/389)
-   [carrier-integration] BPost [#435](https://github.com/karrioapi/karrio/issues/435)
-   [carrier-integration] TNT (full integration) [#425](https://github.com/karrioapi/karrio/issues/425)
-   [carrier-integration] Asendia US (full integration) [#163](https://github.com/karrioapi/karrio/issues/163)
-   (POC) of integration compatibility for `zoom2u` and `locate2u` last mile systems
-   (replace) `amazon_mws` extension by `amazon_shipping`
-   (remove) `yanwen`, `yunexpress` and `sf-express` extensions
-   (clean) up background job tracing

### Dev ex

-   Remove commercial license code leaving the repository with only **Apache v2 OSS** edition server modules
-   Major repository restructuration moving toward a **monorepo** with **server**, **dashboard** and **docs** under karrio's main repository
-   Deprecate separate schema packages for carriers in favour of moving the schemas and generated types directly into the carrier's extension packages
-   Improve Karrio CLI extension template

# Karrio patch 2023.5.3

-   DHL Universal - Error when adding DHL eCommerce tracker. [#439](https://github.com/karrioapi/karrio/issues/439)
-   DHL Express - IsDutiable determination [#437](https://github.com/karrioapi/karrio/issues/437)
-   Paperless Trade - Missing document format using webinterface [#438](https://github.com/karrioapi/karrio/issues/438)# Karrio patch 2023.5.2
-   [dev-ex] Set up build from source [#416](https://github.com/karrioapi/karrio/issues/416)
-   [DHL-Conflict] Pickup XML request issue [#414](https://github.com/karrioapi/karrio/issues/414)
-   Fix Tracking API 500 issue [#410](https://github.com/karrioapi/karrio/issues/410)
-   Merged UPS multi-parcel individual weight [#418](https://github.com/karrioapi/karrio/pull/418)

Thanks to @jacobshilitz for the quick fix# Karrio patch 2023.5.1

-   Ensure cache params are optional with a default value
-   Handle auth token error parsing
-   Disable DHL Express dutiable flag for EU countries
-   Fix / Improve DPDHL Error

Special thanks to @nahall for the USPS service update# Karrio Shipping Platform Edition 2023.5

## Changes

-   (upgrade) UPS API integration to the latest #387
-   (fix) intermittent issue with Canada Post options #381
-   (add) configurable options to FedEx and DHL express connections
-   (fix) carrier config mutation regression
-   (add) metadata to tracker POST API request data
-   (fix) DHL express `"DOC"/"NONDOC"` #367
-   (remove) support for UPS Freight

### Updating to UPS REST API with Oauth2 authentication

**UPS and deprecating their XML and JSON legacy APIs in favour of their new REST API with Oauth2 support. You will need to update your Carrier connection with your app `client_id` and `client_secret`**

_follow these instructions to get your new API credentials_

-   Visit [https://developer.ups.com/apps?loc=en_US](https://developer.ups.com/apps?loc=en_US)
-   Create a new app
-   Copy your `client_id` and `client_secret` to update your karrio's UPS connections

<details>
<summary>app creation screenshots</summary>

![Screenshot 2023-06-04 095624](https://github.com/karrioapi/karrio/assets/10974180/82d07d6e-a754-41d5-8260-f38cfa67e812)

![ups-app-creation-setup](https://github.com/karrioapi/karrio/assets/10974180/cf60f949-02fe-4f85-a6a0-0721ca0d704b)

![ups-app-credentials](https://github.com/karrioapi/karrio/assets/10974180/e91beb7e-10e1-495e-af81-80535d63521d)

</details>

# Karrio 2023.4.6 patch

## Fixes

-   (fix) organization invite on multi-tenant deployments
-   (fix) Canada post falsy options mapping #381
-   (fix) FedEx transit day resolution excluding weekends
-   (simplify) computed address_lines (combining street_number with street_name)
-   (fix) duplication in combined packages description
    # Karrio 2023.4.4 patch

## Changelog

-   (merge) #372
-   (fix) #370
-   (fix) #333 -> a way to handle service suffixes
-   (add) migration fix for tracker info data
-   (add) DHL prefix to native dhl_express service code and filter
-   (introduce) `packstation` as an explicit option and adjust DPDHL
-   (introduce) `service_suffix` config for fixed service suffix with DPDHL
-   (fix) tracker info update
-   (fix) misspelled carrier_tracking_link mapping for shipment tracker
-   (update) tracking status computation to support new statuses and prevent `in_transit` override
    # Karrio 2023.4.2 patch
-   (fix) DPDHL tracking response parsing caused by inconsistent `leitcode` with the schema type
-   (improve) DPDHL error parser (#368)
-   (remove) deprecated field on custom carrier service admin form# Karrio Shipping Platform Edition 2023.4

## What's new

-   (add) `GEODIS` tracking carrier integration
-   (add) `La Poste` tracking carrier integration
-   (add) `Boxknight` carrier integration
-   (add) `Roadie` carrier integration
-   (add) `Nationex` carrier integration
-   (introduce) carrier connection default configuration
-   (improve) order `db` query adding a direct relationship with shipments
-   (improve) migrations for large datasets
-   (add) exception-related shipment status mapping between trackers and shipments.
-   (introduce) label preview for ZPL using `labelary` API
-   (improve) DHL Express support for EU

### Bug Fixes

-   (fix) tracking info property typo
    # Karrio 2023.3.4 patch

## Fixes

-   (fix) DHL support for EU rating and label creation
-   (fix) customs partial update mutation
-   (add) support for HTML response parsing and update DPDHL error parsing to process HTML responses
-   (fix) tracker info data merging# Karrio 2023.3.2 patch

## Fixes

-   (fix) UPS ETD integration

Thanks, @jacobshilitz for the patch# Karrio Shipping Platform Edition 2023.3

## What's New

-   (add) DPD carrier integration `carrier-integration`
-   (enhance) static service level definition with support for zones
-   (introduce) unified tracking statuses
-   (enrich) tracking details with package and shipment info
-   (add) `street_number` field to `Address` model
-   (add) `carrier_tracking_link` to `shipment.meta`

```
	"meta": {
		"carrier_tracking_link": "https://www.fedex.com/fedextrack/?trknbr=794622728852",
		"tracking_numbers": [
			"794622728852"
		],
		"ext": "fedex",
		"carrier": "fedex",
		"service_name": "FEDEX INTERNATIONAL ECONOMY",
		"rate_provider": "fedex"
	},
```

-   (enrich) tracker details with :

```
{
 "tracking_number": "string",
 "carrier_name": "amazon_mws",
 "account_number": "string",
 "reference": "string",
 "info": {
 "carrier_tracking_link": "string",
 "customer_name": "string",
 "expected_delivery": "string",
 "note": "string",
 "order_date": "string",
 "order_id": "string",
 "package_weight": "string",
 "package_weight_unit": "string",
 "shipment_package_count": "string",
 "shipment_pickup_date": "string",
 "shipment_delivery_date": "string",
 "shipment_service": "string",
 "shipment_origin_country": "string",
 "shipment_origin_postal_code": "string",
 "shipment_destication_country": "string",
 "shipment_destination_postal_code": "string",
 "shipping_date": "string",
 "signed_by": "string",
 "source": "string"
 }
}
```

_Note that you can override all the info fields using `POST /v1/trackers` and `PUT /v1/trackers/{tracker_id}`_

-   (add) `latitude` and `longitude` to the `TrackingEvent` model for future use with last-mile carriers and automatic background updates by Karrio.

## Fixes

-   (revert) to FedEx single call ETD implementation
-   (invalid) mapping of the `Suburb` field on the `DHL Express Rate` request
-   (fix) incoherent UPS service names

## Changes

-   (deprecating) `DELETE /v1/orders/{order_id}` in favor of `POST /v1/orders/{order_id}/cancel`
-   (change) tracking request details at the SDK level.
-   Introduce `account_number` and `reference`
-   Remove `level_of_details` and `language`
-   (renamed) UPS services to be region aware (`This will require draft shipments rates to be refreshed`)

# Karrio 2023.1.12 patch

## Changes

-   (fix) regression on one call label generation webhooks trigger
-   (fix) background data archiving on multi-tenant deployments
-   (fix) UPS rate fetch inconsistent transit details
-   (improve) DPDHL requests mapping
-   (update) DPDHL connection settings to correct the authentication problem
-   (raise) error when creating trackers if tracking fails by default.
    And create `tracker` despite errors when `pending_pickup` flag is specified
-   (improvement) of Sendle tracking details

Special thanks to @DanielOaks for the Sendle tracking API update.# Karrio 2023.1.11 patch

-   (enhance) FedEx ETD integration with single request document uploads and label generation# Karrio 2023.1.10 patch

## Changes

-   (update) `dpdhl` to latest schemas 3.4.0
-   (update) minor versions for DPDHL SOAP requests
-   (add) missing UPS shipping options and improve tax parsing
-   (fix) UPS multi-piece labels bundling
-   (apply) FedEx ETD requests requirement patches
-   (introduce) title to commodity as main name
-   (make) all org tracing records accessible to all org users
-   (replace) DISTINCT ON by python code for SQLite support of document generation
    # Karrio Shipping Platform Edition 2023.1

## Changes

-   Migrate to Strawberry for GraphQL support
-   Karrio Admin API foundation
-   Finalize OpenID support through karrio apps registration `experimental`
-   Batch shipment creation (CSV import + batch REST API) `experimental`
-   Batch order creation (CSV import + batch REST API) `experimental`
-   Batch tracker creation (CSV import + batch REST API) `experimental`
-   Add support for shipping `billing_address` and improve support for 3rd party billing
-   Add carrier capabilities to `/v1/carriers` JSON response
-   Remove Postgres-specific fields to allow support for any Django ORM-supported databases (MySQL, Oracle, SQLite...)
-   Add support for `DATABASE_URL` to configure karrio' database connection with a single line
-   Introduce data retention configuration (set up karrio to flush your database of old shipments, API logs...)
-   Improve SDK tracing recording for full transparency (only super admin can see requests logs of system carriers)
-   Add `id` to keyword full-text search for orders and shipments
-   Improve shipment data GraphQL mutations and draft shipment management.
-   Improve international shipment with advance duty 3rd party payment address

## Added to open-source build

-   Orders module (read-only orders fulfilment API)
-   Generic carrier (Register carriers without APIs on karrio to become their API - manage rate sheets, design labels...)
-   Data module (Batch APIs for data imports and batch creation + data export API)
-   Documents module (Document generation API + templating system to generate branded shipping documentation)
-   Document generation use cases: UCC128 labels, Packing slips, branded commercial invoices... anything you need :)

## Dreprecation and Regression

-   Remove support for price range filters to apply rate add-ons
-   Replace `DELETE /v1/shipments/{id}` by `POST /v1/shipments/{id}/cancel` for shipment cancellation
-   Deprecating `GET v1/trackers/{carrier_name}/{tracking_number}` in favor of `POST /v1/trackers` for trackers creation

## Dev experience

-   Improve scripts under the `/bin` folder to simplify development and deployment
-   Introducing Karrio `hobby-deploy` (+ upgrade) to simplify Karrio installation on any cloud with SSL provisioning included
-   Add `vscode` support debug commands to allow running karrio with debugger and breakpoints
-   Add scripts to install karrio without docker (Python packages)
-   Return to SQLite as the default development database to simplify development setup without docker

" "Patch release 2022.8.19

-   Make FedEx ETD optional" "Patch release 2022.8.18
-   (add) preferred units for FedEx US shipment
-   (fix) missing options error on FedEx shipment creation
-   (consolidate) FedEx ETD integration

Special thanks to @nahall for the contribution# Karrio Shipping Platform Edition 2022.8

## Changes

-   Introduce shipping document upload interface for paperless capability
-   DPDHL carrier integration
-   UPS Freight JSON API carrier integration
-   Amazon MWS carrier integration `(experimental)`
-   Chronopost carrier integration (By @Ftayri)
-   Move Oauth2 and OpenID support to OSS build
-   Introduce Karrio CLI powered by [type](https://typer.tiangolo.com/typer-cli/)
-   Add `freight_class` property to parcel for pallet and LTL shipment support
-   Introduce organization user roles and group permissions `(insiders-only)`
    # Karrio Shipping Platform Edition 2022.6

## What's Changed

-   Integrate 2FA for login
-   Introduce package level options (for package insurance/coverage)
-   Add support for audit logging (`insiders only`)
-   Persist carrier requests logs for the foundation of advanced debug mode
-   Data imports foundation for batch tracking data import (`insiders only`)
-   Deprecate `test_mode` flags in favour of `API Keys` in a test or live modes
-   Improve API queries using SQL indexes (API logs, API events, Shipments, Orders...)
-   Improve and standardized error response
    # Karrio Shipping Platform Edition 2022.4

### What's New

-   Distinguish carrier hubs extensions from regular extensions
-   Fix UPS shipment cancellation API call (VOID) (https://github.com/karrioapi/karrio-dashboard/issues/190)
-   Add GraphQL mutations for webhooks
-   Add GraphQL mutations for orders
-   Beta AmazonMws carrier integration
-   Improve DHL Universal tracking extension response parsing and edge cases from all supported DHL services.
-   Set fallback values for DHL express extension shipment commodity codes
-   Set fallback values for FedEx extension shipment address phone numbers.
-   Add webhook for order update
-   Reduce noise in carrier request logs (remove duplicates and make logging optional on Serializable abstraction)
-   Introduce a data module (`insiders only`) for data export (csv, json, xls...). Currently, support exporting orders and shipments

#### Breaking changes

-   Uniformize collection APIs filters for GraphQL and REST APIs
-   Deprecate noisy properties from rates

**Before**:

```JSON
{
 "id": "string",
 "object_type": "rate",
 "carrier_name": "string",
 "carrier_id": "string",
 "currency": "string",
 "service": "string",
 "discount": 0,
 "base_charge": 0,
 "total_charge": 0,
 "duties_and_taxes": 0,
 "transit_days": 0,
 "extra_charges": [ ],
 "meta": { },
 "test_mode": true
}
```

**Now**:

```JSON
{
 "id": "string",
 "object_type": "rate",
 "carrier_name": "string",
 "carrier_id": "string",
 "currency": "string",
 "service": "string",
 "total_charge": 0,
 "transit_days": 0,
 "extra_charges": [ ],
 "meta": { },
 "test_mode": true
}
```

# Karrio Shipping Platform Edition 2022.3

## What's New

-   Rebrand Purplship -> Karrio
-   Improve document management modules (enrich shipment and order template contexts).
-   Introduce `order.order_date` and `line_item.unfulfilled_quantity` properties for better handling of partial orders.
-   Improve custom carrier label management
-   Provide default order and shipment dates
-   Fix tracker `in_transit` status inconsistency
-   Introduce Sentry support for Karrio dashboard error tracking and APM" "Purplship Shipping Platform Edition 2022.2

## Road to cloud beta

-   Consolidate email flows for operations that require confirmations
-   Consolidate organization and team management (`insiders`)
-   Organization members listing and invitation
-   Organization ownership transfer
-   Organization creation
-   Setup foundations for oauth2 and apps integration (beta) (`insiders`)
-   Implement Webhook secret header for event origin signature validation
-   Integrate One-call shipment label purchase
-   Automate incremental tracking_number generation for customs carrier labels
-   Order management update (`insiders`)
-   Introduce `shipping_from` for orginin address prefill
-   Rename `shipping_address` to `shipping_to`

## Breaking changes

-   **The GraphQL API queries and mutations have been enhanced and some renamed for consistency.**
    **We highly recommend using the same version on the server and dashboard**

-   **Introduce `docs: Documents = JStruct[Documents, REQUIRED]` to `ShipmentDetails`**

_The implied the removal of the `label: str` field from the root of `ShipmentDetails` to `ShipmentDetails.docs.label`_

Proxy API `POST /v1/proxy/shiping` now returns as `docs` object with `label` base64 string and optionally an `invoice` base64 string

API `Shipment` object now returns

-   `label_url`: URL to the purchase shipment label
-   `invoice_url`: URL to the purchase shipment invoice when supported

API `Shipment` deprecated data

-   `label` field has been deprecated and removed in order to optimize shipments database queries and size
-   `shipment.meta.invoice` field has been deprecated and removed for optimization as well

**As a result of this change, shipments requests are less heavy and faster**

## Bugs

-   Inconsistent Charfield validation caused validity pre-request and failure to persist carrier API changes to the database.

## Docker builds

Current release `2022.2` - `danh91.docker.scarf.sh/purplship/server:2022.2`
" "Purplship Shipping Platform Edition 2022.1

## What's New

-   Introduce `purplship.generic` the custom carrier extension
-   Add support for custom carrier definition on purplship server
-   Enrich parcel (package) definition for better support of pallets
-   Enhance purplship universal extension support with multi-piece shipment support
-   Introduce order APIs for the relation between order systems and purplship shipments
-   Introduce label template configuration and custom label generation
-   Introduce support adding user metadata to purplship objects (`Order`, `Tracker`, `Commodity`, `Shipment`...)

## Breaking changes

_The Shipping REST APIs are focused on automation and single requests to perform shipping operations. The GraphQL API on the other hand powers manual operations from the dashboard with multiple mutations of shipping objects._

For that reason

-   The following endpoints have been removed
-   `/v1/shipments/<id>/options` to update/add shipment options
-   `/v1/shipments/<id>/customs` to add shipment customs declaration
-   `/v1/shipments/<id>/parcels` to add shipment parcels

_There has been many breaking changes on mutations and queries on the GraphQL API so we recommend checking out the [2022.1.4 purplship dashboard release](https://github.com/purplship/purplship-dashboard/releases/tag/v2022.1)_

## Patch & bug fixes

-   Update support for multi-tenant deployment
-   Prevent automatic tracker creation issues for carriers without `tracking` capabilities
-   Fix supported destination check for `USPS` domestic extension
-   Fix background tracker processing error caused uncaught by dead code

## Docker builds

Stable version `2022.1.4`
danh91.docker.scarf.sh/purplship/server:2022.1.4
" "Purplship Shipping Platform Edition 2021.11

## What's New

-   Apply Canadian postal code pre-validation patch
-   Improve Trackers API to accept tracking numbers without a record as pending
-   Retrieved `estimated_delivery` during tracking for all supporting carriers
-   Ensure FedEx dimension definitions only when `packaging_type` is `your_packaging`
-   Introduced Persisted events
-   Improve FedEx multi-piece shipment compiling all package labels together
-   Introduce DHL Parcel Poland `sponsored` integration (https://github.com/purplship/purplship/issues/166)
-   Introduce the purplship universal carrier service level definition
-   Apply (2121.7.7) database query perf improvements
-   Introduce `TRACKING_PULSE` env var to setup background trackers update interval seconds
-   Introduce `BASE_PATH` env var to set up runtime base path for the API (e.g: `/api` for `example.com/api` deployment)
-   Introduce advanced query filters for shipments, logs, events, trackers and webhooks

## Bugs

-   Fix Webhooks notification scope only to related account and organization" "Purplship Shipping Platform Edition 2021.10

## What's New

-   Enrich `/api/references` endpoint with application metadata info (`APP_NAME`, `APP_VERSION`, `APP_WEBSITE` and other feature flags)
-   Enhance JWT refresh with support for org switching by providing `org_id`
-   Improve OpenAPI docs with existing extensions `carrier_name`(s) and shipments and trackers filters status enums
-   Remove authentication requirement from `/v1/trackers/{id_or_tracking_number}` to simplify trackers access to frontend components
-   Remove authentication requirement from `/api/references` as it serves as the server metadata now and share any user private info
-   Change authentication rules for Graphql view (`/graphql`)
-   The GraphQL Playground can be accessed without being authenticated
-   However, an authentication header is required now to send authenticated requests and receive users owned data
-   Introduce user registration, password change, password reset and more through GraphQL mutations
-   Remove purplship embedded client moving the codebase to https://github.com/purplship/purplship-dashboard

### Bug Fixes

-   Fix circular reference on GraphQL system `carrier.carrier_name` property
-   Fix bugs with exception raised when there is an existing carrier connection in test mode and not live

### Dev Ex

-   Switched to mono repo bringing `purplship-carriers`, `purplship-bridges`, `purplship-server` and all other satellite projects under `purplship` (this simplifies the development process)
-   Improve PHP and Python client generator script options
-   Improve docker setup for local developments
-   Improve docker setup for testing with the same config as production (went from `6 min` build + test time to `2 min`)
-   Change namespaces for consistent branding (went from `purpleserver.*` -> `purplship.server.*`)
-   add as shared .vscode configuration.
-   Fix JWT regression caused by `PyJWT` dependency
-   Enhance Docker image startup and graceful-stop with dumb-init

" "purplship SDK 2021.8

## What's new?

-   Increase JSON API response parsing resilience by introducing `to_object` helper that ignores unknown model fields
-   Use `NamedTuple` to define MeasurementOptionsType instead of `Enum`
-   Add .vscode config to improve dev ex
-   Add alpha integration for `ICS Courier`, `UPS Ground` and `Asendia US`" "purplship SDK 2021.7

## Changes

-   Apply flexible service mapping to all carrier integrations. (meaning that if the carrier introduces a service not mapped by purplship, it will still be handled gracefully by collecting the code required for the shipment creation)
-   Add DHL customs invoice when returned by international shipments
-   Introduced `account_country_code` as base property to all carrier settings. (This is useful for country-specific carrier accounts)
-   Deprecate `gateway.features` in favor of `gateway.capabilities` to describe the list of supported operations by carrier gateways
-   Add pre requests check hooks to validate early carrier gateways capability support as well as country-bounded account usage.
-   Improve the email notification option
-   enabled by default if a recipient email is provided
-   turn the notification off `options: { ..., email_notification: false, ..}`
-   set specific email for notification `options: { ..., email_notification_to: custom@email.com, ..}`

## Fixes

-   Fix shipment reference for all carriers
-   Fix Purolator shipment creation error detection for proper parsing
    " "purplship SDK 2021.6

## Changes

-   Fix FedEx label format
-   Add human-readable names for options and services
-   Add blank Purolator label for test mode since label is not supported with the sandbox server
-   Live tested USPS rating and shipping integration
-   Rename `purolator_courrier` extension to `purolator`
-   Make Purolator setting `user_token` optional
-   Fix Fedex rate timestamp parsing to prevent 0-day returns
-   Fix DHL preset default units with the right package sizes
-   Add omitted `contract_id` to Canada post extension for rate requests
-   Add min dimensions values for FedEx dimension mappers
-   Handle Optional adjustments values for Canada post rate response

" "Purplship SDK 2021.4

## What's new

-   Enrich customs declaration unified model
-   Separate duty definition from the shipment payment model
-   Introduce AddressExtra and a helper to compute address line based on extra
    " "Purplship SDK 2021.3

## Changes

-   Integrate TNT services (Tracking )
-   Prepare USPS rating and shipping integration and split up international and local
-   Rename `ups_package` -> `ups`
-   Rename `fedex_express` -> `fedex`" "Purplship SDK 2021.2 [tracking spree]

## Carrier Tracking service integration spree

-   integrate `aramex` Tracking API
-   update `canpar` Full API integration
-   integrate `australiapost` Tracking API
-   integrate `dhl_universal` Tracking API
-   integrate `dicom` Tracking API
-   integrate `usps` Tracking API
-   integrate `dicom` Tracking API
-   integrate `sendle` Tracking API
-   integrate `sf_express` Tracking API
-   integrate `yanwen` Tracking API
-   integrate `yunexpress` Tracking API

## Other

-   Introduce the concept of features for gateways to show supported APIs dynamically
-   Make Purolator `user_token` required to set up a Purolator gateway
-   Improve canpar's SOAP requests ensuring proper namespace prefixes for all nodes
    " "Purplship SDK 2021.1

## Major Changes

-   Introduce `poetry` for packaging
-   Make Purplship API interface uniform with `purplship.[API].[request](...).from_(gateway).parse()`
-   Deploy `purplship` and all `purplship.extensions` wheels on Pypi

### Enhancements

-   Introduce extension tests templates
-   Log request URLs
-   Update docs" "[release] Purplship SDK 2020.12 (docs and contribution friendly)

## Docs and Contribution Friendly

-   Introduce Purplship SDK docs with `Mkdocs`
-   Introduce formal Purplship Extension with the `Metadata` definition
-   Introduce basic documentation for `Custom Carrier`
-   Add Purplship extension template" "Purplship SDK 2020.12.1 [patch]

## What's New

-   Introduced `MeasurementOptions` as Dimension and Weight output customization for each carrier
-   Introduced `label_type` as a requirement for shipment creation

## Fixes

-   Fix unsupported Canada post decimal values for dimensions and weight
-   Prevent confusing Purolator exception when address properties are required and not defined
-   Fix invalid `CM` -> `IN` conversion
-   Consolidated `Purolator` shipment cancellation request"

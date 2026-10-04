# Medidores utilizados en la estimación

Fuente: respuestas de Azure Retail Prices API guardadas el 03/10/2026. Índice desde cero dentro de `Items`. Selección documentada el 04/10/2026; no se volvió a cotizar.

La licencia SQL de USD 145.95036/mes proviene de la [exportación de calculadora](../calculadora_sql_base.xlsx); no se confunde con el medidor de cómputo. Los tramos de Functions se aplican a consumo bruto para un presupuesto conservador, sin descontar franquicias.

| Archivo e índice | Producto / SKU | Medidor | Región | Precio USD | Unidad | Inicio del tramo | meterId |
|---|---|---|---|---:|---|---:|---|
| [precios_vm.json](precios_vm.json), Items[0] | Virtual Machines BS Series / B2s | B2s | eastus | 0.0416 | 1 Hour | 0.0 | 2c57ed84-f939-4f5c-ba90-782349a367b8 |
| [precios_storage.json](precios_storage.json), Items[505] | Premium SSD Managed Disks / P4 LRS | P4 LRS Disk | eastus | 5.2795 | 1/Month | 0.0 | 5101ea73-2a5b-4120-b00e-30c13185e5a5 |
| [precios_sql.json](precios_sql.json), Items[26] | SQL Database Single/Elastic Pool General Purpose - Compute Gen5 / 2 vCore Zone Redundancy | Zone Redundancy vCore | eastus | 0.18266 | 1 Hour | 0.0 | 23edd1d1-db61-5d1d-98c4-1799a211f960 |
| [precios_sql.json](precios_sql.json), Items[204] | SQL Database Single/Elastic Pool General Purpose - Compute Gen5 / 2 vCore | vCore | eastus | 0.304434 | 1 Hour | 0.0 | d0fc12d4-91ca-4689-bf8f-9ccdf1b0a619 |
| [precios_sql.json](precios_sql.json), Items[32] | SQL Database Single/Elastic Pool General Purpose - Storage / General Purpose | General Purpose Data Stored | eastus | 0.115 | 1 GB/Month | 0.0 | 19b178e9-0b8b-4db7-962c-b9ccb95cb968 |
| [precios_sql.json](precios_sql.json), Items[245] | SQL Database Single/Elastic Pool General Purpose - Storage / General Purpose Zone Redundancy | General Purpose Zone Redundancy Data Stored | eastus | 0.23 | 1 GB/Month | 0.0 | bbecf26c-5792-5c08-b9bd-f4d1e1166966 |
| [precios_storage.json](precios_storage.json), Items[561] | General Block Blob v2 / Hot LRS | Hot Read Operations | eastus | 0.004 | 10K | 0.0 | c5248cf8-ecba-4807-9304-6a8f14b5805a |
| [precios_storage.json](precios_storage.json), Items[700] | General Block Blob v2 / Hot LRS | Hot LRS Data Stored | eastus | 0.0208 | 1 GB/Month | 0.0 | 272492b3-1c92-4a5f-bee9-52a8e10ca514 |
| [precios_storage.json](precios_storage.json), Items[1061] | General Block Blob v2 / Hot ZRS | Hot ZRS Write Operations | eastus | 0.0625 | 10K | 0.0 | b25223ae-4304-47c3-afc1-521c8523189b |
| [precios_storage.json](precios_storage.json), Items[1272] | General Block Blob v2 / Hot ZRS | Hot ZRS Data Stored | eastus | 0.026 | 1 GB/Month | 0.0 | da71cc90-624a-4006-8936-0718046ad8ab |
| [precios_storage.json](precios_storage.json), Items[1456] | General Block Blob v2 / Hot ZRS | Hot ZRS Read Operations | eastus | 0.004 | 10K | 0.0 | f8f7b1ae-6f4c-41f4-bfd0-bd43bfacaf91 |
| [precios_functions.json](precios_functions.json), Items[4] | Flex Consumption / On Demand | On Demand Total Executions | eastus | 4e-06 | 10 | 25000.0 | 4d397fba-0393-57dd-9da3-f145b5c874fe |
| [precios_functions.json](precios_functions.json), Items[11] | Flex Consumption / On Demand | On Demand Execution Time | eastus | 2.6e-05 | 1 GB Second | 100000.0 | cd5d6bae-9b8d-5456-ab84-46919175c318 |
| [precios_ip.json](precios_ip.json), Items[7] | IP Addresses / Standard | Standard IPv4 Static Public IP | eastus | 0.005 | 1 Hour | 0.0 | 9c150bf9-2bad-430e-a53c-c213804f49ef |
| [precios_lb_global.json](precios_lb_global.json), Items[0] | Load Balancer / Standard | Standard Data Processed | attdetroit1 | 0.005 | 1 GB | 0.0 | 0078afeb-d324-59fb-a518-f37202599a7b |
| [precios_lb_global.json](precios_lb_global.json), Items[4] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | attnewyork1 | 0.025 | 1 Hour | 0.0 | 26059e28-0c50-5e44-85d1-ff0a7c4996db |
| [precios_lb_global.json](precios_lb_global.json), Items[5] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | Global | 0.025 | 1 Hour | 0.0 | 27827eb0-7f60-4928-940b-f5fe15e7a4cb |
| [precios_lb_global.json](precios_lb_global.json), Items[9] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | attdetroit1 | 0.025 | 1 Hour | 0.0 | 3aab66fb-cc68-5d48-b641-59de1dc3cc6d |
| [precios_lb_global.json](precios_lb_global.json), Items[11] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | attdallas1 | 0.025 | 1 Hour | 0.0 | 449eafc4-9b22-53e8-871e-5506e5a46a01 |
| [precios_lb_global.json](precios_lb_global.json), Items[13] | Load Balancer / Standard | Standard Data Processed | attnewyork1 | 0.005 | 1 GB | 0.0 | 4f148389-3c9c-52fb-b2e8-dfd7f0990715 |
| [precios_lb_global.json](precios_lb_global.json), Items[16] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | sgxsingapore1 | 0.025 | 1 Hour | 0.0 | 6b1b4081-be68-5949-9bb1-429157dd9d24 |
| [precios_lb_global.json](precios_lb_global.json), Items[23] | Load Balancer / Standard | Standard Data Processed | attatlanta1 | 0.005 | 1 GB | 0.0 | 9db9111e-ac97-5069-9746-9e2e33deeb80 |
| [precios_lb_global.json](precios_lb_global.json), Items[24] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | attatlanta1 | 0.025 | 1 Hour | 0.0 | a3d5f89a-e7d7-5c71-a9bc-892ef5cee18b |
| [precios_lb_global.json](precios_lb_global.json), Items[28] | Load Balancer / Standard | Standard Included LB Rules and Outbound Rules | US Gov | 0.0313 | 1 Hour | 0.0 | af9c885d-12ee-402c-a6ce-27af4afc3c17 |
| [precios_lb_global.json](precios_lb_global.json), Items[37] | Load Balancer / Standard | Standard Data Processed | sgxsingapore1 | 0.005 | 1 GB | 0.0 | d4db77f6-bf12-54c1-9dd0-84b7ded6e0d7 |
| [precios_lb_global.json](precios_lb_global.json), Items[38] | Load Balancer / Standard | Standard Data Processed | US Gov | 0.006 | 1 GB | 0.0 | d8bbe812-009a-41e6-9376-fb17b8555099 |
| [precios_lb_global.json](precios_lb_global.json), Items[43] | Load Balancer / Standard | Standard Data Processed | Global | 0.005 | 1 GB | 0.0 | dfc7cc11-fbe2-41c8-b6fa-24a574223938 |
| [precios_lb_global.json](precios_lb_global.json), Items[45] | Load Balancer / Standard | Standard Data Processed | attdallas1 | 0.005 | 1 GB | 0.0 | ea908c04-a9c8-5135-b243-e4a57048c8b2 |
| [precios_dns.json](precios_dns.json), Items[58] | Azure DNS / Public | Public Zone | Global (vacío en API) | 0.5 | 1 | 0.0 | 8f967c58-b144-4bd7-8882-8bf02767c839 |
| [precios_dns.json](precios_dns.json), Items[89] | Azure DNS / Public | Public Queries | Global (vacío en API) | 0.4 | 1M | 0.0 | d54686f0-77ff-43f3-9e7c-2099030d32a7 |

# Extractos del contrato oficial aportado

Extracción: 04/10/2026. Edición del documento: 01/09/2026. Fuente: [DOCX inglés oficial](https://www.microsoft.com/licensing/docs/documents/download/OnlineSvcsConsolidatedSLA%28WW%29%28English%29%28September_2026%29%28CR%29.docx).

Transcripción del texto y tablas del original; se normaliza el espacio tipográfico. Las fórmulas como objetos pueden perder formato, por lo que deben contrastarse con el DOCX y las capturas. No es una captura de sitio web ni una nueva traducción contractual.

## Azure DNS

Additional Definitions :

“ DNS Zone ” refers to a deployment of the Azure DNS Service containing a DNS zone and record sets.

“ Deployment Minutes ” is the total number of minutes that a given DNS Zone has been deployed in Microsoft Azure during an Applicable Period .

“ Maximum Available Minutes ” is the sum of all Deployment Minutes across all DNS Zones deployed in a given Microsoft Azure subscription during an Applicable Period .

“ Valid DNS Request ” means a DNS request to an Azure DNS Service name server associated with a DNS Zone for a matching record set within the DNS Zone.

“ Downtime ” is the total accumulated Maximum Available Minutes during which the DNS Zone is unavailable. A minute is considered unavailable for a given DNS Zone if a DNS response is not received within two seconds to a valid DNS Request, provided that the valid DNS Request is made to all name servers associated with the DNS Zone and retries are continually attempted for at least 60 consecutive seconds.

Uptime Percentage : The Uptime Percentage is calculated using the following formula :

Maximum Available Minutes-Downtime Maximum Available Minutes x 100

Service Credit :

Uptime Percentage Service Credit <100 10% < 99.99% 25% < 99.5% 100%

## Azure Functions

Additional Definitions

" Function App " is a collection of one or more functions deployed with an associated trigger.

Uptime Calculation and Service Levels for Function App on the Consumption Plan

" Total Triggered Executions " is the total number of all Function App executions triggered by Customer in a given Microsoft Azure subscription during an Applicable Period.

“ Unavailable Executions ” is the total number of executions within Total Triggered Executions which failed to run. An execution failed to run when the given Function App history log did not capture any output five (5) minutes after the trigger is successfully fired.

" Uptime Percentage " for Function Apps on the Consumption plan is calculated as Total Triggered Executions less Unavailable Executions divided by Total Triggered Executions multiplied by 100.

Total Triggered Executions-Unavailable Executions Total Triggered Executions x 100

The following Service Levels and Service Credits are applicable to Customer’s use of Function App on the Consumption plan.

Uptime Percentage Service Credit < 99.95% 10% < 99% 25% < 95% 100%

Uptime Calculation and Service Levels for Function Apps on the Flex Consumption Plan, Premium Plan, or the Dedicated App Service Plan

" Deployment Minutes " is the total number of minutes that a given Function App is available to be triggered during an Applicable Period. Deployment Minutes are measured based on the total time that the service is available to trigger a function execution and not based on the potential number of function executions that might be triggered during a given Applicable Period.

" Maximum Available Minutes " is the sum of all Deployment Minutes for a given Function App deployed by Customer in a given Microsoft Azure subscription during an Applicable Period.

" Downtime " is the total number of minutes within Maximum Available Minutes, during which the Function App is unavailable to be triggered. A minute is considered unavailable for a given Function App when there is no connectivity between plan on which the Function App is hosted (the Flex Consumption plan, Premium plan, or the Dedicated App Service plan) and Microsoft’s Internet gateway.

" Uptime Percentage " for Function Apps on the Flex Consumption plan, Premium plan, or the Dedicated App Service plan is calculated as Maximum Available Minutes less Downtime divided by Maximum Available Minutes multiplied by 100.

Maximum Available Minutes-Downtime Maximum Available Minutes x 100

Service Credit:

Uptime Percentage Service Credit < 99.95% 10% < 99% 25% < 95% 100%

## Azure Load Balancer

Additional Definitions :

“ Load Balanced Endpoint ” is an IP address and associated IP transport port definition.

“ Healthy Virtual Machine ” is a Virtual Machine which returns a Success Code for the health probe sent by the Azure Standard Load Balancer. The Virtual Machine must have Network Security Group rules permitting communication with the load balanced port.

“ Connectivity ” is bi-directional network traffic over supported IP transport protocols that can be sent and received from any IP address configured to allow traffic.

Uptime Calculation and Service Levels for Azure Load Balancer

“ Maximum Available Minutes ” is the total number of minutes that a given Azure Standard Load Balancer (serving two or more Healthy Virtual Machines) has been deployed by Customer in a Microsoft Azure subscription during an Applicable Period .

“ Downtime ” is the total number of minutes within Maximum Available Minutes during which the given Azure Standard Load Balancer is unavailable. A minute is considered unavailable if all Healthy Virtual Machines have no Connectivity through the Load Balanced Endpoint. Downtime does not include minutes resulting from SNAT port exhaustions.

" Uptime Percentage " for Azure Standard Load Balancer is calculated as Maximum Available Minutes less Downtime divided by Maximum Available Minutes multiplied by 100.

Uptime Percentage : The Uptime Percentage is calculated using the following formula:

Maximum Available Minutes-Downtime Maximum Available Minutes x 100

The following Service Levels and Service Credits are applicable to Customer’s use of Azure Load Balancer:

Uptime Percentage Service Credit < 99.9 9 % 10 % < 99 .9 % 25 %

Service Level Exceptions : No SLA is provided for Basic Load Balancer .

## Azure SQL Database

Additional Definitions :

" Availability Zone " is a fault-isolated area within an Azure region, providing redundant power, cooling, and networking.

" Database " means any Microsoft Azure SQL Database created in any of the Service tiers and deployed either as a single database or in an Elastic Pool.

" Zone Redundant Deployment " is a Database that is deployed across multiple Availability Zones.

" Primary " means any Database that has active geo-replication relationship with a Database in other Azure regions. Primary can process read and write requests from the application.

" Secondary " means any Database that maintains asynchronous geo-replication relationship with a Primary in another Azure region and can be used as a failover target. Secondary can process read-only requests from applications.

" Compliant Secondary " means any Secondary that is created with the same configuration and in the same service tier as the Primary. If the Secondary is created in an elastic pool, it is considered Compliant if both Primary and Secondary are created in elastic pools with matching configurations and with density not exceeding 250 databases for a compliant configuration.

Uptime Calculation and Service Levels for Azure SQL Database Service

" Deployment Minutes " is the total number of minutes that a given Database has been operational in Microsoft Azure during an Applicable Period .

“ Maximum Available Minutes ” is the sum of all Deployment Minutes for a given Microsoft Azure subscription during an Applicable Period .

Downtime : is the total accumulated Deployment Minutes across all Databases in a given Microsoft Azure subscription during which the Database is unavailable. A minute is considered unavailable for a given Database if all continuous attempts by Customer to establish a connection to the Database within the minute fail.

Uptime Percentage : for a given Database is calculated as Maximum Available Minutes less Downtime divided by Maximum Available Minutes in an Applicable Period for a given Microsoft Azure subscription.

The Uptime Percentage is calculated using the following formula:

Maximum Available Minutes-Downtime Maximum Available Minutes x 100

The following Service Levels and Service Credits are applicable to Customer's use of the General Purpose, Business Critical , Premium or Hyperscale tiers of the SQL Database Service configured for Zone Redundant Deployments :

Uptime Percentage Service Credit < 99.99 5 % 10% < 99% 25% < 95% 100%

The following Service Levels and Service Credits are applicable to Customer's use of the Hyperscale, Business Critical, Premium or General Purpose, of the SQL Database Service not configured for Zone Redundant Deployments :

Uptime Percentage Service Credit < 99.99% 10% < 99% 25% < 95% 100%

The following Service Levels and Service Credits are applicable to Customer's use of the Basic or Standard tiers of the SQL Database Service :

Uptime Percentage Service Credit < 99.99% 10% < 99% 25% < 95% 100%

## Storage Accounts

Additional Definitions :

“ Archive Access Tier ” is a tier optimized for storing data that is rarely accessed, and that has flexible latency requirements, on the order of hours.

“ Average Error Rate ” for an Applicable Period is the sum of Error Rates for each hour in the Applicable Period divided by the total number of hours in the Applicable Period .

“ Blob Storage Account ” is a storage account specialized for storing data as blobs and provides the ability to specify an access tier indicating how frequently the data in that account is accessed.

“ Block Blob Storage Account ” is a storage account specialized for storing data as block or append blobs on solid-state drives.

“ Col d Access Tier ” is an attribute of a b lob or a ccount indicating it is rarely accessed and has a lower availability service level than blobs in Hot A ccess T ier.

“ Cool Access Tier ” is an attribute of a b lob , file share , or a ccount indicating it is infrequently accessed and has a lower availability service level than blobs in Hot A ccess T ier.

“ Hot Access Tier ” is an attribute of a blob , file share, or account indicating it is frequently accessed.

“ Excluded Transactions ” are storage transactions that do not count toward either Total Storage Transactions or Failed Storage Transactions. Excluded Transactions include pre-authentication failures; authentication failures; attempted transactions for storage accounts over their prescribed quotas; creation or deletion of containers, file shares, tables, or queues; clearing of queues; and copying blobs or files between storage accounts.

“ Error Rate ” is the total number of Failed Storage Transactions divided by the Total Storage Transactions during a set time interval (currently set at one hour). If the Total Storage Transactions in a given one-hour interval is zero, the error rate for that interval is 0%.

“ Failed Storage Transactions ” is the set of all storage transactions within Total Storage Transactions that are not completed within the Maximum Processing Time associated with their respective transaction type, as specified in the table below. Maximum Processing Time includes only the time spent processing a transaction request within the Storage Service and does not include any time spent transferring the request to or from the Storage Service.

Transaction Types Maximum Processing Time PutBlob and GetBlob (includes blocks and pages) Get Valid Page Blob Ranges Two (2) seconds multiplied by the number of MBs transferred in the course of processing the request PutFile and GetFile Two (2) seconds multiplied by the number of MBs transferred in the course of processing the request Copy Blob Ninety (90) seconds (where the source and destination blobs are within the same storage account) Copy File Ninety (90) seconds (where the source and destination files are within the same storage account) PutBlockList GetBlockList Sixty (60) seconds Table Query List Operations Find Operations Ten (10) seconds (to complete processing or return a continuation) Batch Table Operations Thirty (30) seconds All Single Entity Table Operations All other Blob, File, and Message Operations Two (2) seconds

These figures represent maximum processing times. Actual and average times are expected to be much lower.

Failed Storage Transactions do not include:

Transaction requests that are throttled by the Storage Service due to a failure to obey appropriate back-off principles.

Transaction requests having timeouts set lower than the respective Maximum Processing Times specified above.

Read transactions requests to RA-GRS and RA-GZRS Accounts for which you did not attempt to execute the request against Secondary Region associated with the storage account if the request to the Primary Region was not successful.

Read transaction requests to RA-GRS and RA-GZRS Accounts that fail due to Geo-Replication Lag.

“ Geo Replication Lag ” for GRS , GZRS, RA-GRS , and RA-G Z RS Accounts is the time it takes for data stored in the Primary Region of the storage account to replicate to the Secondary Region of the storage account. Because GRS , GZRS, RA-GRS , and RA-G Z RS Accounts are replicated asynchronously to the Secondary Region, data written to the Primary Region of the storage account will not be immediately available in the Secondary Region. You can query the Geo Replication Lag for a storage account, but Microsoft does not provide any guarantees as to the length of any Geo Replication Lag under this SLA. “ Geo Redundant Storage (GRS) Account ” is a storage account for which data is replicated synchronously within a Primary Region and then replicated asynchronously to a Secondary Region. You cannot directly read data from or write data to the Secondary Region associated with GRS Accounts.

“ Locally Redundant Storage (LRS) Account ” is a storage account for which data is replicated synchronously only within a Primary Region.

“ Primary Region ” is a geographical region in which data within a storage account is located, as selected by you when creating the storage account. You may execute write requests only against data stored within the Primary Region associated with storage accounts.

“ Read Access Geo Redundant Storage (RA-GRS) Account ” is a storage account for which data is replicated synchronously within a Primary Region and then replicated asynchronously to a Secondary Region. You can directly read data from, but cannot write data to, the Secondary Region associated with RA-GRS Accounts.

“ Secondary Region ” is a geographical region in which data within a GRS or RA-GRS Account is replicated and stored, as assigned by Microsoft Azure based on the Primary Region associated with the storage account. You cannot specify the Secondary Region associated with storage accounts.

“ Total Storage Transactions ” is the set of all storage transactions, other than Excluded Transactions, attempted within a one-hour interval across all storage accounts in the Storage Service in a given subscription.

“ Transaction Optimized Access Tier ” is an attribute of a n Azure file share indicating it is accessed frequently .

“ Zone Redundant Storage (ZRS) Account ” is a storage account for which data is replicated across multiple facilities. These facilities may be within the same geographical region or across two geographical regions.

“ Geo Z one R edundant Storage ( G ZRS) Account ” is a storage account for which data is replicated across multiple facilities. These facilities may be within the same geographical region or across two geographical regions. D ata is also replicated synchronously within a Primary Region and then replicated asynchronously to a Secondary Region. You cannot directly read data from or write data to the Secondary Region associated with G Z RS Accounts.

“ Read Access Geo Z one R edundant Storage ( RA-G ZRS) Account ” is a storage account for which data is replicated across multiple facilities. These facilities may be within the same geographical region or across two geographical regions. D ata is also replicated synchronously within a Primary Region and then replicated asynchronously to a Secondary Region. You can directly read data from, but cannot write data to, the Secondary Region associated with RA-G Z RS Accounts.

Uptime Percentage : Uptime Percentage is calculated using the following formula:

100%-Average Error Rate

Hot , and Transaction Optimized Access Tiers

Service Credit –LRS, ZRS, GRS , GZRS, RA-GRS , and RA-GZRS (write requests) for Hot, and Transaction Optimized Access Tiers :

Uptime Percentage Service Credit < 99.9% 10% < 99% 25%

Service Credit –RA-GRS and RA-GZRS (read requests) for Hot, and Transaction Optimized Access Tiers

Uptime Percentage Service Credit < 99.99% 10% < 99% 25%

Service Credit – LRS, ZRS, GRS and GZRS ( read requests) for Hot, and Transaction Optimized Access Tiers

Uptime Percentage Service Credit < 99 .9 % 10% < 9 9 % 25%

Cool, Cold , and Archive Tiers

Service Credit – LRS , ZRS, GRS, GZRS, RA-GRS , & RA-GZRS (write requests) for Cool, Cold , and Archive Access Tiers

Uptime Percentage Service Credit < 99% 10% < 98% 25%

Service Credit – RA-GRS & RA- GZRS ( read requests) Cool, Cold , and Archive Access Tiers

Uptime Percentage Service Credit < 99.9% 10% < 98% 25%

Service Credit – LRS, ZRS, GRS, GZRS (read requests) for Cool, Cold, and Archive Access Tiers

Uptime Percentage Service Credit < 99.9% 10% < 98% 25%

Service Exceptions : Cool , Cold and Archive SLA are applicable only to storage account types that support Cool , Cold and Archive tier.

## Virtual Machines

Additional Definitions :

“ Availability Set ” refers to two or more Virtual Machines deployed across different Fault Domains to avoid a single point of failure.

“ Availability Zone ” is a fault-isolated area within an Azure region, providing redundant power, cooling, and networking.

" Azure Dedicated Host " provides physical servers that host one or more Azure virtual machines with the (default) setting of autoReplaceOnFailure required for any SLA.

“ Data Disk ” is a persistent virtual hard disk, attached to a Virtual Machine, used to store application data.

" Dedicated Host Group " is a collection of Azure Dedicated Hosts deployed within an Azure region across different Fault Domains to avoid a single point of failure.

“ Fault Domain ” is a collection of servers that share common resources such as power and network connectivity.

“ Operating System Disk ” is a persistent virtual hard disk, attached to a Virtual Machine, used to store the Virtual Machine’s operating system.

“ Shared Disk ” is a Data Disk attached to multiple Virtual Machines simultaneously.

“ Single- Instance Virtual Machine ” is defined as any single Microsoft Azure Virtual Machine that either is not deployed in an Availability Set or has only one instance deployed in an Availability Set.

“ Virtual Machine ” refers to persistent instance types that can be deployed individually or as part of an Availability Set or using a Dedicated Host Group. A virtual machine can be deployed in a multi-tenant environment in Azure or in an isolated, single-tenant environment using Azure Dedicated Hosts .

“ Virtual Machine Connectivity ” is bi-directional network traffic between the Virtual Machine and other IP addresses using TCP or UDP network protocols in which the Virtual Machine is configured for allowed traffic. The IP addresses can be IP addresses in the same Cloud Service as the Virtual Machine, IP addresses within the same virtual network as the Virtual Machine or public, routable IP addresses.

Uptime Calculation and Service Levels for Virtual Machines in Availability Zones

“ Maximum Available Minutes ” is the total accumulated minutes during an Applicable Period that have two or more instances deployed across two or more Availability Zones in the same region. Maximum Available Minutes is measured from when at least two Virtual Machines across two Availability Zones in the same region have both been started resultant from action initiated by Customer to the time Customer has initiated an action that would result in stopping or deleting the Virtual Machines.

“ Downtime ” is the total accumulated minutes that are part of Maximum Available Minutes that have no Virtual Machine Connectivity in the region.

“ Uptime Percentage ” for Virtual Machines in Availability Zones is calculated as Maximum Available Minutes less Downtime divided by Maximum Available Minutes in an Applicable Period for a given Microsoft Azure subscription. Uptime Percentage is represented by the following formula:

Monthly Uptime %= (Maximum Available Minutes-Downtime) Maximum Available Minutes x 100

Service Credit :

The following Service Levels and Service Credits are applicable to Customer’s use of Virtual Machines deployed across two or more Availability Zones in the same region :

Uptime Percentage Service Credit < 99.9 9 % 10 % < 99% 25 % < 95 % 100 %

Uptime Calculation and Service Levels for Virtual Machines in an Availability Set or in the same Dedicated Host Group

Maximum Available Minutes : The total accumulated minutes during an Applicable Period for all Internet facing Virtual Machines that have two or more instances deployed in the same Availability Set on in the same Dedicated Host Group. Maximum Available Minutes is measured from when at least two Virtual Machines in the same Availability Set, or same Dedicated Host Group, have both been started resultant from action initiated by you to the time you have initiated an action that would result in stopping or deleting the Virtual Machines.

Downtime : The total accumulated minutes that are part of Maximum Available Minutes that have no Virtual Machine Connectivity.

Uptime Percentage : for Virtual Machines is calculated as Maximum Available Minutes less Downtime divided by Maximum Available Minutes in an Applicable Period for a given Microsoft Azure subscription. Uptime Percentage is represented by the following formula:

Monthly Uptime %= (Maximum Available Minutes-Downtime) Maximum Available Minutes x 100

Service Credit :

The following Service Levels and Service Credits are applicable to Customer’s use of Virtual Machines in an Availability Set or same Dedicated Host Group. This SLA does not apply to Availability Sets leveraging Azure shared disks :

Uptime Percentage Service Credit < 99.95% 10% < 99% 25% < 95% 100%

Uptime Calculation and Service Levels for Single-Instance Virtual Machines and Virtual Machines using the same Shared Disks

“ Minutes in the Applicable Period ” is the total number of minutes in a given Applicable Period .

Downtime : is the total accumulated minutes that are part of Minutes in the Applicable Period that have no Virtual Machine Connectivity.

Uptime Percentage : is calculated by subtracting from 100% the percentage of Minutes in the Applicable Period in which any Single - Instance Virtual Machine had Downtime or in which all Virtual Machines using the same Shared Disk had Downtime .

Monthly Uptime %= (Minutes in the Applicable Period - Downtime) Minutes in the Applicable Period x 100

Service Credit :

The following Service Levels and Service Credits are applicable to Customer’s use of Single-Instance Virtual Machines and Virtual Machines using the same Shared Disks by Disk type . For any Single - Instance Virtual Machine using multiple disk types and for all Virtual Machines using the same Shared Disks of multiple types* , the lowest SLA of all the disks on the Virtual Machine will apply :

*For example, given two Virtual Machines VM1 and VM2 using a Premium SSD Shared Disk and a Standard SSD Shared Disk, the uptime SLA for VM1 and VM2 will be the same as the SLA for a Single-Instance Virtual Machine using Standard SSD, as shown below.

Uptime Percentage (Premium SSD, Premium SSD v2, and Ultra Disk)** Uptime Percentage (Standard SSD Managed Disk) Uptime Percentage (Standard HDD Managed Disk) Service Credit < 99.9% <99.5% <95% 10% < 99% <95% <92% 25% < 95% <90% <90% 100%

**Premium SSD for all Operating System Disks, and Premium SSD, Premium SSD v2 or Ultra Disk for all Data Disks.

# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*
- *Choose the appropriate solution (VM or App Service) for deploying the app*
- *Justify your choice*

App Service: For this scenario, I think that [at least at the first stages of the app development] the App Service is the proper solution. It is easy to setup, since it is an PaaS, we do not have to consider anything regarding the infrastructure, except to define the proper tier during the setup. The programming language that we chose is Python, which is among the languages that the App Service can support. It's main limitation is the hardware - 14 Gigabytes of memory and 4 vCPUs. The app more likely won't need more than that, so we will probably be fine. Plus we can start in a lower tier, to lower the upfront cost, and then scale - either horizontally or vertically. Regarding cost, although is reasonable, we must have in mind that we are always paying for the App Service, no matter if we use it.

Virtual Machine: It is considered as IaaS, which on one hand gives us the flexibility to chose the exact hardware we want and to install the proper software on that, on the other hand that freedom comes with a price, we need to configure the VM manually, which needs time and knowledge. And VM's support scaling, since we can group together several VMs. In terms of cost, we only pay for the time we use the VM, which gives us the opportunity to save some money, if we properly manage the time the VM is running. But we must always have in mind that, as it was mentioned in the classroom, if the app requirements are within App Service limitations, it is better to go with App Service.

### Assess app changes that would change your decision.

*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 

As mentioned above, since the programming language we chose to be Python, which is supported in both cases, the main consideration is how the app might change in the future. If it is about to be something that it will require computing power - or in general hardware, like using it for Machine Learning or setting up a new Social Network in which the users that will be registered can share videos/photos, or even edit them through app, then the hardware requirements will reach the limit, so it might be better to switch of the App service and go for VM.
Another case could be the need to use another programming language, that is not supported in the App Service. 
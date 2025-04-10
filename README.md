Download Neo4j Desktop

Install APOC plugin
https://neo4j.com/docs/apoc/5/installation/?_gl=1*1gdaha5*_ga*MTk0MDk5NjkzNy4xNzQxNjUyMjM2*_ga_DZP8Z65KK4*MTc0MTY1MjIzNC4xLjEuMTc0MTY1NTIyNi4wLjAuMA..


Add jar file to folder

```
Add config to neo4j.conf

```
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.*
```
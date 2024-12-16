**User Guide for Database Masking Tool
**This guide provides step-by-step instructions for using the Database Masking Tool, which helps transfer data between databases while applying various levels of masking to sensitive information.
Features

**Three Masking Levels:
**Low: Minimal masking, suitable for non-sensitive data.
Medium: Moderate masking, suitable for semi-sensitive data.
High: Full masking for data containing Personally Identifiable Information (PII).

**Supported Database Types:
**pg for PostgreSQL
mariadb for MariaDB
mysql for MySQL

**Prerequisites**
Ensure the following Python libraries are installed on your system:
Faker
psycopg2
mysql
These can be installed using pip:
pip install Faker psycopg2 mysql


**Usage Instructions
**The tool is executed via a Python script named Database.py. Below is the general command format:
python Database.py [source database type] [source database name] [destination database type] [destination database name] [level of masking]
Command Parameters
[source database type]: The type of the source database (pg, mariadb, mysql).
[source database name]: The name of the source database.
[destination database type]: The type of the destination database (pg, mariadb, mysql).
[destination database name]: The name of the destination database.
[level of masking]: The desired masking level (low, medium, high).


**Example**
Here is an example command to transfer data:
Scenario: The source database is mysourcedb of type mysql. The destination database is pgdestdb of type postgres. You want to apply high PII masking.
python Database.py mysql mysourcedb pg pgdestdb high

**Explanation of the Command:
**mysql: Source database type.
mysourcedb: Source database name.
pg: Destination database type.
pgdestdb: Destination database name.
high: Level of masking.

**Additional Notes
**Ensure you have appropriate permissions to access the source and destination databases.
The script requires Python to be installed on your system.
Verify database connectivity before running the script.
If the masking type is not defined for a specific field, the tool will prompt you to choose between two options:
No masking: Press 1 to apply no masking to the field.
Fixed masking: Press 2 to mask the field with the value "***".

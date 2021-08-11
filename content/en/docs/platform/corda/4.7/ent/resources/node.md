Azure SQL/SQL SERVER

#In a production environment, the configuration obfuscator should be used.

"dataSourceProperties" : {

    "dataSource" : {

        "url" : "jdbc:sqlserver://SQLSERVER:1433;database=DATABASE;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;",

        "user" : "USER"

        "password" : "PASSWORD"

    },

    "dataSourceClassName" : "com.microsoft.sqlserver.jdbc.SQLServerDataSource"

}

postGres RDBMS

#In a production environment, the configuration obfuscator should be used.

"dataSourceProperties" : {

    "dataSource" : {

        "url" : "jdbc:postgresql://SERVERNAME:5432/DATABASENAME",

        "user" : "user",

        "password" : "password"

    },

    "dataSourceClassName" : "org.postgresql.ds.PGSimpleDataSource"

},

Oracle RDBMS

#In a production environment, the configuration obfuscator should be used.

"dataSourceProperties" : {

    "dataSourceClassName" : "oracle.jdbc.pool.OracleDataSource",

    "dataSource" : {

        "url" : "jdbc:oracle:thin:@SERVERNAME:1521/DATABASENAME",

        "user" :  "user",

        "password" : "password"

    }

},

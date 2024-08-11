
DROP TABLE IF EXISTS adp_dwh.co_sandbox_datos.tmp_datacontracts_val;
CREATE TABLE adp_dwh.co_sandbox_datos.tmp_datacontracts_val (
    id INT IDENTITY(1,1),
    created_at datetime default sysdate,
    modified_at datetime default sysdate,
    raw_data super,
    PRIMARY KEY (id)
    )
;

-- GRANT SELECT ON TABLE adp_dwh.co_sandbox_datos.tmp_datacontracts_val TO ROL;


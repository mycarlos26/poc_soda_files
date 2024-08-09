drop table if exists adp_dwh.co_sandbox_datos.tmp_test_fabio;
create table adp_dwh.co_sandbox_datos.tmp_test_fabio (id int, raw_data super);

insert into adp_dwh.co_sandbox_datos.tmp_test_fabio
select 1 as id, '{"llave": "Valor"}'
;


select *
from adp_dwh.co_sandbox_datos.tmp_test_fabio
;

/*
Funciones para trabajar con JSON: https://docs.aws.amazon.com/redshift/latest/dg/json-functions.html
- JSON_PARSE function:
	https://docs.aws.amazon.com/redshift/latest/dg/JSON_PARSE.html
	JSON_PARSE( {json_string | binary_value} )
	SELECT JSON_PARSE('[10001,10002,"abc"]');
- JSON_EXTRACT_PATH_TEXT
	https://docs.aws.amazon.com/redshift/latest/dg/JSON_EXTRACT_PATH_TEXT.html
Tipo de dato con el que se debe crear el campo en la tabla para usar las funciones: https://docs.aws.amazon.com/redshift/latest/dg/super-overview.html

 * 
 * 
 * */

select
	id
	, raw_data::varchar
	, CAN_JSON_PARSE(raw_data::VARCHAR) as can_json
	, JSON_SERIALIZE(raw_data) as json
	, JSON_EXTRACT_PATH_TEXT(raw_data::varchar, 'llave') as extraccion
	, JSON_EXTRACT_PATH_TEXT(raw_data::varchar, 'llave_inexistente') as inexistente
from adp_dwh.co_sandbox_datos.tmp_test_fabio
;


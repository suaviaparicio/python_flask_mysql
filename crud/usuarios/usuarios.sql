use esquema_registro_usuarios;
SELECT * FROM usuarios;
SELECT * FROM ninjas;

SELECT * FROM usuarios WHERE ID=8;

SELECT * FROM dojos 
LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id 
WHERE dojos.id = 7;

SELECT * FROM ninjas
JOIN dojos ON ninjas.dojo_id = dojos.id;
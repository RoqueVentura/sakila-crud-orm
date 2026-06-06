-- =============================================================
--  FASE I  |  Sakila DB  |  SQL Scripts
--  Parte A: 10 Consultas
--  Parte B: Unique Constraints
--  Parte C: 10 Consultas de validacion
-- =============================================================

USE sakila;

-- -----------------------------------------------------------
-- PARTE A: 10 CONSULTAS
-- -----------------------------------------------------------

-- Q1. Ciudades con su pais
SELECT ci.city_id, ci.city AS ciudad, co.country AS pais
FROM city ci
JOIN country co ON ci.country_id = co.country_id
ORDER BY co.country, ci.city
LIMIT 20;

-- Q2. Total de ciudades por pais - top 10
SELECT co.country AS pais, COUNT(ci.city_id) AS total_ciudades
FROM country co
JOIN city ci ON co.country_id = ci.country_id
GROUP BY co.country
ORDER BY total_ciudades DESC
LIMIT 10;

-- Q3. Peliculas con duracion mayor al promedio
SELECT film_id, title, length, rating
FROM film
WHERE length > (SELECT AVG(length) FROM film)
ORDER BY length DESC
LIMIT 15;

-- Q4. Top 10 peliculas mas rentadas
SELECT f.title, COUNT(r.rental_id) AS total_rentas
FROM film f
JOIN inventory i ON f.film_id      = i.film_id
JOIN rental    r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY total_rentas DESC
LIMIT 10;

-- Q5. Clientes con mas de 30 rentas
SELECT cu.customer_id,
       CONCAT(cu.first_name, ' ', cu.last_name) AS cliente,
       COUNT(r.rental_id) AS rentas
FROM customer cu
JOIN rental r ON cu.customer_id = r.customer_id
GROUP BY cu.customer_id
HAVING rentas > 30
ORDER BY rentas DESC;

-- Q6. Ingresos totales por categoria
SELECT ca.name AS categoria, ROUND(SUM(p.amount), 2) AS ingresos_usd
FROM category ca
JOIN film_category fc ON ca.category_id  = fc.category_id
JOIN inventory     i  ON fc.film_id      = i.film_id
JOIN rental        r  ON i.inventory_id  = r.inventory_id
JOIN payment       p  ON r.rental_id     = p.rental_id
GROUP BY ca.name
ORDER BY ingresos_usd DESC;

-- Q7. Inventario por tienda
SELECT s.store_id, COUNT(i.inventory_id) AS total_inventario
FROM store s
JOIN inventory i ON s.store_id = i.store_id
GROUP BY s.store_id;

-- Q8. Top 10 actores con mas peliculas
SELECT a.actor_id,
       CONCAT(a.first_name, ' ', a.last_name) AS actor,
       COUNT(fa.film_id) AS peliculas
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id
ORDER BY peliculas DESC
LIMIT 10;

-- Q9. Peliculas que nunca han sido rentadas
SELECT f.film_id, f.title
FROM film f
WHERE f.film_id NOT IN (
    SELECT DISTINCT i.film_id
    FROM inventory i
    JOIN rental r ON i.inventory_id = r.inventory_id
)
LIMIT 10;

-- Q10. Estadisticas de rental_rate por rating
SELECT rating,
       COUNT(*)                                       AS total_films,
       ROUND(AVG(rental_rate), 2)                     AS media_precio,
       ROUND(MIN(rental_rate), 2)                     AS minimo,
       ROUND(MAX(rental_rate), 2)                     AS maximo,
       ROUND(MAX(rental_rate) - MIN(rental_rate), 2)  AS rango
FROM film
GROUP BY rating
ORDER BY rating;


-- -----------------------------------------------------------
-- PARTE B: UNIQUE CONSTRAINTS
-- -----------------------------------------------------------

ALTER TABLE country
ADD CONSTRAINT uq_country_name UNIQUE (country);

ALTER TABLE city
ADD CONSTRAINT uq_city_country UNIQUE (city, country_id);

ALTER TABLE film
ADD CONSTRAINT uq_film_title_year UNIQUE (title, release_year);

ALTER TABLE actor
ADD CONSTRAINT uq_actor_fullname UNIQUE (first_name, last_name);

ALTER TABLE category
ADD CONSTRAINT uq_category_name UNIQUE (name);

-- Para revertir:
-- ALTER TABLE country  DROP INDEX uq_country_name;
-- ALTER TABLE city     DROP INDEX uq_city_country;
-- ALTER TABLE film     DROP INDEX uq_film_title_year;
-- ALTER TABLE actor    DROP INDEX uq_actor_fullname;
-- ALTER TABLE category DROP INDEX uq_category_name;


-- -----------------------------------------------------------
-- PARTE C: 10 CONSULTAS POST-CONSTRAINTS
-- -----------------------------------------------------------

-- V1. UNIQUE constraints activos en sakila
SELECT TABLE_NAME AS tabla, CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'sakila' AND CONSTRAINT_TYPE = 'UNIQUE'
ORDER BY TABLE_NAME;

-- V2. Ciudades duplicadas (deberian ser 0 tras el constraint)
SELECT city, country_id, COUNT(*) AS ocurrencias
FROM city GROUP BY city, country_id HAVING ocurrencias > 1;

-- V3. Paises duplicados
SELECT country, COUNT(*) AS ocurrencias
FROM country GROUP BY country HAVING ocurrencias > 1;

-- V4. Films con titulo + anio duplicado
SELECT title, release_year, COUNT(*) AS ocurrencias
FROM film GROUP BY title, release_year HAVING ocurrencias > 1;

-- V5. Actores con nombre completo duplicado
SELECT first_name, last_name, COUNT(*) AS ocurrencias
FROM actor GROUP BY first_name, last_name HAVING ocurrencias > 1;

-- V6. Peliculas por idioma
SELECT l.name AS idioma, COUNT(f.film_id) AS total_films
FROM language l
JOIN film f ON l.language_id = f.language_id
GROUP BY l.name;

-- V7. Clientes activos vs inactivos por tienda
SELECT store_id,
       SUM(active)     AS activos,
       SUM(1 - active) AS inactivos
FROM customer GROUP BY store_id;

-- V8. Promedio dias de renta por categoria
SELECT ca.name AS categoria,
       ROUND(AVG(f.rental_duration), 2) AS dias_renta_prom
FROM category ca
JOIN film_category fc ON ca.category_id = fc.category_id
JOIN film          f  ON fc.film_id     = f.film_id
GROUP BY ca.name ORDER BY dias_renta_prom DESC;

-- V9. Top 5 ciudades con mas clientes
SELECT ci.city, COUNT(cu.customer_id) AS total_clientes
FROM city ci
JOIN address  a  ON ci.city_id   = a.city_id
JOIN customer cu ON a.address_id = cu.address_id
GROUP BY ci.city ORDER BY total_clientes DESC LIMIT 5;

-- V10. Costo por rating
SELECT rating,
       MAX(replacement_cost)            AS max_costo,
       MIN(replacement_cost)            AS min_costo,
       ROUND(AVG(replacement_cost), 2)  AS prom_costo
FROM film GROUP BY rating;

CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR phone LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM phonebook
    ORDER BY name
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;

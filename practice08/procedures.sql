
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users(users JSON)
LANGUAGE plpgsql AS $$
DECLARE
    u JSON;
    bad_data JSON := '[]'::JSON;
    p_name TEXT;
    p_phone TEXT;
BEGIN
    FOREACH u IN ARRAY json_array_elements(users) LOOP
        p_name := u->>'name';
        p_phone := u->>'phone';
        
        IF p_phone ~ '^\d+$' THEN
            CALL insert_or_update_user(p_name, p_phone);
        ELSE
            bad_data := bad_data ||  u;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Invalid entries: %', bad_data;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;

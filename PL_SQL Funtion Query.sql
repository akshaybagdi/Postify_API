-- First, let's check and set the correct schema
SET search_path TO public;

-- Function to get post details by ID
CREATE OR REPLACE FUNCTION public.get_post_by_id(
    p_post_id INTEGER
)
RETURNS TABLE (
    post_title VARCHAR,
    post_content TEXT,
    post_category VARCHAR,
    post_is_published BOOLEAN,
    post_rating  NUMERIC(3,2),
    post_website VARCHAR
) AS 
$$
BEGIN
    -- Check if post exists
    IF NOT EXISTS (SELECT 1 FROM public."Postify_post" WHERE id = p_post_id) THEN
        RAISE EXCEPTION 'Post with ID % does not exist', p_post_id;
    END IF;

    -- Return the post details
    RETURN QUERY 
    SELECT 
        title,
        content,
        category,
        is_published,
        rating,
        website
    FROM public."Postify_post"
    WHERE id = p_post_id;

    -- If no rows returned (additional safety check)
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No post found with ID %', p_post_id;
    END IF;

END;
$$ LANGUAGE plpgsql;


SELECT * FROM get_post_by_id(3);
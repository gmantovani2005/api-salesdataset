SELECT COUNT(*) FROM category;        -- 6
SELECT COUNT(*) FROM region;          -- 3
SELECT COUNT(*) FROM payment_method;  -- 3
SELECT COUNT(*) FROM product;         -- ~217
SELECT COUNT(*) FROM sales_order;     -- 240
SELECT SUM(total_revenue) FROM sales_order;